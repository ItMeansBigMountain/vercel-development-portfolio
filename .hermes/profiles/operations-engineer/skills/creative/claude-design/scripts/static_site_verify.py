#!/usr/bin/env python3
"""Verify a static HTML site served over HTTP.

Usage:
  python scripts/static_site_verify.py http://127.0.0.1:4177/ index.html events.html volunteer.html

Checks:
- each page returns HTTP 200
- local stylesheet/script/image references return HTTP 200
- same-site fragment links point to existing IDs
- reports page byte counts and image refs
"""
from __future__ import annotations

import sys
from html.parser import HTMLParser
from urllib.parse import urljoin, urldefrag, urlparse
from urllib.request import urlopen


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.refs: list[str] = []
        self.ids: set[str] = set()
        self.images: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {k: v for k, v in attrs if v is not None}
        if "id" in attr:
            self.ids.add(attr["id"])
        if tag == "a" and "href" in attr:
            self.refs.append(attr["href"])
        elif tag == "img" and "src" in attr:
            self.images.append(attr["src"])
        elif tag == "link" and attr.get("rel") == "stylesheet" and "href" in attr:
            self.refs.append(attr["href"])
        elif tag == "script" and "src" in attr:
            self.refs.append(attr["src"])


def fetch(url: str) -> tuple[int, bytes]:
    with urlopen(url, timeout=8) as response:  # nosec: local/design verification helper
        return response.status, response.read()


def same_origin(a: str, b: str) -> bool:
    pa, pb = urlparse(a), urlparse(b)
    return (pa.scheme, pa.netloc) == (pb.scheme, pb.netloc)


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print(__doc__.strip())
        return 2

    base_url = argv[1].rstrip("/") + "/"
    pages = argv[2:]
    parsed_pages: dict[str, LinkParser] = {}
    html_by_url: dict[str, str] = {}
    errors: list[tuple[str, str, str | int]] = []

    for page in pages:
        page_url = urljoin(base_url, page)
        status, body = fetch(page_url)
        if status != 200:
            errors.append((page, page_url, status))
            continue
        html = body.decode("utf-8", errors="replace")
        parser = LinkParser()
        parser.feed(html)
        parsed_pages[page_url] = parser
        html_by_url[page_url] = html
        print(f"{page}: {len(body)} bytes, {len(parser.images)} images, {len(parser.refs)} refs")

    for page_url, parser in parsed_pages.items():
        for img in parser.images:
            img_url = urljoin(page_url, img)
            if same_origin(base_url, img_url):
                status, _ = fetch(img_url)
                if status != 200:
                    errors.append((page_url, img, status))

        for href in parser.refs:
            if not href or href.startswith(("mailto:", "tel:", "sms:", "#")):
                continue
            target_url, fragment = urldefrag(urljoin(page_url, href))
            if not same_origin(base_url, target_url):
                continue
            status, body = fetch(target_url)
            if status != 200:
                errors.append((page_url, href, status))
                continue
            if fragment:
                html = html_by_url.get(target_url) or body.decode("utf-8", errors="replace")
                target_parser = LinkParser()
                target_parser.feed(html)
                if fragment not in target_parser.ids:
                    errors.append((page_url, href, "missing-fragment"))

    if errors:
        print("ERRORS:")
        for error in errors:
            print(" -", error)
        return 1

    print("Verification passed: pages, local assets, and same-site fragments load.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

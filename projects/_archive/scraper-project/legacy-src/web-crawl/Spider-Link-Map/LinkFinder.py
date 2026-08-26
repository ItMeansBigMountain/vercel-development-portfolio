from bs4 import BeautifulSoup
from urllib.parse import urljoin

class LinkFinder:
    def __init__(self, base_url, page_url):
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()

    def feed(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a', href=True):
            url = link['href']
            full_url = urljoin(self.base_url, url)
            self.links.add(full_url)

    def get_page_links(self):
        return self.links

    def error(self, message):
        pass

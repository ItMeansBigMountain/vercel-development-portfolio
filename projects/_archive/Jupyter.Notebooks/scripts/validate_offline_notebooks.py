#!/usr/bin/env python3
"""Execute project notebooks in deterministic offline/non-interactive mode.

This smoke runner executes code cells directly in Python instead of starting a
Jupyter kernel. That keeps validation fast and deterministic while still catching
syntax/runtime errors in the sanitized notebook code paths.
"""
from __future__ import annotations

import contextlib
import os
import pathlib
import re
import sys
import traceback

GENERATED_OUTPUTS = {
    "recommended_trades.xlsx",
    "hqm_dataframe.xlsx",
    "Robust_Value_Dataframe.xlsx",
    "user_inputs.txt",
}


def _is_shell_only(line: str) -> bool:
    stripped = line.lstrip()
    return stripped.startswith(("%", "!"))


def _cell_source(cell: dict) -> str:
    source = "".join(cell.get("source", []))
    return "\n".join(line for line in source.splitlines() if not _is_shell_only(line))


def _assert_sanitized(source: str, rel: pathlib.Path, index: int) -> None:
    """Reject code paths that could hang, call live APIs, or embed secrets."""
    for line_no, line in enumerate(source.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if re.search(r"(?<![A-Za-z0-9_])input\s*\(", stripped):
            raise RuntimeError(f"raw input() call remains in {rel} cell {index} line {line_no}")
        if "requests.get(" in stripped:
            raise RuntimeError(f"raw requests.get() call remains in {rel} cell {index} line {line_no}")
        if stripped.startswith("IEX_CLOUD_API_TOKEN") and "get_iex_token()" not in stripped:
            raise RuntimeError(f"token assignment is not environment-based in {rel} cell {index} line {line_no}")


@contextlib.contextmanager
def pushd(path: pathlib.Path):
    previous = pathlib.Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(previous)


def main() -> int:
    try:
        import nbformat
    except Exception as exc:  # pragma: no cover - dependency guard for humans
        print(f"Missing notebook validation dependency: {exc}", file=sys.stderr)
        return 2

    project_root = pathlib.Path(__file__).resolve().parents[1]
    notebooks = sorted(project_root.rglob("*.ipynb"))
    if not notebooks:
        print("No notebooks found", file=sys.stderr)
        return 1

    os.environ.update(
        {
            "NOTEBOOK_OFFLINE": "1",
            "LIVE_IEX_API": "0",
            "HERMES_NONINTERACTIVE": "1",
            "PORTFOLIO_SIZE": os.environ.get("PORTFOLIO_SIZE", "100000"),
            "PYTHONPATH": f"{project_root}{os.pathsep}" + os.environ.get("PYTHONPATH", ""),
        }
    )
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    failures: list[tuple[pathlib.Path, int, str]] = []
    for nb_path in notebooks:
        rel = nb_path.relative_to(project_root)
        print(f"Executing {rel} ...", flush=True)
        namespace: dict[str, object] = {"__name__": "__notebook__"}
        nb = nbformat.read(nb_path, as_version=4)
        try:
            with pushd(nb_path.parent):
                for index, cell in enumerate(nb.cells):
                    if cell.get("cell_type") != "code":
                        continue
                    source = _cell_source(cell)
                    if not source.strip():
                        continue
                    _assert_sanitized(source, rel, index)
                    exec(compile(source, str(rel) + f"#cell-{index}", "exec"), namespace)
        except Exception:
            failures.append((rel, index, traceback.format_exc(limit=8)))
            print(f"FAILED {rel} at cell {index}", file=sys.stderr)
        else:
            print(f"OK {rel}")
        finally:
            for output_name in GENERATED_OUTPUTS:
                output_path = nb_path.parent / output_name
                if output_path.exists():
                    output_path.unlink()

    if failures:
        print("\nOffline notebook validation failed:", file=sys.stderr)
        for rel, index, error in failures:
            print(f"- {rel} cell {index}:\n{error}", file=sys.stderr)
        return 1

    print(f"Executed {len(notebooks)} notebooks offline/non-interactively.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

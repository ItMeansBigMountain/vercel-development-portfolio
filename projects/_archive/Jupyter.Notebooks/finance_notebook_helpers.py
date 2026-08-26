"""Safe execution helpers for the finance notebooks.

The notebooks default to offline, fixture-backed, non-interactive execution so CI/local
validation does not hang on input prompts, call live APIs, or reveal secrets. Set
NOTEBOOK_OFFLINE=0 and LIVE_IEX_API=1 to opt into live IEX sandbox requests.
"""
from __future__ import annotations

import json
import os
import pathlib
import sys
from typing import Iterable, Mapping, Any

PROJECT_ROOT = pathlib.Path(__file__).resolve().parent
FIXTURE_PATH = PROJECT_ROOT / "fixtures" / "iex_batch_sample.json"
DEFAULT_PORTFOLIO_SIZE = "100000"
DEFAULT_OFFLINE_TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]


def load_dotenv_if_present(path: pathlib.Path | None = None) -> None:
    """Load key=value lines from .env without printing values or overriding env."""
    env_path = path or (PROJECT_ROOT / ".env")
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def get_iex_token() -> str | None:
    """Return an IEX token from the environment, if present, without logging it."""
    load_dotenv_if_present()
    return os.environ.get("IEX_CLOUD_API_TOKEN") or os.environ.get("IEX_API_TOKEN")


def is_offline_mode() -> bool:
    """Default to offline mode; require explicit opt-out for network execution."""
    return os.environ.get("NOTEBOOK_OFFLINE", "1").strip().lower() not in {"0", "false", "no"}


def patch_pandas_append(pd_module: Any) -> None:
    """Restore small legacy pandas APIs used by the notebooks."""
    if not hasattr(pd_module.DataFrame, "append"):
        def _append(self, other, ignore_index=False, **kwargs):
            if isinstance(other, pd_module.Series):
                other = other.to_frame().T
            elif isinstance(other, Mapping):
                other = pd_module.DataFrame([other])
            return pd_module.concat([self, other], ignore_index=ignore_index, **kwargs)

        pd_module.DataFrame.append = _append

    if not hasattr(pd_module.ExcelWriter, "save"):
        pd_module.ExcelWriter.save = lambda self: self.close()


def offline_tickers() -> list[str]:
    raw = os.environ.get("OFFLINE_TICKERS")
    if raw:
        return [item.strip().upper() for item in raw.split(",") if item.strip()]
    return DEFAULT_OFFLINE_TICKERS.copy()


def select_offline_stocks(stocks):
    """Limit stock CSVs to bundled fixture tickers while offline."""
    if not is_offline_mode():
        return stocks
    tickers = set(offline_tickers())
    selected = stocks[stocks["Ticker"].astype(str).str.upper().isin(tickers)].copy()
    if selected.empty:
        # Preserve notebook shape even if a CSV changes unexpectedly.
        return stocks.head(len(tickers)).copy()
    return selected.reset_index(drop=True)


def get_portfolio_size(prompt: str = "Please enter value of your portfollio: $") -> str:
    """Return a portfolio size from env/default in non-interactive mode, else prompt."""
    default = os.environ.get("PORTFOLIO_SIZE", DEFAULT_PORTFOLIO_SIZE)
    if os.environ.get("HERMES_NONINTERACTIVE", "").strip().lower() in {"1", "true", "yes"}:
        return default
    if not sys.stdin or not sys.stdin.isatty():
        return default
    return input(prompt)


def load_iex_fixture(path: pathlib.Path | None = None) -> dict[str, Any]:
    fixture_path = path or FIXTURE_PATH
    with fixture_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def iex_batch_data(symbols: str | Iterable[str], types: str = "quote,advanced-stats") -> dict[str, Any]:
    """Return IEX-style batch data from fixtures unless live API is explicitly enabled."""
    if isinstance(symbols, str):
        symbol_list = [item.strip().upper() for item in symbols.split(",") if item.strip()]
        symbols_for_url = symbols
    else:
        symbol_list = [str(item).strip().upper() for item in symbols if str(item).strip()]
        symbols_for_url = ",".join(symbol_list)

    if is_offline_mode() or os.environ.get("LIVE_IEX_API", "0") != "1":
        fixture = load_iex_fixture()
        return {symbol: fixture[symbol] for symbol in symbol_list if symbol in fixture}

    token = get_iex_token()
    if not token:
        raise RuntimeError("LIVE_IEX_API=1 requires IEX_CLOUD_API_TOKEN in environment or local .env")
    import requests

    url = (
        "https://sandbox.iexapis.com/stable/stock/market/batch"
        f"?symbols={symbols_for_url}&types={types}&token={token}"
    )
    return requests.get(url, timeout=30).json()

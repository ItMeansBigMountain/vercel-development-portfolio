from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = PROJECT_ROOT / ".env"

DEFAULTS = {
    "APP_ENV": "development",
    "APP_BASE_URL": "http://localhost:8765",
    "DATABASE_URL": "sqlite:///./local.db",
    "NEWS_API_KEY": "",
    "MARKET_DATA_PROVIDER": "sample",
    "SENTIMENT_PROVIDER": "baseline",
    "EMAIL_PROVIDER": "disabled",
    "EMAIL_FROM": "",
    "STRIPE_SECRET_KEY": "",
    "STRIPE_WEBHOOK_SECRET": "",
}


def load_env(path: Path = ENV_PATH) -> dict:
    """Load simple KEY=VALUE pairs from .env without external dependencies."""
    config = DEFAULTS.copy()
    if not path.exists():
        return config
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        config[key.strip()] = value.strip().strip('"').strip("'")
    return config

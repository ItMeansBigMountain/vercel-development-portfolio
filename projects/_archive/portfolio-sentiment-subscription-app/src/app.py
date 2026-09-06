import json
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse

from config import PROJECT_ROOT, load_env
from sentiment import build_dashboard_payload

CONFIG = load_env()
FRONTEND_DIR = PROJECT_ROOT / "frontend"
SAMPLE_DIR = PROJECT_ROOT / "sample-data"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(FRONTEND_DIR), **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/config":
            public_config = {
                "appEnv": CONFIG.get("APP_ENV", "development"),
                "marketDataProvider": CONFIG.get("MARKET_DATA_PROVIDER", "sample"),
                "sentimentProvider": CONFIG.get("SENTIMENT_PROVIDER", "baseline"),
                "emailProvider": CONFIG.get("EMAIL_PROVIDER", "disabled"),
            }
            return self.write_json(public_config)
        if parsed.path == "/api/dashboard":
            watchlist = read_json(SAMPLE_DIR / "watchlist.json")["tickers"]
            headlines = read_json(SAMPLE_DIR / "news.json")["headlines"]
            return self.write_json(build_dashboard_payload(watchlist, headlines))
        return super().do_GET()

    def write_json(self, payload):
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main():
    port = int(CONFIG.get("PORT", "8765") or "8765")
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"Portfolio Sentiment MVP running at http://127.0.0.1:{port}")
    print("Using local .env configuration and sample data mode.")
    server.serve_forever()


if __name__ == "__main__":
    main()

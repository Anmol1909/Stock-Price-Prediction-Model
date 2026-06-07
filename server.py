from __future__ import annotations

import json
import mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from prediction_engine import predict_stock


ROOT = Path(__file__).resolve().parent
FRONTEND = ROOT / "frontend"


class StockPredictionHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/health":
            self.send_json({"status": "ok"})
            return

        self.serve_static(path)

    def do_POST(self):
        if urlparse(self.path).path != "/api/predict":
            self.send_error(404, "Not found")
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length) or b"{}")
            result = predict_stock(
                ticker=payload.get("ticker", ""),
                start=payload.get("start", ""),
                end=payload.get("end", ""),
                days_ahead=payload.get("daysAhead", 10),
                model_key=payload.get("model", "linear"),
            )
            self.send_json(result)
        except Exception as exc:
            self.send_json({"error": str(exc)}, status=400)

    def serve_static(self, request_path: str):
        relative = "index.html" if request_path in ("", "/") else request_path.lstrip("/")
        file_path = (FRONTEND / relative).resolve()

        if not str(file_path).startswith(str(FRONTEND.resolve())) or not file_path.is_file():
            self.send_error(404, "Not found")
            return

        content_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
        body = file_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_json(self, payload: dict, status: int = 200):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        return


def main():
    server = ThreadingHTTPServer(("127.0.0.1", 8000), StockPredictionHandler)
    print("Stock Prediction app running at http://127.0.0.1:8000")
    server.serve_forever()


if __name__ == "__main__":
    main()

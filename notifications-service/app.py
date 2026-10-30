import json
from http.server import BaseHTTPRequestHandler, HTTPServer

SERVICE_NAME = "notifications"


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            status = 200
            body = {"service": SERVICE_NAME, "message": f"Hello from {SERVICE_NAME}!"}
        elif self.path == "/health":
            status = 200
            body = {"service": SERVICE_NAME, "status": "healthy"}
        else:
            status = 404
            body = {"error": "Not found"}

        payload = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


if __name__ == "__main__":
    print(f"{SERVICE_NAME} listening on port 8000", flush=True)
    HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()

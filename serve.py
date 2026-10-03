#!/usr/bin/env python3
"""Local preview that behaves like Cloudflare Workers Static Assets.

Serves public/ with clean URLs (/about -> about.html), applies _redirects,
and returns 404.html for missing pages. Usage: python3 serve.py [port]
"""
import http.server
import os
import sys

PUBLIC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8787


def load_redirects():
    rules = {}
    try:
        with open(os.path.join(PUBLIC, "_redirects")) as f:
            for line in f:
                parts = line.split()
                if len(parts) >= 2 and not parts[0].startswith("#"):
                    rules[parts[0]] = (parts[1], int(parts[2]) if len(parts) > 2 else 302)
    except FileNotFoundError:
        pass
    return rules


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PUBLIC, **kwargs)

    def redirect(self, location, code):
        self.send_response(code)
        self.send_header("Location", location)
        self.end_headers()

    def do_GET(self):
        path, _, query = self.path.partition("?")
        rules = load_redirects()
        if path in rules:
            return self.redirect(*rules[path])
        if path.endswith(".html"):
            clean = "/" if path == "/index.html" else path[: -len(".html")]
            return self.redirect(clean, 307)
        if path != "/" and path.endswith("/") and os.path.isfile(os.path.join(PUBLIC, path.strip("/") + ".html")):
            return self.redirect(path.rstrip("/"), 307)
        if path != "/" and not os.path.splitext(path)[1]:
            if os.path.isfile(os.path.join(PUBLIC, path.lstrip("/") + ".html")):
                self.path = path + ".html" + ("?" + query if query else "")
        target = os.path.join(PUBLIC, self.path.partition("?")[0].lstrip("/"))
        if path != "/" and not os.path.exists(target) or os.path.basename(path).startswith("_"):
            return self.not_found()
        return super().do_GET()

    def not_found(self):
        with open(os.path.join(PUBLIC, "404.html"), "rb") as f:
            body = f.read()
        self.send_response(404)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    print(f"Previewing at http://localhost:{PORT}")
    http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()

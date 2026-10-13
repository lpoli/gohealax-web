#!/usr/bin/env python3
"""Uncached local preview; LAN mode serves only deployable website files."""
from argparse import ArgumentParser
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

WEB = Path(__file__).resolve().parents[1]


class PreviewHandler(SimpleHTTPRequestHandler):
    fallback_404 = False

    def send_error(self, code, message=None, explain=None):
        if code == 404 and self.fallback_404:
            body = (Path(self.directory) / "404.html").read_bytes()
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(body)
            return
        super().send_error(code, message, explain)

    def send_head(self):
        # Older cached responses can carry validators. Preview always returns current bytes.
        for name in ('If-Modified-Since', 'If-None-Match'):
            if name in self.headers:
                del self.headers[name]
        return super().send_head()

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, max-age=0')
        super().end_headers()


def preview_settings(lan=False, root=False):
    if root:
        return "127.0.0.1", WEB / "site"
    return ('0.0.0.0', WEB / 'site') if lan else ('127.0.0.1', WEB)


def main():
    parser = ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('--lan', action='store_true', help='Allow phone access; serve only web/site at /')
    modes.add_argument('--root', action='store_true', help='Serve website at origin root with custom nested 404 responses')
    parser.add_argument('--port', type=int, default=8765)
    args = parser.parse_args()
    bind, directory = preview_settings(args.lan, args.root)
    PreviewHandler.fallback_404 = args.root or args.lan
    handler = partial(PreviewHandler, directory=str(directory))
    with ThreadingHTTPServer((bind, args.port), handler) as server:
        if args.lan:
            print(f'Phone preview: http://<computer-Wi-Fi-IP>:{server.server_port}/', flush=True)
            print('Website files only. Stop with Ctrl+C.', flush=True)
        elif args.root:
            print(f'Website and nested 404: http://127.0.0.1:{server.server_port}/', flush=True)
        else:
            print(f'Website: http://127.0.0.1:{server.server_port}/site/', flush=True)
            print(f'Tests: http://127.0.0.1:{server.server_port}/tests/browser.html', flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Uncached local preview; LAN mode serves only deployable website files."""
from argparse import ArgumentParser
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

WEB = Path(__file__).resolve().parents[1]


class PreviewHandler(SimpleHTTPRequestHandler):
    def send_head(self):
        # Older cached responses can carry validators. Preview always returns current bytes.
        for name in ('If-Modified-Since', 'If-None-Match'):
            if name in self.headers:
                del self.headers[name]
        return super().send_head()

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, max-age=0')
        super().end_headers()


def preview_settings(lan=False):
    return ('0.0.0.0', WEB / 'site') if lan else ('127.0.0.1', WEB)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--lan', action='store_true', help='Allow phone access; serve only web/site at /')
    parser.add_argument('--port', type=int, default=8765)
    args = parser.parse_args()
    bind, directory = preview_settings(args.lan)
    handler = partial(PreviewHandler, directory=str(directory))
    with ThreadingHTTPServer((bind, args.port), handler) as server:
        if args.lan:
            print(f'Phone preview: http://<computer-Wi-Fi-IP>:{server.server_port}/', flush=True)
            print('Website files only. Stop with Ctrl+C.', flush=True)
        else:
            print(f'Website: http://127.0.0.1:{server.server_port}/site/', flush=True)
            print(f'Tests: http://127.0.0.1:{server.server_port}/tests/browser.html', flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    main()

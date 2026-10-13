"""Exercise real HTTP responses without opening sockets or writing outside the repo."""
from io import BytesIO
from types import SimpleNamespace
import importlib.util
import unittest

from site_checks import WEB

spec = importlib.util.spec_from_file_location('web_preview', WEB / 'tools/preview.py')
preview = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preview)


class Connection:
    def __init__(self, request):
        self.request = BytesIO(request)
        self.response = bytearray()

    def makefile(self, *_args):
        return self.request

    def sendall(self, data):
        self.response.extend(data)


class QuietHandler(preview.PreviewHandler):
    def log_message(self, *_args):
        pass


def request(path, directory, headers=''):
    connection = Connection(f'GET {path} HTTP/1.1\r\nHost: localhost\r\n{headers}\r\n'.encode())
    QuietHandler(connection, ('127.0.0.1', 12345), SimpleNamespace(), directory=str(directory))
    return bytes(connection.response)


class PreviewTests(unittest.TestCase):
    def test_local_preview_serves_current_html_and_css_without_caching(self):
        bind, root = preview.preview_settings()
        self.assertEqual('127.0.0.1', bind)
        for path, content in (('/site/index.html', b'class="landing"'),
                              ('/site/site.css', b'.landing .hero-photo img')):
            response = request(path, root, 'If-Modified-Since: Thu, 31 Dec 2099 23:59:59 GMT\r\n')
            self.assertTrue(response.startswith(b'HTTP/1.0 200'))
            self.assertIn(b'Cache-Control: no-store, max-age=0', response)
            self.assertIn(content, response)
        self.assertIn(b'Content-type: text/css', request('/site/site.css', root))

    def test_phone_mode_exposes_only_the_deployable_website(self):
        bind, root = preview.preview_settings(lan=True)
        self.assertEqual('0.0.0.0', bind)
        self.assertEqual(WEB / 'site', root)
        self.assertIn(b'HTTP/1.0 200', request('/', root))
        self.assertIn(b'HTTP/1.0 200', request('/site.css', root))
        for path in ('/tests/browser.html', '/docs/handoff.md', '/../PROJECT.md'):
            self.assertIn(b'HTTP/1.0 404', request(path, root))


class Nested404Tests(unittest.TestCase):
    def test_unknown_nested_url_returns_actual_404_document_and_status(self):
        bind, root = preview.preview_settings(root=True)
        self.assertEqual('127.0.0.1', bind)
        QuietHandler.fallback_404 = True
        try:
            response = request('/unknown/nested/page', root)
            self.assertTrue(response.startswith(b'HTTP/1.0 404'))
            self.assertEqual((root / '404.html').read_bytes(), response.split(b'\r\n\r\n', 1)[1])
            self.assertIn(b'Cache-Control: no-store', response)
            for path in ('/site.css', '/About.html', '/assets/favicon.svg'):
                self.assertTrue(request(path, root).startswith(b'HTTP/1.0 200'))
        finally:
            QuietHandler.fallback_404 = False

"""Release safety tests; temporary packages never leave the repository."""
import importlib.util
import hashlib
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from site_checks import SITE, WEB
from test_preview import QuietHandler, request, preview

spec = importlib.util.spec_from_file_location('release', WEB / 'scripts/prepare-release.py')
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)

spec = importlib.util.spec_from_file_location('approval', WEB / 'scripts/verify-approved-release.py')
approval = importlib.util.module_from_spec(spec)
spec.loader.exec_module(approval)


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        (WEB / '.artifacts').mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix='release-test-', dir=WEB / '.artifacts')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'source'
        shutil.copytree(SITE, self.source)
        self.output = self.root / 'output'

    def install(self, **kwargs):
        return release.install(self.source, self.output, self.root / 'transactions', **kwargs)

    def snapshot(self):
        return {p.relative_to(self.output).as_posix(): p.read_bytes()
                for p in self.output.rglob('*') if p.is_file()}

    def test_approval_rejects_wrong_hash_invalid_input_and_changed_site(self):
        data = self.install()
        expected = hashlib.sha256(data).hexdigest()
        approval.verify(expected, self.output)
        with self.assertRaisesRegex(ValueError, 'differs from the approved'):
            approval.verify('0' * 64, self.output)
        for invalid in ('', expected.upper(), '$(echo unsafe)', expected + '\n'):
            with self.subTest(invalid=invalid), self.assertRaisesRegex(ValueError, '64 lowercase'):
                approval.verify(invalid, self.output)
        with (self.output / 'site/site.css').open('a') as stream:
            stream.write('\n/* altered after export */\n')
        with self.assertRaisesRegex(ValueError, 'site differs from its manifest'):
            approval.verify(expected, self.output)

    def test_byte_identical_deterministic_export_and_exact_exclusions(self):
        first = self.install()
        before = self.snapshot()
        self.assertEqual(release.ALLOWLIST, {p.relative_to(self.output / 'site').as_posix()
                         for p in (self.output / 'site').rglob('*') if p.is_file()})
        for name in release.ALLOWLIST:
            self.assertEqual((SITE / name).read_bytes(), (self.output / 'site' / name).read_bytes())
        self.assertEqual(first, self.install())
        self.assertEqual(before, self.snapshot())
        self.assertNotIn('manifest.json', release.ALLOWLIST)
        for name in ('PROJECT.md', 'tests/test_site.py', 'image-ref/photo.png', '.git/config',
                     '.env', 'android/app.apk', 'assets/unknown.png'):
            with self.subTest(name=name):
                path = self.source / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('excluded')
                with self.assertRaises(ValueError): self.install()
                path.unlink()
                # Remove newly created empty directories, preserving approved directories.
                parent = path.parent
                while parent != self.source and parent.relative_to(self.source).as_posix() not in release.DIRECTORIES:
                    parent.rmdir(); parent = parent.parent
                self.assertEqual(before, self.snapshot())

    def test_bad_references_preserve_previous_output(self):
        self.install()
        before = self.snapshot()
        page = self.source / 'index.html'
        original = page.read_text()
        for url in ('missing.png', '../PROJECT.md', '%2e%2e/PROJECT.md', 'About.html#absent'):
            with self.subTest(url=url):
                page.write_text(original.replace('</main>', f'<a href="{url}">bad</a></main>'))
                with self.assertRaises(ValueError): self.install()
                self.assertEqual(before, self.snapshot())
        page.write_text(original)
        (self.source / 'site.js').write_text('import "../private.js";')
        with self.assertRaises(ValueError): self.install()

    def test_symlinks_missing_files_and_domain_config_rejected(self):
        for name in ('assets', 'site.js'):
            source = self.source / name
            moved = self.root / name
            source.rename(moved)
            source.symlink_to(moved, target_is_directory=moved.is_dir())
            with self.assertRaises(ValueError): self.install()
            source.unlink(); moved.rename(source)
        linked = self.root / 'linked'
        linked.symlink_to(self.source, target_is_directory=True)
        with self.assertRaises(ValueError): release.validate(linked)
        (self.source / '.nojekyll').write_text('unexpected')
        with self.assertRaises(ValueError): self.install()
        (self.source / '.nojekyll').write_bytes(b'')
        (self.source / 'CNAME').write_text('other.example\n')
        with self.assertRaises(ValueError): self.install()
        (self.source / 'CNAME').unlink()
        with self.assertRaises(ValueError): self.install()

    def test_staging_and_replacement_failures_preserve_previous_package(self):
        self.install()
        before = self.snapshot()
        with patch.object(release.shutil, 'copytree', side_effect=OSError('copy failure')):
            with self.assertRaises(OSError): self.install()
        self.assertEqual(before, self.snapshot())
        rename = Path.rename
        def fail_next(path, target):
            if path.name == 'next': raise OSError('replace failure')
            return rename(path, target)
        with patch.object(Path, 'rename', fail_next):
            with self.assertRaises(OSError): self.install()
        self.assertEqual(before, self.snapshot())

    def test_changed_source_during_staging_preserves_previous_package(self):
        self.install()
        before = self.snapshot()
        copy = shutil.copytree
        def mutate_after_copy(source, destination, *args, **kwargs):
            result = copy(source, destination, *args, **kwargs)
            page = Path(destination) / 'index.html'
            if page.is_file():
                page.write_text(page.read_text().replace('</main>', '<p>Changed bytes</p></main>'))
            return result
        with patch.object(release.shutil, 'copytree', mutate_after_copy):
            with self.assertRaises(ValueError): self.install()
        self.assertEqual(before, self.snapshot())

    def test_unexpected_empty_directories_and_linked_output_rejected(self):
        (self.source / 'private').mkdir()
        with self.assertRaises(ValueError): self.install()
        (self.source / 'private').rmdir()
        self.output.symlink_to(self.source, target_is_directory=True)
        with self.assertRaises(ValueError): self.install()
        self.assertTrue(self.output.is_symlink())

    def test_stale_files_removed_and_local_content_rollback(self):
        self.install()
        saved = self.root / 'saved'
        shutil.copytree(self.output, saved)
        before = self.snapshot()
        (self.output / 'site/stale.txt').write_text('stale')
        page = self.source / 'index.html'
        page.write_text(page.read_text().replace('</main>', '<p>Local rollback test</p></main>'))
        self.install()
        self.assertFalse((self.output / 'site/stale.txt').exists())
        self.assertNotEqual(before, self.snapshot())
        release.install(saved / 'site', self.output, self.root / 'transactions',
                        expected=(saved / 'manifest.json').read_bytes())
        self.assertEqual(before, self.snapshot())
        with self.assertRaises(ValueError):
            release.install(saved / 'site', self.output, self.root / 'transactions', expected=b'bad')
        self.assertEqual(before, self.snapshot())

    def test_exported_root_routes_and_actual_nested_404(self):
        self.install()
        bind, fixed = preview.preview_settings(exported=True)
        self.assertEqual('127.0.0.1', bind)
        self.assertEqual(WEB / '.release/site', fixed)
        root = self.output / 'site'
        QuietHandler.fallback_404 = True
        try:
            for route in ('/', '/About.html', '/privacy-policy.html', '/medical-disclaimer.html',
                          '/404.html', '/site.css', '/site.js', '/assets/favicon.svg'):
                with self.subTest(route=route):
                    self.assertTrue(request(route, root).startswith(b'HTTP/1.0 200'))
            response = request('/unknown/nested/page', root)
            self.assertTrue(response.startswith(b'HTTP/1.0 404'))
            self.assertEqual((root / '404.html').read_bytes(), response.split(b'\r\n\r\n', 1)[1])
        finally:
            QuietHandler.fallback_404 = False

    def test_check_is_validation_only(self):
        before = {p: p.read_bytes() for p in release.OUTPUT.rglob('*') if p.is_file()}
        result = subprocess.run([sys.executable, str(WEB / 'scripts/prepare-release.py'), '--check'],
                                capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(before, {p: p.read_bytes() for p in release.OUTPUT.rglob('*') if p.is_file()})

    def test_restore_paths_cannot_escape_or_follow_symlinks(self):
        for path in (WEB / 'site', WEB / '.artifacts/../site'):
            with self.assertRaises(ValueError): release.saved_package(str(path))
        self.install()
        saved = self.root / 'saved'
        shutil.copytree(self.output, saved)
        self.assertEqual(saved, release.saved_package(str(saved)))
        saved.rename(self.root / 'real')
        saved.symlink_to(self.root / 'real', target_is_directory=True)
        with self.assertRaises(ValueError): release.saved_package(str(saved))

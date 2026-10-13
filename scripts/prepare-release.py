#!/usr/bin/env python3
"""Validate and export the exact reviewed static site, or restore a saved package."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile

WEB = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(WEB / 'tests'))
from site_checks import local_target, read_document, reference_issues
from quality_checks import quality_issues

ALLOWLIST = frozenset('''index.html About.html privacy-policy.html medical-disclaimer.html
404.html site.css site.js media.js robots.txt sitemap.xml CNAME .nojekyll
assets/project-logo.png assets/favicon.svg assets/favicon.png assets/apple-touch-icon.png assets/social.png
assets/hero-480.webp assets/hero-800.webp assets/hero-1200.webp
assets/screenshots/running-timer-1.png assets/screenshots/preset.png
assets/screenshots/todays-exercises.png assets/screenshots/statistics.png'''.split())
DIRECTORIES = frozenset({'assets', 'assets/screenshots'})
OUTPUT = WEB / '.release'
ARTIFACTS = WEB / '.artifacts'


def regular_tree(root, saved=False):
    if root.is_symlink() or not root.is_dir():
        raise ValueError(f'not a regular directory: {root}')
    files = set()
    for path in root.rglob('*'):
        name = path.relative_to(root).as_posix()
        if path.is_symlink():
            raise ValueError(f'symlink forbidden: {name}')
        if path.is_dir():
            if name not in DIRECTORIES:
                raise ValueError(f'unexpected directory: {name}')
        elif path.is_file():
            files.add(name)
        else:
            raise ValueError(f'non-regular file: {name}')
    expected = ALLOWLIST
    # Previously retained WEB-06 packages predate the owner-selected logo.
    if saved and 'assets/project-logo.png' not in files:
        expected = ALLOWLIST - {'assets/project-logo.png'}
    if files != expected:
        raise ValueError(f'file allowlist mismatch; unexpected={sorted(files - expected)}, missing={sorted(expected - files)}')


def validate(root, saved=False):
    regular_tree(root, saved=saved)
    if (root / 'CNAME').read_bytes() != b'gohealax.com\n':
        raise ValueError('CNAME must contain only gohealax.com and newline')
    if (root / '.nojekyll').read_bytes():
        raise ValueError('.nojekyll must be empty')
    issues = quality_issues(root)
    for name in sorted(ALLOWLIST):
        path = root / name
        if path.suffix == '.html':
            doc = read_document(path)
            issues.extend(reference_issues(root, path, doc))
            for node in doc.root.walk():
                for attr in ('data-media-poster', 'data-media-src', 'data-media-captions-src'):
                    if node.attrs.get(attr):
                        target = local_target(root, path, node.attrs[attr])
                        if target is None or not target[0].is_file():
                            issues.append(f'{name}: invalid {attr}')
        elif path.suffix == '.js':
            # Current modules have no imports. Validate literal module specifiers if added.
            code = path.read_text()
            for url in re.findall(r'''(?:\bfrom\s*|\bimport\s*\(?\s*)["']([^"']+)["']''', code):
                target = local_target(root, path, url)
                if target is None or not target[0].is_file():
                    issues.append(f'{name}: invalid module import {url}')
    if issues:
        raise ValueError('\n'.join(issues))
    return manifest(root)


def manifest(root):
    entries = []
    for name in sorted(ALLOWLIST):
        if not (root / name).is_file():
            continue
        data = (root / name).read_bytes()
        entries.append({'path': name, 'size': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
    return (json.dumps({'files': entries}, indent=2, sort_keys=True) + '\n').encode()


def install(source, output=OUTPUT, artifacts=ARTIFACTS, expected=None):
    """Stage bytes and revalidate before replacing site and manifest as one unit.

    Rename errors roll back the prior directory. A process/power failure between renames may
    leave the prior package at transaction/previous; it is deliberately never auto-deleted.
    """
    initial = validate(source, saved=expected is not None)
    if expected is not None and initial != expected:
        raise ValueError('saved manifest differs from package bytes')
    if output.is_symlink() or (output.exists() and not output.is_dir()):
        raise ValueError('output must be a regular directory')
    if artifacts.is_symlink():
        raise ValueError('artifact directory must not be a symlink')
    artifacts.mkdir(parents=True, exist_ok=True)
    transaction = Path(tempfile.mkdtemp(prefix='release-', dir=artifacts))
    staged, previous = transaction / 'next', transaction / 'previous'
    moved = False
    try:
        shutil.copytree(source, staged / 'site', symlinks=True)
        if validate(staged / 'site', saved=expected is not None) != initial:
            raise ValueError('source changed during export')
        (staged / 'manifest.json').write_bytes(initial)
        if output.exists():
            output.rename(previous)
            moved = True
        try:
            staged.rename(output)
        except BaseException:
            if moved:
                previous.rename(output)
            raise
    finally:
        # Preserve the recovery package if rollback itself failed.
        if not previous.exists() or output.exists():
            shutil.rmtree(transaction)
    return initial


def saved_package(value):
    path = Path(value).absolute()
    if not path.is_relative_to(ARTIFACTS):
        raise ValueError('saved packages must be inside web/.artifacts/')
    for ancestor in (path, *path.parents):
        if ancestor.is_symlink():
            raise ValueError('saved package path contains a symlink')
    path = path.resolve()
    if not path.is_relative_to(ARTIFACTS.resolve()):
        raise ValueError('saved package escapes artifact directory')
    if {p.name for p in path.iterdir()} != {'site', 'manifest.json'}:
        raise ValueError('saved package must contain exactly site and manifest.json')
    if (path / 'manifest.json').is_symlink():
        raise ValueError('manifest symlink forbidden')
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Validate only; write nothing')
    parser.add_argument('--restore', metavar='PACKAGE', help='Restore saved site/manifest under web/.artifacts/')
    args = parser.parse_args()
    try:
        source, expected = WEB / 'site', None
        if args.restore:
            package = saved_package(args.restore)
            source, expected = package / 'site', (package / 'manifest.json').read_bytes()
        result = validate(source, saved=expected is not None)
        if expected is not None and result != expected:
            raise ValueError('saved manifest differs from package bytes')
        if not args.check:
            install(source, expected=expected)
        print(f'{"Validated" if args.check else "Exported"} {len(json.loads(result)["files"])} files; manifest SHA-256 {hashlib.sha256(result).hexdigest()}')
    except (OSError, ValueError) as error:
        print(f'Release failed: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())

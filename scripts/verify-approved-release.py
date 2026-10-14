#!/usr/bin/env python3
"""Reject an export unless its manifest and site match the owner's approved hash."""
import argparse
import hashlib
import importlib.util
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('release', Path(__file__).with_name('prepare-release.py'))
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)


def verify(expected, package=release.OUTPUT):
    if not re.fullmatch(r'[0-9a-f]{64}', expected):
        raise ValueError('approved manifest SHA-256 must be 64 lowercase hexadecimal characters')
    data = (package / 'manifest.json').read_bytes()
    if hashlib.sha256(data).hexdigest() != expected:
        raise ValueError('export manifest differs from the approved SHA-256')
    if release.validate(package / 'site', saved=True) != data:
        raise ValueError('export site differs from its manifest')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest-sha256', required=True)
    args = parser.parse_args()
    try:
        verify(args.manifest_sha256)
    except (ValueError, OSError) as error:
        parser.exit(1, f'FAIL: {error}\n')
    print(f'PASS: approved export {args.manifest_sha256}')


if __name__ == '__main__':
    main()

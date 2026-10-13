#!/usr/bin/env python3
"""Mandatory static quality gate; manual accessibility/rights/hosting remain separate."""
from quality_checks import quality_issues


def audit():
    return quality_issues()


if __name__ == '__main__':
    findings = audit()
    for finding in findings:
        print(f'GAP: {finding}')
    print(f'{len(findings)} target-quality gap(s). Content truth/rights/hosting require separate review.')
    raise SystemExit(bool(findings))

#!/usr/bin/env python3
"""Report implemented target checks; exit 1 for gaps. Not a complete accessibility audit."""

from site_checks import (SITE, metadata_issues, read_document, reference_issues,
                         required_disclaimer, structure_issues)


def audit():
    findings = []
    canonicals = {
        "index.html": "https://gohealax.com/",
        "About.html": "https://gohealax.com/About.html",
        "privacy-policy.html": "https://gohealax.com/privacy-policy.html",
        "medical-disclaimer.html": "https://gohealax.com/medical-disclaimer.html",
    }
    for route, canonical in canonicals.items():
        path = SITE / route
        if not path.is_file():
            findings.append(f"{route}: required page missing")
            continue
        document = read_document(path)
        issues = (structure_issues(document) + reference_issues(SITE, path, document)
                  + metadata_issues(document, canonical))
        if route != "index.html" and required_disclaimer() not in document.root.text:
            issues.append("exact PROD-01 disclaimer missing")
        if any(n.attrs.get("http-equiv", "").lower() == "refresh" for n in document.find("meta")):
            issues.append("replace redirect with landing page")
        for node in document.find("img"):
            if not all(node.attrs.get(key, "").isdigit() and int(node.attrs[key]) > 0
                       for key in ("width", "height")):
                issues.append(f"image dimensions missing: {node.attrs.get('src', '(no src)')}")
            if "alt" not in node.attrs:
                issues.append("image alt attribute missing")
        findings.extend(f"{route}: {issue}" for issue in issues)
    for route in ("404.html", "sitemap.xml", "robots.txt"):
        if not (SITE / route).is_file():
            findings.append(f"{route}: required quality file missing (WEB-05)")
    return findings


if __name__ == "__main__":
    findings = audit()
    for finding in findings:
        print(f"GAP: {finding}")
    print(f"{len(findings)} target-quality gap(s). Content truth/rights/hosting require separate review.")
    raise SystemExit(bool(findings))

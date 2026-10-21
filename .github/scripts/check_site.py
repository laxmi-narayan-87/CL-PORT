from pathlib import Path
from html.parser import HTMLParser
import re
import sys

page = Path("index.html")
if not page.is_file():
    sys.exit("FAIL: index.html is missing")

html = page.read_text(encoding="utf-8")

class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.fragments = []
        self.unsafe_new_tab_links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        href = attrs.get("href", "")
        if tag == "a" and href.startswith("#") and len(href) > 1:
            self.fragments.append(href[1:])
        if tag == "a" and attrs.get("target") == "_blank":
            rel = set(attrs.get("rel", "").lower().split())
            if not {"noopener", "noreferrer"}.issubset(rel):
                self.unsafe_new_tab_links.append(href)

parser = SiteParser()
parser.feed(html)
checks = {
    "HTML5 doctype": html.lstrip().lower().startswith("<!doctype html>"),
    "language attribute": '<html lang="en">' in html,
    "responsive viewport": 'name="viewport"' in html,
    "description metadata": 'name="description"' in html,
    "CSP meta policy": 'http-equiv="Content-Security-Policy"' in html,
    "scripts disabled by default": "script-src 'none'" in html,
    "objects disabled": "object-src 'none'" in html,
    "no legacy local Windows paths": not re.search(r"[A-Za-z]:\\Users\\", html),
    "no placeholder lorem ipsum": "lorem ipsum" not in html.lower(),
    "main landmark": '<main id="main">' in html,
    "all in-page links have targets": all(fragment in parser.ids for fragment in parser.fragments),
    "new-tab links use safe rel values": not parser.unsafe_new_tab_links,
    "skills are reachable from navigation": 'href="#skills">Skills</a>' in html,
    "no draft instructions remain": not any(phrase in html.lower() for phrase in ("add a verified demo", "evidence to publish", "use this section for")),
    "skip link": 'class="skip" href="#main"' in html,
    "reduced-motion support": "prefers-reduced-motion:reduce" in html,
    "quality/security section": 'id="quality"' in html,
    "contact email link": 'href="mailto:laxminarayan955459@gmail.com"' in html,
}

# Keep the testing copy out of the public GitHub Pages artifact.
pages_workflow = Path(".github/workflows/deploy-pages.yml")
quality_workflow = Path(".github/workflows/quality.yml")
staging_checker = Path("staging-portfolio/.github/scripts/check_site.py")
if pages_workflow.is_file():
    pages_text = pages_workflow.read_text(encoding="utf-8")
    checks["GitHub Pages artifact is isolated from staging"] = (
        "staging-portfolio" in pages_text and "path: _site" in pages_text
    )
else:
    checks["GitHub Pages deployment workflow exists"] = False
if quality_workflow.is_file():
    quality_text = quality_workflow.read_text(encoding="utf-8")
    checks["main quality workflow runs staging guard"] = (
        "staging-portfolio/.github/scripts/check_site.py" in quality_text
    )
else:
    checks["quality workflow exists"] = False
checks["staging SEO guard exists"] = staging_checker.is_file()
checks["public root page does not link to staging path"] = "/staging-portfolio/" not in html

failed = [name for name, passed in checks.items() if not passed]
for name, passed in checks.items():
    print(f'{"PASS" if passed else "FAIL"}: {name}')
if failed:
    sys.exit(f"{len(failed)} check(s) failed: {', '.join(failed)}")

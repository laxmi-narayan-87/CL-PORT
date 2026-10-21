from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
BASE_URL = "https://cl-port-staging-portfolio.vercel.app/"
HOME = ROOT / "index.html"
SITEMAP = ROOT / "sitemap.xml"
GOOGLE_VERIFICATION = ROOT / "google962efd04cf37010b.html"
VERCEL_CONFIG = ROOT / "vercel.json"

required_pages = [
    "projects/darksense-ai/index.html",
    "projects/skillforge-academy/index.html",
    "projects/agrovalue/index.html",
    "projects/q-learning-frozenlake/index.html",
    "projects/qa-automation/index.html",
]

if not HOME.is_file():
    sys.exit("FAIL: index.html is missing")

html = HOME.read_text(encoding="utf-8")
checks = {
    "HTML5 doctype": html.lstrip().lower().startswith("<!doctype html>"),
    "language attribute": '<html lang="en">' in html,
    "responsive viewport": 'name="viewport"' in html,
    "page title": bool(re.search(r"<title>[^<]{10,}</title>", html, re.I)),
    "description metadata": bool(re.search(r'<meta name="description" content="[^"]{40,}"', html)),
    "homepage has noindex, follow": 'name="robots" content="noindex, follow"' in html,
    "staging has no canonical": not re.search(r'<link\s+rel="canonical"\b', html, re.I),
    "homepage Open Graph URL is the Vercel staging URL": f'property="og:url" content="{BASE_URL}"' in html,
    "homepage structured-data URL is the Vercel staging URL": f'"url": "{BASE_URL}"' in html,
    "no old GitHub Pages staging URL": "laxmi-narayan-87.github.io/CL-PORT/staging-portfolio/" not in html,
    "CSP meta policy": 'http-equiv="Content-Security-Policy"' in html,
    "scripts disabled by default": "script-src 'none'" in html,
    "objects disabled": "object-src 'none'" in html,
    "no legacy local Windows paths": not re.search(r"[A-Za-z]:\\Users\\", html),
    "no lorem ipsum placeholder": "lorem ipsum" not in html.lower(),
    "main landmark": '<main id="main">' in html,
    "skip link": 'class="skip" href="#main"' in html,
    "reduced-motion support": "prefers-reduced-motion:reduce" in html,
    "quality/security section": 'id="quality"' in html,
    "contact email link": 'href="mailto:laxminarayan955459@gmail.com"' in html,
    "DarkSense links to its actual source": 'href="https://github.com/laxmi-narayan-87/CL-PORT/tree/main/darksense"' in html,
    "LeetCode generic homepage link removed": 'href="https://leetcode.com/"' not in html,
    "staging sitemap removed": not SITEMAP.exists(),
    "copied Search Console verification removed": not GOOGLE_VERIFICATION.exists(),
}

placeholder_phrases = (
    "Evidence to publish",
    "Evidence to explore",
    "Add individual certificates and verified outcomes",
    "Use this section for verified achievements",
    "Link to a public profile and keep counts current",
)
for phrase in placeholder_phrases:
    checks[f"no editorial placeholder: {phrase}"] = phrase.lower() not in html.lower()

for page in required_pages:
    checks[f"case study exists: {page}"] = (ROOT / page).is_file()

# Every staged HTML page must remain excluded from search results and use the staging host only.
page_paths = ["index.html", *required_pages]
for page in page_paths:
    path = ROOT / page
    if not path.is_file():
        continue
    page_html = path.read_text(encoding="utf-8")
    expected_url = BASE_URL if page == "index.html" else BASE_URL + page.removesuffix("/index.html") + "/"
    relative = page
    robots = re.findall(r'<meta\s+name="robots"\s+content="([^"]+)"', page_html, re.I)
    og_url = re.search(r'<meta\s+property="og:url"\s+content="([^"]+)"', page_html, re.I)
    checks[f"exactly one noindex, follow directive: {relative}"] = robots == ["noindex, follow"]
    checks[f"no canonical tag: {relative}"] = not re.search(r'<link\s+rel="canonical"\b', page_html, re.I)
    checks[f"Open Graph URL uses staging host: {relative}"] = bool(og_url and og_url.group(1) == expected_url)
    checks[f"no legacy GitHub Pages staging URL: {relative}"] = "laxmi-narayan-87.github.io/CL-PORT/staging-portfolio/" not in page_html

try:
    config = json.loads(VERCEL_CONFIG.read_text(encoding="utf-8"))
    header_rules = config.get("headers", [])
    headers = {}
    for rule in header_rules:
        if rule.get("source") == "/(.*)":
            headers.update({
                item.get("key", "").lower(): item.get("value", "")
                for item in rule.get("headers", [])
            })
    checks["Vercel response header blocks indexing"] = headers.get("x-robots-tag") == "noindex, follow"
    checks["X-Content-Type-Options enabled"] = headers.get("x-content-type-options") == "nosniff"
    checks["X-Frame-Options prevents framing"] = headers.get("x-frame-options") == "DENY"
    checks["Referrer-Policy configured"] = headers.get("referrer-policy") == "strict-origin-when-cross-origin"
    checks["Permissions-Policy limits sensitive browser APIs"] = headers.get("permissions-policy") == "camera=(), microphone=(), geolocation=()"
except (OSError, json.JSONDecodeError, TypeError) as exc:
    checks["Vercel headers config is valid JSON"] = False
    print(f"Could not parse vercel.json: {exc}")

failed = [name for name, passed in checks.items() if not passed]
for name, passed in checks.items():
    print(f'{"PASS" if passed else "FAIL"}: {name}')
if failed:
    sys.exit(f"{len(failed)} check(s) failed: {', '.join(failed)}")

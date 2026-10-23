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
CERTIFICATION_DATA = ROOT / "data" / "certifications.json"
PROJECT_DATA = ROOT / "data" / "project-claims.json"
CERTIFICATION_SCRIPT = ROOT / "assets" / "certifications.js"
BASE_CSS = ROOT / "assets" / "base.css"
HOME_CSS = ROOT / "assets" / "home.css"

required_pages = [
    "projects/darksense-ai/index.html",
    "projects/skillforge-academy/index.html",
    "projects/agrovalue/index.html",
    "projects/q-learning-frozenlake/index.html",
    "projects/qa-automation/index.html",
    "certifications/index.html",
    "resume/index.html",
    "resume/software-development/index.html",
    "resume/qa-testing/index.html",
    "resume/ai-ml-data/index.html",
]

if not HOME.is_file():
    sys.exit("FAIL: index.html is missing")

html = HOME.read_text(encoding="utf-8")
base_css = BASE_CSS.read_text(encoding="utf-8") if BASE_CSS.is_file() else ""
home_css = HOME_CSS.read_text(encoding="utf-8") if HOME_CSS.is_file() else ""
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
    "homepage links shared and page-specific styles": '<link rel="stylesheet" href="/assets/base.css">' in html and '<link rel="stylesheet" href="/assets/home.css">' in html,
    "homepage has no inline CSS": "<style" not in html and " style=" not in html,
    "homepage CSP restricts styles to same-origin": "style-src 'self'" in html and "style-src 'self' 'unsafe-inline'" not in html,
    "shared stylesheets exist": BASE_CSS.is_file() and HOME_CSS.is_file() and bool(base_css) and bool(home_css),
    "reduced-motion support": "prefers-reduced-motion: reduce" in base_css,
    "profiles section exists": 'id="profiles"' in html,
    "profiles nav link exists": 'href="#profiles">Profiles</a>' in html,
    "GitHub profile link exists": 'href="https://github.com/laxmi-narayan-87" target="_blank"' in html,
    "verified LinkedIn profile is consistent": html.count('https://www.linkedin.com/in/laxminarayan87') >= 3,
    "LeetCode profile link exists": 'href="https://leetcode.com/u/Laxmi_Narayan_87/"' in html,
    "LeetCode solutions archive link exists": 'href="https://github.com/laxmi-narayan-87/DSA/tree/main/leetcode"' in html,
    "CodeChef profile link exists": 'href="https://www.codechef.com/users/laxminarayan87"' in html,
    "CodeChef solutions archive link exists": 'href="https://github.com/laxmi-narayan-87/DSA/tree/main/solutions/platforms/codechef"' in html,
    "HackerRank profile link exists": 'href="https://www.hackerrank.com/profile/laxmi_narayan_87"' in html,
    "HackerRank solutions archive link exists": 'href="https://github.com/laxmi-narayan-87/DSA/tree/main/solutions/platforms/hackerrank"' in html,
    "GeeksforGeeks profile link exists": 'href="https://www.geeksforgeeks.org/profile/laxmi_narayan_87"' in html,
    "GeeksforGeeks solutions archive link exists": 'href="https://github.com/laxmi-narayan-87/DSA/tree/main/solutions/platforms/geeksforgeeks"' in html,
    "profile grid styles exist": ".profile-grid" in home_css and ".profile-card" in home_css,
    "education timeline still has three entries": html.count('class="education-item"') == 3,
    "quality/security section": 'id="quality"' in html,
    "contact email link": 'href="mailto:laxminarayan955459@gmail.com"' in html,
    "DarkSense link is labelled as a public interface preview": "View public interface preview" in html,
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
    checks[f"required page exists: {page}"] = (ROOT / page).is_file()


# Keep project-card and case-study technology tags aligned with the project claim register.
try:
    project_claims = json.loads(PROJECT_DATA.read_text(encoding="utf-8"))
    project_records = project_claims.get("projects", []) if isinstance(project_claims, dict) else []
    checks["project claim registry has five projects"] = isinstance(project_claims, dict) and isinstance(project_records, list) and len(project_records) == 5
    checks["project claim registry explains its purpose"] = isinstance(project_claims, dict) and bool(project_claims.get("purpose"))
    home_cards = re.findall(r'<article class="project">([\\s\\S]*?)</article>', html)
    for record in project_records:
        name = record.get("name", "unknown project")
        expected_tags = record.get("technologies", [])
        title = record.get("homepage_title", name)
        card_html = next((card for card in home_cards if f"<h3>{title}</h3>" in card), "")
        card_tags = re.findall(r'<span class="tag">([^<]+)</span>', card_html)
        checks[f"homepage project card exists: {name}"] = bool(card_html)
        checks[f"homepage tags match claim register: {name}"] = card_tags == expected_tags
        case_path = ROOT / record.get("case_study_path", "")
        case_html = case_path.read_text(encoding="utf-8") if case_path.is_file() else ""
        tag_block = re.search(r'<div class="tags">(.*?)</div>', case_html, re.S)
        case_tags = re.findall(r'<span class="tag">([^<]+)</span>', tag_block.group(1)) if tag_block else []
        checks[f"case-study exists and tags match registry: {name}"] = bool(case_html) and case_tags == expected_tags
        list_fields = ("implemented_features", "experiments", "planned_features", "measured_results", "limitations")
        checks[f"claim categories and evidence state exist: {name}"] = all(
            isinstance(record.get(field), list) for field in list_fields
        ) and bool(record.get("status")) and bool(record.get("evidence_status"))
        diagram = record.get("architecture_diagram")
        if diagram:
            checks[f"architecture diagram exists and is linked: {name}"] = (ROOT / diagram).is_file() and f'src="../../{diagram}"' in case_html
        else:
            checks[f"deferred architecture is explicitly disclosed: {name}"] = 'id="architecture-pending"' in case_html and "intentionally deferred" in case_html
except (OSError, json.JSONDecodeError, TypeError, AttributeError) as exc:
    checks["project claim registry is valid"] = False
    print(f"Could not parse project claim registry: {exc}")

# Validate the client-side certification explorer's data and CSP boundary.
CERT_PAGE = ROOT / "certifications" / "index.html"
CERT_PAGE_HTML = CERT_PAGE.read_text(encoding="utf-8") if CERT_PAGE.is_file() else ""
CERT_JS = CERTIFICATION_SCRIPT.read_text(encoding="utf-8") if CERTIFICATION_SCRIPT.is_file() else ""
try:
    cert_records = json.loads(CERTIFICATION_DATA.read_text(encoding="utf-8"))
    checks["certification JSON is a list"] = isinstance(cert_records, list)
    checks["certification JSON preserves 56 records"] = isinstance(cert_records, list) and len(cert_records) == 56
    cert_ids = [record.get("id") for record in cert_records] if isinstance(cert_records, list) else []
    checks["certification record IDs are unique"] = len(cert_ids) == len(set(cert_ids)) and None not in cert_ids
    checks["all certification records have required fields"] = isinstance(cert_records, list) and all(
        all(key in record for key in ("id", "title", "issuer", "platform", "date", "tags", "link", "course_url", "course_url_checked", "focus_areas"))
        for record in cert_records
    )
    checks["certification URLs are HTTPS or null"] = isinstance(cert_records, list) and all(
        value is None or (isinstance(value, str) and value.startswith("https://"))
        for record in cert_records for value in (record.get("link"), record.get("course_url"))
    )
except (OSError, json.JSONDecodeError, TypeError, AttributeError) as exc:
    cert_records = []
    checks["certification JSON is valid"] = False
    print(f"Could not parse certification JSON: {exc}")

cert_csp = re.search(r'<meta\s+http-equiv="Content-Security-Policy"\s+content="([^"]+)"', CERT_PAGE_HTML, re.I)
checks["certification page exists"] = CERT_PAGE.is_file()
checks["certification page uses self-only script policy"] = bool(cert_csp and "script-src 'self'" in cert_csp.group(1) and "script-src 'none'" not in cert_csp.group(1) and "'unsafe-inline'" not in cert_csp.group(1).split("script-src", 1)[1].split(";", 1)[0])
checks["certification page uses a self-hosted deferred script"] = '<script src="/assets/certifications.js" defer></script>' in CERT_PAGE_HTML
checks["certification page has no inline JavaScript"] = not re.search(r"<script(?![^>]*\bsrc=)[^>]*>", CERT_PAGE_HTML, re.I)
checks["certification list loads local JSON"] = 'fetch(DATA_URL' in CERT_JS and 'const DATA_URL = "/data/certifications.json";' in CERT_JS
checks["certification list shows personal and course links separately"] = "Verify credential" in CERT_JS and "View course page" in CERT_JS
checks["certification page excludes job-description matcher"] = 'id="jd-text"' not in CERT_PAGE_HTML and 'id="match-jd"' not in CERT_PAGE_HTML and "Which learning is relevant to this JD?" not in CERT_PAGE_HTML
checks["homepage links to certification explorer"] = 'href="/certifications/"' in html
checks["homepage links to role-based resume selector"] = 'href="/resume/"' in html
resume_selector = (ROOT / "resume" / "index.html").read_text(encoding="utf-8") if (ROOT / "resume" / "index.html").is_file() else ""
checks["resume selector offers all three tailored routes"] = all(
    route in resume_selector for route in ("/resume/software-development/", "/resume/qa-testing/", "/resume/ai-ml-data/")
)
for resume_page in ("resume/software-development/index.html", "resume/qa-testing/index.html", "resume/ai-ml-data/index.html"):
    resume_html_path = ROOT / resume_page
    resume_html = resume_html_path.read_text(encoding="utf-8") if resume_html_path.is_file() else ""
    checks[f"resume page supports print-to-PDF: {resume_page}"] = (
        "Print" in resume_html and "Save as PDF" in resume_html and "resume-paper" in resume_html
    )

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
    checks[f"shared base stylesheet linked: {relative}"] = "assets/base.css" in page_html

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

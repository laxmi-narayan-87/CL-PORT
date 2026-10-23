# Staging Portfolio Change Plan

## Status
- Repository: `laxmi-narayan-87/CL-PORT`
- Working baseline: `main` at `6c2f8845043c0478a29b30e705837545537be66c`
- Isolated review branch: `claudex/staging-portfolio-review`
- Scope: inspect and harden the existing `staging-portfolio/` experience without merging, deploying production changes, or altering the original portfolio repository.
- Assumption: the requested change is a full staging-portfolio review and fix-up based on the existing recent portfolio work, since no single bug/change was specified.

## Recon summary
- Static HTML/CSS site; the staging entry point is `staging-portfolio/index.html`, shared styles in `staging-portfolio/assets/base.css` and `home.css`, six HTML pages total including the certification explorer, data-driven credentials, and per-project case studies.
- Existing checker: `python staging-portfolio/.github/scripts/check_site.py`; root CI also runs `.github/scripts/check_site.py`, certification JavaScript syntax check, and a staging SEO/header guard.
- Staging safeguards already present: per-page `noindex, follow`, no canonical tags, Vercel `X-Robots-Tag: noindex, follow`, defensive headers, no staging sitemap or copied Search Console verification file.
- Root GitHub Pages workflow excludes `staging-portfolio/` from published artifacts.
- Latest main changes add coding profile links and adjust education timeline; do not revert those.
- Current main quality and deployment checks report success for the latest visible commit.
- Branch `main` is unprotected according to the public branches response; no branch protection changes will be made.

## Acceptance criteria
1. All existing staging pages remain present and linked correctly.
2. All local fragment links resolve to existing IDs; external `target=_blank` links use `noopener noreferrer`.
3. Every staging HTML page keeps exactly one `noindex, follow` robots directive, no canonical tag, and staging-host Open Graph URLs.
4. The Vercel response-header policy keeps noindex and the required security headers.
5. Production Pages artifact remains isolated from staging.
6. Existing content claims, contact details, education data, and project links are not fabricated or rewritten without specific evidence.
7. CSS remains responsive and accessible: visible focus, skip navigation, reduced-motion support, semantic landmarks, and usable mobile navigation.
8. Relevant automated checks pass; every test result must be reported with the exact evidence and limitations.

## Planned implementation scope
- Inspect every staging HTML page, CSS/JS, link targets, metadata, headers and workflows.
- Apply only evidence-backed, minimal fixes that do not remove or weaken SEO/privacy/release-safety guarantees.
- Keep changes confined to staging and its dedicated checks unless a root checker requires a narrowly-scoped regression guard.
- Create an auditable change record in `PLAN-REVIEW-LOG.md`.

## Risks and non-goals
- GitHub API access can commit individual files but cannot run local commands or render screenshots; source checks and hosted CI are not a substitute for cross-browser visual inspection.
- Vercel account settings, access protection, root directory, and live response headers require deployment-dashboard or live HTTP access and must not be assumed from repository source alone.
- No production promotion, PR merge, custom domain change, account/security setting change, or branch protection mutation.
- No new claims, fake metrics, invented testimonials, or fabrication of work/results.

## Proof commands
Run from repository root where a local checkout is available:
- `python .github/scripts/check_site.py`
- `python staging-portfolio/.github/scripts/check_site.py`
- `node --check staging-portfolio/assets/certifications.js`
- Optionally validate HTML with an HTML checker and inspect all routes and responsive viewports manually.

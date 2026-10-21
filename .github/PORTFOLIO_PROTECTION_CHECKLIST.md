# Portfolio isolation, SEO, and release-safety checklist

**Last updated:** 2026-10-22  
**Purpose:** Keep testing copies separate from the original portfolio and prevent staging metadata or deployments from damaging production search visibility.

## Scope and canonical source of truth

- **Original portfolio:** [laxmi-narayan-87/portfolio](https://github.com/laxmi-narayan-87/portfolio), branch `portfolio`. Its canonical homepage is `https://laxmi-narayan-87.github.io/portfolio/`.
- **Testing copy:** `laxmi-narayan-87/CL-PORT/staging-portfolio/`, intended for the separate Vercel project at `https://cl-port-staging-portfolio.vercel.app/`.
- **Separate root site:** `CL-PORT`'s own root site remains distinct. Its GitHub Pages workflow now excludes the staging directory.

## Implemented and source-verified

- [x] All six staging HTML pages (home and five case studies) contain `<meta name="robots" content="noindex, follow">`.
- [x] Added a staging-only `vercel.json` response-header policy with `X-Robots-Tag: noindex, follow`, `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy`, and a restrictive `Permissions-Policy`.
- [x] Removed canonical link tags from staging HTML so it doesn't send canonical signals to an unintended host.
- [x] Updated staging Open Graph URLs and homepage structured-data URL to the Vercel staging hostname.
- [x] Removed the staging sitemap. A test-only copy should not be submitted as a production sitemap.
- [x] Removed the copied Google Search Console verification HTML file from the staging directory. The original repository's verification file was not changed.
- [x] Changed the `CL-PORT` GitHub Pages workflow to build a clean `_site` artifact that explicitly excludes `staging-portfolio/`, `.github/`, and the generated output directory.
- [x] Pinned GitHub Pages deployment actions to full commit SHAs from verified upstream releases; constrained workflow permissions and disabled persisted checkout credentials.
- [x] Made the root `CL-PORT` quality checker fail if the Pages deployment stops excluding staging.
- [x] Made the root quality workflow execute both the root-site checks and the staging SEO/header checks. The inactive nested workflow file was removed to avoid implying GitHub runs it.
- [x] Added production-side CI checks in `laxmi-narayan-87/portfolio` to enforce `index, follow`, exact production canonicals, Open Graph URLs, and the homepage structured-data URL across the homepage and five case studies.
- [x] Kept the original production HTML, canonical metadata, and production sitemap unchanged; the production change is limited to its checker and quality workflow.

## Account and deployment checks still requiring dashboard access

These cannot be safely inferred from source code. The connected Vercel API currently denies access to this project, and the connected GitHub API denies access to branch-protection settings. No protection settings were changed.

- [ ] **Vercel project linkage:** In [the staging project settings](https://vercel.com/laxminarayan955459-6139s-projects/cl-port-staging-portfolio), confirm the linked repository is `laxmi-narayan-87/CL-PORT`, the Production Branch is `main`, and the **Root Directory is `staging-portfolio`**. The `vercel.json` header policy is effective only when this file is at the Vercel project's configured root.
- [ ] **Vercel privacy:** Confirm Deployment Protection / Vercel Authentication (SSO) is enabled if the staging page is intended to be private. If you deliberately make it public for review, keep the `noindex` meta tag and response header. `noindex` is not access control.
- [ ] **Domain and configuration separation:** Confirm the staging project has no production custom domain, and is not sharing production redirects, routing rules, environment variables, or a project/domain alias with the original portfolio.
- [ ] **GitHub branch rules:** Add rulesets for `CL-PORT:main` and `portfolio:portfolio`: require pull requests, require the relevant `Static site quality checks / quality` job to pass, block force pushes, and prevent branch deletion. For a solo-maintained portfolio, requiring one external approval can make the branch impossible for you to merge; prioritize PR + checks and decide review requirements accordingly.
- [ ] **Deployment verification:** After the next GitHub Actions run completes, confirm the root site still works, the GitHub Pages path `/CL-PORT/staging-portfolio/` is no longer published, and the separate Vercel staging site serves the `X-Robots-Tag` header. The active Vercel project could not be inspected from this connection.
- [ ] **Search Console review:** Keep the production Search Console property and sitemap limited to the original portfolio URL and `https://laxmi-narayan-87.github.io/portfolio/sitemap.xml`. Do not submit a staging sitemap. If any old staging URL remains in results, inspect that exact staging URL and request recrawling/removal for staging URLs only; never remove the production URLs.

## Release checklist for every future change

- [ ] Test the staging deployment and links before promoting anything.
- [ ] Keep `noindex, follow` and the staging `X-Robots-Tag` on the testing project.
- [ ] Keep staging canonicals absent and do not add staging URLs to the production sitemap or structured data.
- [ ] Promote approved content to the original `portfolio` repository only after reviewing the diff; do not copy `noindex` into production.
- [ ] Recheck canonical URL, robots metadata, sitemap URLs, broken links, page titles/descriptions, and rendered mobile/desktop behaviour after a release.
- [ ] Never commit secrets or credentials. Keep the public static portfolio free of server-side secrets, forms, and third-party scripts unless separately reviewed.

## Important crawler behaviour

Do not try to enforce `noindex` by disallowing staging URLs in `robots.txt`: a crawler must be able to access the page or response to read the `noindex` directive. Google also notes that de-indexing happens after recrawling, so an old result may persist until it revisits the URL. For sensitive previews, use Vercel access protection in addition to SEO directives.

References: [Google Search Central — Block indexing](https://developers.google.com/search/docs/crawling-indexing/block-indexing) · [GitHub — Ruleset protections](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)

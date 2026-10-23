# Portfolio staging workspace

This directory is an isolated test copy of the portfolio maintained in [laxmi-narayan-87/portfolio](https://github.com/laxmi-narayan-87/portfolio), branch `portfolio`. It is not the production source of truth.

## Non-negotiable SEO boundary

- Every staging HTML page uses `<meta name="robots" content="noindex, follow">`.
- `vercel.json` adds `X-Robots-Tag: noindex, follow` plus security response headers for the staging deployment.
- Staging pages have **no canonical link**. Their Open Graph URLs use the Vercel staging hostname, not the production hostname or the old GitHub Pages staging path.
- A staging sitemap and the copied Google Search Console verification file are intentionally absent.
- Do not submit staging URLs or a staging sitemap in the production Search Console property.
- Keep the production portfolio's `index, follow`, canonical URLs, structured-data URL, and sitemap intact. Never copy the staging `noindex` directive into production.

## Deployment separation

The repository-level GitHub Pages workflow explicitly excludes `staging-portfolio/` from its site artifact. The Vercel project should use this directory as its Root Directory and retain deployment protection when private testing is intended. Verify that setting in Vercel before relying on the project-level response headers.

## Certification page

The staging portfolio has a dedicated `/certifications/` page backed by `data/certifications.json`, copied from the certification inventory in the Placement Intelligence repository. The page provides a straightforward searchable, filterable list with personal credential links and separately labeled public course pages where available. There is no job-description matcher or server-side processing of user input. The page remains `noindex, follow`.

## Verification

Run `python staging-portfolio/.github/scripts/check_site.py` from the repository root. The staging quality checker fails if any HTML page loses `noindex, follow`, acquires a canonical, points its social URL at the wrong host, or if the Vercel response-header policy drifts.

## Project claim register

`data/project-claims.json` is the canonical register for each featured project's technology tags, status, implementation claims, experiments, planned work, measured-results state, limitations, and evidence state. The homepage and case-study pages are narrative views; their technology tags must exactly match the register. The staging quality checker validates this consistency and verifies architecture diagrams where the implementation is sufficiently understood.

Keep the categories separate when updating a case study:
- **Implemented:** backed by the accessible repository or recorded project evidence.
- **Experiment:** an approach under evaluation, without implying a successful result.
- **Planned:** proposed work that has not shipped.
- **Measured result:** publish the configuration, evaluation method, and outcome together; do not substitute pipeline volume for model quality.
- **Limitations:** state constraints and known gaps rather than hiding them in future-work copy.

DarkSense AI's detailed architecture and case study remain provisional until its application implementation can be shared. The current public folder is an interface/flowchart preview, not the application's source of truth.

## Role-specific resumes

The `/resume/` route asks visitors to choose a role and opens a matching, print-ready resume for software development, QA/testing, or applied AI/ML and data. The profile variants reuse the same project facts and are formatted for the browser's Print → Save as PDF workflow.

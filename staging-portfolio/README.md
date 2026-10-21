# Portfolio staging workspace

This directory is a staging copy of the live portfolio repository: https://github.com/laxmi-narayan-87/portfolio (branch `portfolio`).

Make and test changes here before manually reviewing and promoting them to the live portfolio. The root `CL-PORT/index.html` and existing DarkSense project are kept separate.

The staging copy does not automatically update the live portfolio. Before publishing a separate preview, adapt canonical/OG URLs, sitemap entries, verification files, and CI workflow paths for the staging URL.

## Staging SEO policy

This directory is for testing and review only. Every HTML page must include `<meta name="robots" content="noindex, follow">`. The staging quality check enforces this so test pages are not intentionally offered for search indexing. Do not carry this directive into the production portfolio when promoting approved changes.

# CL-PORT

Personal engineering portfolio and project workspace.

## Repository structure

- **Root site** — portfolio pages and shared assets.
- **`staging-portfolio/`** — isolated working copy for portfolio iteration.
- **`master-checker/`** — Master Checker dashboard and supporting files.
- **`darksense/`** — DarkSense AI project materials.
- **`foddb/`** — FODDB project workspace.
- **`.github/scripts/`** — repository-level validation scripts.
- **`.github/workflows/`** — automated repository checks.

## Quality checks

Run the root-site checks:

```bash
python .github/scripts/check_site.py
```

Run the staging workspace checks:

```bash
python staging-portfolio/.github/scripts/check_site.py
```

Check the certification explorer JavaScript syntax:

```bash
node --check staging-portfolio/assets/certifications.js
```

The GitHub Actions quality workflow runs these checks on its configured events.

## Working principles

- Keep project claims evidence-based and distinguish implemented work from experiments and plans.
- Preserve existing assets unless a change explicitly requires otherwise.
- Keep changes scoped to the relevant project or workspace.
- Review accessibility, broken links, and unintended external requests when modifying site content.

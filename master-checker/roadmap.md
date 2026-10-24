# Master Checker roadmap

## Priority 0 — Evidence and privacy
- [ ] Review this public folder for accidental personal data or secrets before adding future entries.
- [ ] Keep raw credentials, private application IDs, private contact details and confidential interview notes out of the public repository.
- [ ] For any potentially exposed secret, rotate it at the provider and verify that the old value is no longer usable; never paste the secret into an issue or commit.

## Priority 1 — Oxcel QA deliverable
- [ ] Revisit all seven source pages.
- [ ] Give each issue a stable ID and preserve exact source text.
- [ ] Record page URL, section, issue type, severity, expected correction (only for the QA report), screenshot/evidence, and verification date.
- [ ] Deduplicate the issue list and calculate the total only after review.
- [ ] For the clone, compare the current original and current clone separately from the grammar audit.
- [ ] Fix only proven mismatches in the clone. Preserve the original's wording even where it contains errors.
- [ ] Re-test the deployed clone and record the commit and deployment URL.

## Priority 2 — CityHangAround research
- [ ] Retest both `www` and non-`www` entry points.
- [ ] Record timestamp, HTTP/SSL behavior, redirects and screenshots.
- [ ] Separate directly verified SEO facts from estimated traffic or inferred causes.
- [ ] Finish recommendations with evidence and limitations.
- [ ] Record whether the assignment video/report was actually submitted.

## Priority 3 — Backend and project verification
- [ ] Rasoi: test Supabase connection with a minimal query using a secure environment variable.
- [ ] Verify the selected backend from the running environment; do not infer it only from local shell output.
- [ ] Test a small import, compare row counts, then plan the full migration.
- [ ] Check Vercel deployment logs and environment-variable scope after the database connection works.
- [ ] DarkSense: verify all public claims against code and the live application.
- [ ] Ablespace and Nimbus: turn notes into reproducible cases and record pass/fail results.

## Priority 4 — Plugin validation
- [ ] QA Quality Agent: list supported operations, run one real test workflow, capture output and limitations.
- [ ] MiroFish: verify whether the plugin merely describes/connects to the repository or can actually execute against a live service.
- [ ] Update plugin status only after an end-to-end test.

## Priority 5 — Career and portfolio
- [ ] Recheck job listings and deadlines before applying.
- [ ] Keep a private application tracker outside this public repo.
- [ ] Draft the Portfolio Handbook outline.
- [ ] For each project, record problem, architecture, alternatives, trade-offs, evidence, limitations and likely interviewer questions.
- [ ] Continue the Winter Arc public journal with professional-only information.

## Definition of done
A task can be marked **Completed** only when its deliverable exists and there is evidence such as a verified commit, test output, live URL check, submitted file/receipt, or source-backed report. Otherwise use **In progress**, **Planned**, **Blocked**, or **Needs verification**.

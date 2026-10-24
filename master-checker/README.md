# Master Checker — October 2026

A dated, evidence-aware tracker of work recorded in prior ChatGPT conversations for **1–24 October 2026**. This is a reconstruction of the available conversation history, not a complete device/activity log. If an exact date was not available, the task is labelled `DATE_UNCONFIRMED` rather than assigned an invented date.

## Purpose

Capture for every workstream:
- **What** was done or proposed.
- **When** it was recorded.
- **Why** it mattered.
- **Implementation steps / decisions** already recorded.
- **Vision and intended outcome**.
- **Status** and the next evidence-based action.
- **Reference** to a repository, website, or project where known.

## Contents

- [Visual task dashboard](dashboard.html) — search and filter the task ledger, review status counts, and view the suggested weekend plate.
- [Task ledger (CSV)](tasks.csv) — filterable rows with dates, rationale, steps, status, next action and references.
- [Timeline and workstream notes](timeline.md) — readable dated summary, decisions and key project context.
- [Roadmap](roadmap.md) — priorities and criteria for marking tasks complete.

## Status rules

- **Completed** — the recorded deliverable or step is confirmed as completed.
- **In progress** — work started, but the full outcome is not confirmed.
- **Planned** — intention or approach discussed, not execution.
- **Blocked** — a known issue prevents progress.
- **Needs verification** — a previous claim, current state, deployment, or result needs fresh evidence.
- **DATE_UNCONFIRMED** — the month-level context exists, but a reliable day cannot be assigned.

These labels describe the evidence available in conversation history, not a claim that every task has been independently re-tested.

## Important guardrails

1. Keep facts separate from assumptions and plans.
2. Do not mark a website, deployment, plugin, migration, or submission complete without checking the actual result.
3. Preserve the user's explicit constraint for Oxcel cloning: the original page is the source of truth; do not invent, improve, redesign, or rewrite.
4. Do not store passwords, API keys, tokens, private application identifiers, contact details, sensitive personal information, or confidential interview notes in this public repository.
5. Before publishing new detail, check that it is appropriate for a public portfolio repo.
6. Update the CSV and supporting notes after each meaningful session; include date and evidence.

## Highest-priority open work

1. **Oxcel recruitment/QA deliverables:** verify each grammar finding, deduplicate the seven-page issue list, and prepare reproducible evidence.
2. **Marathahalli clone:** compare current live original and clone, then fix only confirmed differences.
3. **CityHangAround:** retest the reported SSL issue and finish the evidence-backed SEO/digital-presence report.
4. **Rasoi:** diagnose the Supabase/PostgreSQL connection before retrying a full import; verify Vercel against a working database.
5. **Ablespace/Nimbus QA:** turn recorded scenarios and observations into executable or reproducible test cases.
6. **Plugins:** verify real supported capabilities rather than relying on the fact that plugin creation was reported.
7. **Portfolio Handbook:** convert the concept into a structured document with evidence-backed project chapters.

## Scope note

This tracker includes relevant work from October 2026 and a small number of ongoing project/security follow-ups from earlier context where they materially affect the next action. It deliberately excludes personal identifiers and secret values.

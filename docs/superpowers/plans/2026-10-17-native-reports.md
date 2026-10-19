# Native weekly report pages implementation plan

**Goal:** Read full Urofragen research and maintenance reports on the existing website in Spanish, English and German, reached from the learning homepage.

**Architecture:** Keep the six dated Markdown reports authoritative and unchanged. A deterministic standard-library Python generator renders complete static reports and three archives. A main-branch workflow rebuilds report pages after source commits and explicitly requests the existing Pages build. Quiz construction remains separate to preserve importer rollback boundaries.

**Constraints:** Preserve all clinical text, sources, relevance grades, confidence, dates, audit JSON and question/review data. No new medical research or approvals. Existing merge/publication authorization applies. Python 3.8+, no runtime CDN dependency. Canonical web English has no suffix; Spanish uses -es, German -de. Canonical German source Markdown stays unsuffixed.

## Task 1: Website reports and publication

- [x] Add `review/verify_reports.py` and observe failure for missing native rendering/navigation.
- [x] Implement `tools/build_reports.py`: discover complete language triplets, render safe Markdown, rewrite local report links, produce dated pages and newest-first archives; validate before writing.
- [x] Add responsive `assets/reports.css`, update only the homepage report target in `build.py`, regenerate the quiz HTML.
- [x] Add report generation/tests to `.github/workflows/pruefung.yml`; add serialized `.github/workflows/publish-reports.yml` for source-only report updates, ordinary fast-forward pushes and explicit legacy Pages rebuild.
- [x] Document native URLs and source/publication boundaries in `weekly-reports/README.md` and the project README.
- [x] Run new tests plus the current full workflow checks. Verify desktop/mobile navigation, all language switches, tables/code, unchanged browser progress and no missing local links.
- [x] Obtain independent code review; resolve important findings with regression tests.
- [ ] Publish exact tested tree in a PR, await CI, merge with expected head, inspect Pages and verify actual web URLs.

## Review focus

- Missing translations must preserve the previously complete generated archive.
- Relative cross-series links and monitoring-state anchors must resolve natively.
- Markdown HTML and unsafe schemes must never become executable content.
- Concurrent source publication must never overwrite another contributor's main commit.
- Report publication must not regenerate or modify questions, approvals, saved learning state or CME assets.

## Verification record

All current Python/Node workflow checks passed. Full CME and multilingual CME Chromium suites passed, plus the native report desktop/mobile suite. Chromium 151 headless shell was used locally because the full Chrome process singleton is restricted in this environment; GitHub CI uses its normal bundled Chromium. Screenshots visually inspected. Source Markdown and question/approval/CME data remain unchanged. Next-edition regression reproduced (15 pages versus a fixed nine) and corrected by source-discovered validation; browser reference-content checks now open their dated archived fixture.

Independent read-only review confirmed all nine generated pages match regeneration, normalized full text is preserved in all six reports, and audit JSON matches exactly. No remaining actionable findings.

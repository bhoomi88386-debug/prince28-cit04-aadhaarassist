# Dataset: AadhaarAssist

Helps service-centre operators with Aadhaar enrolment and update rules: valid documents, update limits, fees and process, in Tamil and English.

- **Start target:** FAQs + document list + regulations
- **Full target:** + circulars, notifications and Tamil versions (1,200+ pages)
- **Collected by:** `scripts/fetch.py` as `examate-student-bot` (https://github.com/bhoomi88386-debug/prince28-cit04-aadhaarassist): robots.txt respected, at most 4 requests at once, 0.5 s between requests to one site.

## Where the documents come from

- https://uidai.gov.in/

## Terms I follow

Public UIDAI documents. Never store real Aadhaar numbers.

- Every answer links to the original document.
- No personal data is collected.

<!-- generated:start -->
## Sources (generated 2026-11-23 19:51 UTC by scripts/dataset_report.py)

| Source | Licence / terms | Files | MB | Pages* | How | Fetched | Example URL |
|---|---|---|---|---|---|---|---|
| test | Local test only | 1 | 21.0 | 0 | http | 2026-11-23 | http://127.0.0.1:8765/slow.pdf |
| uidai | UIDAI Website Copyright Policy - reproduction with attribution; research/private study only; non-commercial; third-party content excluded | 1 | 18.4 | 68 | http | 2026-11-23 | https://www.uidai.gov.in/images/LR_Aadhaar_Handbook_2026.pdf |

**Total:** 2 files, 39.3 MB, 68 pages. Not downloaded: 0 blocked by robots.txt, 1 failed.

*Pages = PDF pages, plus one page per 3,000 characters of text or HTML.

## Files (first 2 of 2)

The complete list, with a sha256 fingerprint of every file, is `data/manifest.jsonl`.

| # | Title / file | Source | Pages | Fetched | URL |
|---|---|---|---|---|---|
| 1 | Slow Download Test | test |  | 2026-11-23 | http://127.0.0.1:8765/slow.pdf |
| 2 | Aadhaar Handbook 2026 | uidai | 68 | 2026-11-23 | https://www.uidai.gov.in/images/LR_Aadhaar_Handbook_2026.pdf |
<!-- generated:end -->

## Known gaps

- (what is still missing from the start target, and why)

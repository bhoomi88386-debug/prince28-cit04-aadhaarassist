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
## Sources (generated 2026-11-24 06:42 UTC by scripts/dataset_report.py)

| Source | Licence / terms | Files | MB | Pages* | How | Fetched | Example URL |
|---|---|---|---|---|---|---|---|
| uidai | UIDAI Website Copyright Policy - reproduction with attribution; research/private study only; non-commercial; third-party content excluded | 4 | 22.0 | 127 | http | 2026-11-24 | https://www.uidai.gov.in/images/LR_Aadhaar_Handbook_2026.pdf |

**Total:** 4 files, 22.0 MB, 127 pages. Not downloaded: 0 blocked by robots.txt, 0 failed.

*Pages = PDF pages, plus one page per 3,000 characters of text or HTML.

## Files (first 4 of 4)

The complete list, with a sha256 fingerprint of every file, is `data/manifest.jsonl`.

| # | Title / file | Source | Pages | Fetched | URL |
|---|---|---|---|---|---|
| 1 | Aadhaar Enrolment and Update First Amendment Regulations 2026 | uidai | 35 | 2026-11-24 | https://backend.uidai.gov.in/get/files/media/document/2026-06/Aadhaar_Enrolment_and_Update_First_Amendment_Regulations_2026.pdf |
| 2 | UIDAI Frequently Asked Questions | uidai | 2 | 2026-11-24 | https://uidai.gov.in/en/faq |
| 3 | List of Supporting Documents for Aadhaar Enrolment and Update | uidai | 22 | 2026-11-24 | https://www.uidai.gov.in/images/commdoc/List_of_Supporting_Document_for_Aadhaar_Enrolment_and_Update.pdf |
| 4 | Aadhaar Handbook 2026 | uidai | 68 | 2026-11-23 | https://www.uidai.gov.in/images/LR_Aadhaar_Handbook_2026.pdf |
<!-- generated:end -->

## Known gaps

- The three start-target categories (FAQs, supporting documents and regulations) are collected.
- The current FAQ extraction contains only 3 app-related questions; broader Aadhaar FAQs still need coverage.
- The full corpus still needs additional circulars, notifications and Tamil-language versions.
- More documents are needed to improve coverage and validate the estimated corpus size.

## Duplicate detection

Duplicate detection was performed using SHA-256 hashes from
`data/manifest.jsonl`.

- Duplicate groups: 0
- Extra duplicate downloads: 0

No downloaded files with identical SHA-256 hashes were found.

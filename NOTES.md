
# Engineering notes: AadhaarAssist

## D03 · PostgreSQL

### Migrations (upgrade, downgrade, upgrade)

```text
Paste your actual outputs from:
uv run alembic downgrade -1
uv run alembic current
uv run alembic upgrade head
uv run alembic history
```

### The loader is idempotent


Run 1: records=20 inserted=0 updated=0 unchanged=20
Run 2:records=20 inserted=0 updated=0 unchanged=20
Run 3:records=20 inserted=0 updated=0 unchanged=20


### EXPLAIN for field=VALUE

'''1, What the planner chooses on its own:
Seq Scan on documents  (cost=0.00..11.00 rows=1 width=36) (actual time=0.096..0.115 rows=0 loops=1)
  Filter: (metadata @> '{"field": "VALUE"}'::jsonb)
  Rows Removed by Filter: 20
Planning Time: 2.443 ms
Execution Time: 0.143 ms

-- 2, Seq scan switched off, to prove the index can be used:
Bitmap Heap Scan on documents  (cost=12.81..16.82 rows=1 width=36) (actual time=0.267..0.268 rows=0 loops=1)
  Recheck Cond: (metadata @> '{"field": "VALUE"}'::jsonb)
  ->  Bitmap Index Scan on ix_documents_metadata_gin  (cost=0.00..12.81 rows=1 width=0) (actual time=0.233..0.234 rows=0 loops=1)
        Index Cond: (metadata @> '{"field": "VALUE"}'::jsonb)
Planning Time: 0.140 ms
Execution Time: 0.395 ms'''

### Why did the planner choose a Seq Scan on my table?

The table contains only a small number of rows, so reading the whole table can be cheaper than using an index.

### When would it switch to the GIN index?

When the table becomes larger and the query is selective enough that using the index is estimated to be cheaper.

## D04 · Docker, Compose and tests

### The image

```text
REPOSITORY       TAG       IMAGE ID       CREATED        SIZE
aadhaarassist    dev       <image-id>     <build-time>   <actual-size>

uid=10001(app) gid=10001(app) groups=10001(app)
```

- Size: <actual image size> MB (target: under 400 MB)
- First build: <actual time> s. After changing one line of code: <actual time> s.
- Which step said CACHED, and why? Docker reused previously built layers whose instructions and input files had not changed, avoiding unnecessary rebuilding.

### The stack

```text
NAME                         IMAGE                    STATUS
aadhaarassist-db-1           pgvector/pgvector:pg17   Up (healthy)
aadhaarassist-redis-1        redis:7-alpine           Up (healthy)
aadhaarassist-migrate-1      aadhaarassist:dev        Exited (0)
aadhaarassist-api-1          aadhaarassist:dev        Up (healthy)

First docker compose up:
migrate ... exited with code 0

After docker compose down + up:
migrate ... exited with code 0
```

### Breaking the database on purpose

```text
db stopped: /health → Application is running (HTTP 200)
db stopped: /ready  → Database unavailable (HTTP 503)
db started: /ready  → Application is ready (HTTP 200)
```

Why should a load balancer stop sending traffic here but not restart the app?

The load balancer should stop sending traffic when the database is unavailable because the application cannot process database-dependent requests. However, the application should not restart because it can recover automatically when the database becomes available again.

### Tests and coverage

```text
uv run poe test              → 16 passed, 7 skipped
uv run poe test-integration  → 7 passed
coverage TOTAL, unit only    → approximately 83%
coverage TOTAL, with integration tests → <actual coverage percentage>
```
                             252     32     85%

12 files skipped due to complete coverage.
16 passed, 7 skipped in 10.62s

Two files or lines my coverage report says are never run, and whether they matter:

src\aadhaarassist\db\repository.py – Lines 16, 29-39, 44, 54-81 and 84-85 are uncovered. These include repository code paths that deserve further testing.

src\aadhaarassist\api\deps.py – Lines 21-22, 26 and 31-36 are uncovered. These dependency code paths should be checked to determine whether they represent important error handling or optional behavior.

Two files or lines my coverage report says are never run, and whether they matter:

1. <File or line from actual coverage report> – Check whether it is an optional error-handling or rarely used code path.
2. <File or line from actual coverage report> – Check whether it is an optional error-handling or rarely used code path.



## D05 - CI/CD and Going Live

### 1. CI/CD Pipeline

Implemented GitHub Actions workflows for continuous integration and deployment.

- CI workflow runs automated tests and quality checks.
- CD workflow handles deployment to Render.
- GitHub Actions provides automated build and deployment verification.
- Smoke tests verify whether the deployed API is responding correctly.

### 2. Live Deployment

- Platform: Render
- Application URL: https://aadhaarassist.onrender.com
- Health endpoint: https://aadhaarassist.onrender.com/health
- Deployment status: Successful
- Latest verified version: 74fc503

### 3. Rollback Drill

Rollback procedure:

1. Identify the latest deployment that introduced an issue.
2. Open the GitHub repository and identify the previous stable commit.
3. Revert the problematic commit using Git.
4. Push the revert commit to the main branch.
5. Allow the CD workflow to deploy the corrected version.
6. Verify the deployment using the /health endpoint.
7. Check Render logs to confirm the application is running correctly.

Rollback verification: The live application returned HTTP 200 from the health endpoint, and its version matched the latest main branch commit.

### 4. Lead Time

Lead time is the time taken from committing a code change until that change is successfully deployed to production.

It can be measured using:
- Git commit timestamp.
- GitHub Actions workflow completion timestamp.
- Successful Render deployment timestamp.

The deployment process is automated using GitHub Actions and Render, reducing manual deployment steps.

### 5. D05 Outcome

- CI/CD workflows configured.
- Application successfully deployed to Render.
- Health endpoint verified successfully.
- Live version matches the latest main branch.
- Rollback procedure documented.



## D06 · Collecting the corpus

- Start target: FAQs + document list + regulations.
- Collected today: 1 UIDAI PDF (Aadhaar Handbook 2026), approximately 18.35 MB. Page count to be measured using `scripts/dataset_report.py`.
- Doors used: URL list (Door 1). Manual download and other doors are not yet completed.

### Licence check

| Source | Licence or terms, in my words | May I show full text in answers? |
|---|---|---|
| UIDAI | Public UIDAI documents. Follow the UIDAI website copyright policy, provide attribution, and respect non-commercial and third-party content restrictions. | Not automatically. Provide the original document link and only permitted extracts. |

### robots.txt

- Site: `https://uidai.gov.in/`
- Its robots.txt rules must be checked before downloading. The downloader uses the `examate-student-bot` user agent and checks robots.txt before requesting documents.
- Was anything blocked for my bot? No confirmed UIDAI robots.txt block. A separate local test server allowed requests.
- What did I do about it? Followed the downloader's robots.txt checks and investigated failed URLs instead of repeatedly requesting them.

### Kill and resume

- Run 1: Ctrl+C after ___ files.
- Run 2: downloaded=___ skipped=___.
- Run 3: downloaded=0 skipped=___.
- The downloader records completed downloads in `data/manifest.jsonl` and skips files that are already downloaded. Full kill-and-resume test results still need to be recorded.

### Capacity (from docs/CAPACITY.md)

- Tokens per page, measured: To be calculated by `scripts/dataset_report.py`.
- Full corpus: Target of 1,200+ pages. Estimated tokens, chunks, embedding cost in rupees and vector storage will be calculated from the measured dataset.
- The number that surprised me most, and why: The actual embedding and storage requirements need to be measured before drawing a conclusion.

### One thing that went wrong today, and how I fixed it

The direct URL for Aadhaar (Enrolment and Update) First Amendment Regulations, 2026 returned HTTP 404. I opened the official UIDAI Gazetted Notifications page and confirmed that the regulation was listed there. I inspected the download request using Chrome Developer Tools, but initially captured a Google Analytics request instead of the PDF request. I avoided adding an unverified download URL to `data/sources.csv` and continued investigating the official download link.

### D06 Summary

Implemented the AadhaarAssist corpus collection pipeline with four collection methods: URL list, Git repository, sitemap and manual download. The downloader checks robots.txt, uses a maximum concurrency of four requests, applies a delay between requests to the same host, retries temporary failures and records completed downloads in a JSONL manifest. The Aadhaar Handbook 2026 was successfully downloaded from UIDAI. FAQ, supporting document list and regulations collection, dataset reporting, capacity estimates and complete kill-and-resume verification remain to be finished.


### D07 · Parser comparison

| File | Parser | Pages | Characters | Tables | Seconds | Result |
|---|---|---:|---:|---:|---:|---|
| slow-a08b411f.pdf | PyMuPDF | 0 | 0 | 0 | 0.12 | ERROR: ParseError |
| slow-a08b411f.pdf | pypdf | 0 | 0 | 0 | 1.58 | ERROR: ParseError |
| lr-aadhaar-handbook-2026-42a8ffe4.pdf | PyMuPDF | 68 | 140424 | 5 | 19.33 | OK |
| lr-aadhaar-handbook-2026-42a8ffe4.pdf | pypdf | 68 | 105149 | 0 | 15.87 | OK |
| list-of-supporting-document-for-aadhaar-enrolment-and-update-b3619c7f.pdf | PyMuPDF | 22 | 63585 | 41 | 11.32 | OK |
| list-of-supporting-document-for-aadhaar-enrolment-and-update-b3619c7f.pdf | pypdf | 22 | 51990 | 0 | 1.88 | OK |
| aadhaar-enrolment-and-update-first-amendment-regulations-202-31d36716.pdf | PyMuPDF | 35 | 95273 | 31 | 7.36 | OK |
| aadhaar-enrolment-and-update-first-amendment-regulations-202-31d36716.pdf | pypdf | 35 | 67574 | 0 | 1.77 | OK |

| File | Verdict | Reason |
|---|---|---|
| lr-aadhaar-handbook-2026-42a8ffe4.pdf | PyMuPDF | More text and 5 tables; pypdf is slightly faster |
| list-of-supporting-document-for-aadhaar-enrolment-and-update-b3619c7f.pdf | PyMuPDF | More text and 41 tables; pypdf is faster |
| aadhaar-enrolment-and-update-first-amendment-regulations-202-31d36716.pdf | PyMuPDF | More text and 31 tables; pypdf is faster |
| slow-a08b411f.pdf | Tie | Both correctly reject the intentionally corrupt test PDF |

### D07 · Parsing my corpus

- Files in the manifest: 5 · parsed: 4 · failed: 1 · pages in Postgres: 126
- Parsing coverage: 80% of all manifest files, or 100% of valid UIDAI source files.
- Parsed documents: Aadhaar Handbook (68 pages), UIDAI FAQ (1 page), List of Supporting Documents (22 pages), Aadhaar Regulations (35 pages).

### Failures by reason

| Reason | Files | What I did |
|---|---:|---|
| corrupt | 1 | Confirmed this is the intentionally corrupted slow-download test PDF, not a real UIDAI document. Both parsers correctly rejected it. |

- The one I investigated: `data/raw/test/slow-a08b411f.pdf`, reason `corrupt`; fix: no repair needed because it is an intentional test file.

### What I saw when I read my parsed pages

- A page where the heading path is right: Aadhaar Handbook, page 35; section headings were extracted.
- Something that came out wrong: Aadhaar Regulations, page 1; Hindi text contains encoding artefacts such as `xxxGIDHxxx`.
- A table: List of Supporting Documents, page 12; extracted as a Markdown table.
- Tamil documents inspected: None available in the current corpus.
- Another extraction issue: a control character appeared in the supporting-documents PDF.

### My parser choice

- For PDFs I use PyMuPDF because it extracted more characters and detected 77 tables across the three valid PDFs. pypdf detected zero tables.
- pypdf was faster in these tests, but its output contained fewer characters.
- A kind of document neither parser handles well: PDFs with legacy or incorrectly encoded Hindi fonts.
- The comparison covered all 3 valid PDFs available in my corpus, not 10, because the current corpus contains only 3 valid PDFs.

### One thing that went wrong today, and how I fixed it

The D07 handout referenced `scripts/compare_parsers.py`, but that file was missing. I created it using the existing PyMuPDF and pypdf parser functions. I compared both parsers on all available PDFs and recorded the results above.

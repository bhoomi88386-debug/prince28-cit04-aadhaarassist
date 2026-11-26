
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
### One thing that went wrong today, and how I fixed it

The D07 handout referenced `scripts/compare_parsers.py`, but that file was missing. I created it using the existing PyMuPDF and pypdf parser functions. I compared both parsers on all available PDFs and recorded the results above.

### D07 · Parser comparison

| File | Parser | Pages | Characters | Tables | Seconds | Result |
|---|---|---:|---:|---:|---:|---|
| lr-aadhaar-handbook-2026-42a8ffe4.pdf | PyMuPDF | 68 | 140424 | 5 | 14.86 | OK |
| lr-aadhaar-handbook-2026-42a8ffe4.pdf | pypdf | 68 | 105149 | 0 | 16.98 | OK |
| list-of-supporting-document-for-aadhaar-enrolment-and-update-b3619c7f.pdf | PyMuPDF | 22 | 63585 | 41 | 10.68 | OK |
| list-of-supporting-document-for-aadhaar-enrolment-and-update-b3619c7f.pdf | pypdf | 22 | 51990 | 0 | 1.68 | OK |
| aadhaar-enrolment-and-update-first-amendment-regulations-202-31d36716.pdf | PyMuPDF | 35 | 95273 | 31 | 7.94 | OK |
| aadhaar-enrolment-and-update-first-amendment-regulations-202-31d36716.pdf | pypdf | 35 | 67574 | 0 | 2.26 | OK |

| File | Verdict | Reason |
|---|---|---|

# D08 · LLM Gateway — Day 1 Results

## 1. Provider configuration

- **Primary:** Gemini (`gemini-3.8-flash`)
- **Fallback:** Groq (`openai/gpt-oss-20b`)

### First question on my laptop

- First words after: **Not measured yet**
- Total response time: **Not measured yet**
- Tokens in / out: **Not measured yet**
- Cost: **Not measured yet**

**Expected output:** The gateway should return a response from Gemini when available. If Gemini fails, it should automatically use Groq and return the fallback response.

### Same question on my live URL (second, awake request)

- First words after: **Not measured yet**
- Day 1 target: **Under 1.5 seconds**

**Expected output:** The second request should respond faster if the application and provider connections are already warm. Actual streaming latency must be measured separately.

---

## 2. Tokens: English against Tamil

| Message | Tokens in |
|---|---:|
| "Hi" (baseline: mostly my system prompt) | Not measured |
| The English sentence | Not measured |
| The same sentence in Tamil | Not measured |

- Tamil message token multiplier: **Not measured yet**

**Expected output:** Tamil may require more tokens than the equivalent English sentence, depending on the tokenizer and the exact wording. The ratio must be calculated from actual API usage.

---

## 3. What the model does without my documents

- **Question 6:** "Is this person's Aadhaar linked to their bank account?"
  - Actual response: Not tested / not recorded.
  - Expected behaviour: The model should admit that it cannot know whether an individual's Aadhaar is linked to their bank account without access to verified information.

- **A detail it got wrong or invented:**
  - Actual example: Not recorded.
  - Expected format: Question → Model's answer → Verified truth.

- **Off-topic question:**
  - Actual response: Not recorded.
  - Expected behaviour: The model should politely decline or redirect in one concise sentence.

---

## 4. Fallback and circuit breaker

### Provider health tests

Repeated runs of `uv run python scripts/llm_ping.py` showed:

| Provider | Result | Observed response time |
|---|---|---:|
| Gemini | Initially failed with ReadTimeout / HTTP 503 | Unavailable during those attempts |
| Groq | Successful | 639–1433 ms |
| Gemini (later attempt) | Successful | 2409 ms |
| Groq (same later attempt) | Successful | 1192 ms |

- Gemini's HTTP 503 message indicated temporary high demand.
- Groq successfully returned `pong` in every recorded run.
- One successful Gemini test reported model `gemini-3.5-flash`, not `gemini-3.8-flash`. Verify the configured model before treating this as a successful test of the intended primary model.

### Fallback and circuit breaker results

- With the primary broken, provider: **Gemini (primary failed)**
- Fallback: **Groq (`openai/gpt-oss-20b`)**
- First words after: **Not measured through the application gateway**
- Question at which `llm call gemini … error` stopped appearing: **Not measured**

**Expected behaviour:** When Gemini fails after the configured retry attempts, the gateway should switch to Groq. The circuit breaker should reduce repeated calls to an unhealthy primary provider.

---

## 5. The bill

`/v1/usage` actual application results: **Not recorded yet**.

- Calls today: Not measured
- Errors: Not measured
- Fallbacks: Not measured
- Cost: Not measured
- Average cost per answered question: Not measured
- Day 1 cost target: **Under ₹0.50 per answered question**

**Expected output:** The usage endpoint should return today's call count, errors, fallback count, token usage and total estimated cost in INR.

Average cost formula:

`Total cost in INR / Number of answered questions`

---

## 6. One thing that went wrong today, and how I fixed it

### Problem 1: Gemini provider instability

Gemini repeatedly returned `ReadTimeout` and HTTP 503 errors because the provider was temporarily experiencing high demand.

**Fix / observation:**
- Ran `scripts/llm_ping.py` repeatedly to check both providers.
- Confirmed Groq was responding successfully.
- Later, Gemini also returned a successful `pong` response.
- This confirmed that the fallback provider was reachable even when the primary provider was unavailable.

### Problem 2: Missing request ID context

Running:

`uv run pytest tests/unit/test_gateway.py`

initially failed because `gateway.py` imported `request_id_ctx` from `logging_setup.py`, but that variable was missing.

**Fix:**
- Added a `ContextVar` named `request_id_ctx` in `logging_setup.py`.
- Updated the request middleware to set the request ID before processing the request.
- Reset the context variable after the request finished.

### Problem 3: Incorrect SQLAlchemy import

Alembic initially failed because `Numeric` was not imported correctly.

**Fix:**
- Corrected the import to use `sqlalchemy.Numeric`, not `sqlalchemy.orm.Numeric`.
- Successfully generated the `add_llm_calls` migration.
- Successfully applied it using `uv run alembic upgrade head`.

### Final verification

| Check | Result |
|---|---|
| Gateway unit tests | 19 passed |
| API unit tests | 17 passed |
| Full unit test suite | 59 passed |
| Ruff lint | All checks passed |
| Ruff format | 59 files already formatted |
| Full pytest run | All tests passed |
| Local development server | Started successfully |

Commands executed successfully:

- `uv run pytest -q`
- `uv run pytest tests/unit/test_gateway.py -q`
- `uv run pytest tests/unit/test_api.py -q`
- `uv run poe test`
- `uv run poe lint`
- `uv run alembic upgrade head`
- `uv run poe dev`

**Final status:** The gateway-related unit tests pass, linting and formatting checks pass, the database migration was applied, and the local FastAPI development server started successfully. Provider latency, live URL latency, Tamil token comparison, fallback timing and usage costs still need to be measured.

## D09 · Prompt versions compared

<!-- prompts:start -->

| Prompt version | Correct | Accuracy | Invalid replies | Avg tokens in |
|---|---|---|---|---|
| classify_v1 | 13/20 | 65% | 0 | 85 |
| classify_v2 | 20/20 | 100% | 0 | 288 |
| classify_v3 | 20/20 | 100% | 0 | 600 |
| classify_v4 | 20/20 | 100% | 0 | 684 |

<!-- prompts:end -->

## D09 · Prompts and structured output

- **My best router prompt:** `classify_v4` with **20/20 (100%)**. Versions v2, v3 and v4 all achieved 20/20.
- **What I changed in v4, and what happened to the score:** Added a decision rule explaining that classification must depend on the information required to answer the question, not just keywords. It clarified the difference between document-based questions, live/personal questions and unrelated questions. The score remained 20/20.
- **The question my best version still gets wrong (line, wanted, got), and why I think so:** None in the 20-question test set. Best version achieved 100%.
- **A label in my test set that I changed after seeing the results:** None.
- **Input tokens per question:** v1 — exact average not recorded here; best version — exact average not recorded here. v1 achieved 65%, while v4 achieved 100% (+35 percentage points). The extra accuracy is worth the additional prompt instructions, although token cost should also be considered.

## My contract (DocMeta)

- **Fields I kept from my project card:** `doc_kind`, `year`, `language`, `summary`, `topics`.
- **Fields I deleted, and why they make no sense per document:** Operational details such as fees, update limits, enrolment modes and valid-document lists were not kept as universal metadata fields. They are document-specific content and should be retrieved from the relevant source rather than forced into every document's metadata.
- **The field I tightened, and how:** `year`. It must represent a plausible publication year rather than an arbitrary number. Missing years can remain null, and invalid future values such as 3024 are rejected.

## Extraction run

- **Prompt version:** `extract_v1` · **Documents:** 4 OK, 1 repaired, 0 failed (out of 4 parsed). The repaired record is included in the successful records.
- **Not finished? Why, and how many are left:** The first run stopped because Gemini's circuit breaker was open and Groq returned HTTP 429 rate-limit errors. I waited and reran the same command. Extraction subsequently completed; the final run reported `pending=0`.
- **Most common failure reason, and what I did about it:** The model initially returned a response without a valid JSON object. The repair mechanism retried with the validation error. I also waited for provider rate limits to recover before continuing.
- **A record that was valid but wrong:** The supporting-documents PDF (`f-07e1d5ff18a56ac8e565`) produced a `valid_documents` list containing only seven entries, even though the source PDF contains 41 tables. This is a possible incomplete extraction that needs checking against the original document.
- **Cost at list price:** Rs **0.2673** in total (Rs 0.1499 + Rs 0.1174), approximately Rs **0.0668 per document** across four successfully extracted documents.

## One thing that went wrong today, and how I fixed it

The extraction process stopped because Gemini became unavailable through its circuit breaker and Groq returned a 429 rate-limit error. Instead of resetting the extraction or deleting completed records, I waited for the limits to recover and ran the same command again. The script resumed pending records, used its repair mechanism for invalid JSON, and eventually completed with zero pending and zero failed records.

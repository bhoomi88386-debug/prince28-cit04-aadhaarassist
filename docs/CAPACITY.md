# Capacity plan: AadhaarAssist

Full corpus target: + circulars, notifications and Tamil versions (1,200+ pages)

<!-- generated:start -->
## Measured on my start corpus (2026-11-24 06:42 UTC)

| What | Value |
|---|---|
| Files | 4 |
| Size on disk | 22.0 MB |
| Pages (PDF pages + 1 per 3,000 characters of text/HTML) | 127 |
| Characters of text | 243,437 |
| Estimated tokens (characters / 4) | 60,859 |
| Tokens per page | 481 |
| PDFs with almost no text (scanned? OCR is Day 7) | 0 |
| Files not measured (zip, xlsx, unreadable) | 0 |

## Estimate for the full corpus (target: 1,200 pages)

| What | How | Value |
|---|---|---|
| Scale factor | target / measured | x 9.5 |
| Tokens | measured tokens x scale | 0.58 M |
| Raw files | measured MB x scale | 208 MB |
| Chunks | tokens / 400 x 1.15 overlap | 1,658 |
| Embedding cost, one time | tokens x 1.15 x $0.15 per 1M | $0.10 = Rs 9 |
| Vector storage | chunks x 768 numbers x 4 bytes | 5 MB |
| Text in Postgres | characters x scale x 1.2 | 3 MB |

Assumptions: 4 characters per token, 400-token chunks, 768-dimension embeddings at $0.15 per 1M tokens, Rs 95 per US dollar.
<!-- generated:end -->

## What I conclude

1. Embedding cost is not a major problem: the estimated one-time cost for 1,200 pages is only $0.10 (approximately Rs 9).

2. Estimated vector and text storage is approximately 8 MB (5 MB + 3 MB); it fits only if my database's available storage quota is greater than this amount.

3. I am least sure about the estimated token count because it is extrapolated from 127 pages; I will measure it again using the complete 1,200-page corpus.

4. If the planned 1,200-page corpus grows 10 times, it will reach approximately 12,000 pages, 5.8 million tokens and 16,580 chunks.
   Estimated embedding cost will be about $1 (Rs 95), with approximately 50 MB of vector storage, 30 MB of text storage and 2.08 GB of raw files.

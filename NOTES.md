
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

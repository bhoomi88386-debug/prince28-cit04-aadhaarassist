
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

```text
Run 1: Paste actual output here
Run 2: Paste actual output here
Run 3 (after editing one record): Paste actual output here
```

### EXPLAIN for field=VALUE

```text
Paste the actual output from:
uv run python scripts/explain.py field VALUE
```

### Why did the planner choose a Seq Scan on my table?

The table contains only a small number of rows, so reading the whole table can be cheaper than using an index.

### When would it switch to the GIN index?

When the table becomes larger and the query is selective enough that using the index is estimated to be cheaper.

"""Generate a database-backed ingestion report."""

import asyncio
from datetime import datetime
from pathlib import Path

from sqlalchemy import func, select

from aadhaarassist.db.models import (
    Document,
    IngestItem,
    LlmCall,
    Page,
    ParseFailure,
)
from aadhaarassist.db.session import engine

REPORT_PATH = Path("docs/INGEST_REPORT.md")
START = "<!-- AUTO-GENERATED:START -->"
END = "<!-- AUTO-GENERATED:END -->"
LEARN_START = "<!-- WHAT-I-LEARNT:START -->"
LEARN_END = "<!-- WHAT-I-LEARNT:END -->"


async def collect_report_data() -> dict:
    """Collect ingestion statistics from PostgreSQL."""
    async with engine.connect() as connection:
        documents = await connection.scalar(select(func.count()).select_from(Document))

        pages = await connection.scalar(select(func.count()).select_from(Page))

        page_texts = (await connection.execute(select(Page.text))).scalars().all()

        estimated_tokens = sum(len((page_text or "").split()) for page_text in page_texts)

        failed_items = await connection.scalar(
            select(func.count()).select_from(IngestItem).where(IngestItem.status == "failed")
        )

        parse_failures = await connection.scalar(select(func.count()).select_from(ParseFailure))

        llm_calls = await connection.scalar(select(func.count()).select_from(LlmCall))

        total_cost = await connection.scalar(select(func.coalesce(func.sum(LlmCall.cost_inr), 0)))

        status_result = await connection.execute(
            select(IngestItem.status, func.count()).group_by(IngestItem.status)
        )
        item_statuses = dict(status_result.all())

    return {
        "documents": documents or 0,
        "pages": pages or 0,
        "estimated_tokens": estimated_tokens,
        "dead_letter": failed_items or 0,
        "parse_failures": parse_failures or 0,
        "llm_calls": llm_calls or 0,
        "total_cost": total_cost or 0,
        "item_statuses": item_statuses,
    }


def get_learning_notes(existing: str) -> str:
    """Keep the user's notes between the learning markers."""
    if LEARN_START in existing and LEARN_END in existing:
        return existing.split(LEARN_START, 1)[1].split(LEARN_END, 1)[0].strip()

    return "Add your own notes about what you learnt during the ingestion work."


def write_report(data: dict) -> None:
    """Write updated statistics while preserving manual learning notes."""
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    existing = REPORT_PATH.read_text(encoding="utf-8") if REPORT_PATH.exists() else ""
    learning_notes = get_learning_notes(existing)

    generated = f"""# AadhaarAssist Ingestion Report

{START}
## Database statistics

| Metric | Value |
|---|---:|
| Documents | {data["documents"]} |
| Pages | {data["pages"]} |
| Estimated whitespace-separated tokens | {data["estimated_tokens"]:,} |
| Failed ingestion items (dead-letter) | {data["dead_letter"]} |
| Parse failures | {data["parse_failures"]} |
| LLM calls | {data["llm_calls"]} |
| Total estimated LLM cost (INR) | INR {float(data["total_cost"]):.4f} |

## Ingestion item statuses

| Status | Count |
|---|---:|
"""

    if data["item_statuses"]:
        for status, count in sorted(data["item_statuses"].items()):
            generated += f"| {status} | {count} |\n"
    else:
        generated += "| No ingestion items | 0 |\\n"

    generated += f"""
_Report generated: {datetime.now().astimezone().isoformat(timespec="seconds")}_

{END}

## What I learnt

{LEARN_START}
{learning_notes}
{LEARN_END}
"""

    REPORT_PATH.write_text(generated, encoding="utf-8")
    print(f"Report written to: {REPORT_PATH}")
    print(f"Documents: {data['documents']}")
    print(f"Pages: {data['pages']}")
    print(f"Dead-letter items: {data['dead_letter']}")
    print(f"LLM calls: {data['llm_calls']}")
    print(f"Estimated LLM cost: INR {float(data['total_cost']):.4f}")


async def main() -> None:
    try:
        data = await collect_report_data()
        write_report(data)
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())

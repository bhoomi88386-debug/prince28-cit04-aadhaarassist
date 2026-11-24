"""Compare PyMuPDF and pypdf on the downloaded PDF corpus."""

import argparse
import json
import time
from pathlib import Path

from aadhaarassist.ingest.parse import parse_pdf_pymupdf, parse_pdf_pypdf

MANIFEST = Path("data/manifest.jsonl")


def load_pdfs():
    latest = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        try:
            record = json.loads(line)
            latest[record["url"]] = record
        except (json.JSONDecodeError, KeyError):
            continue

    records = [
        r
        for r in latest.values()
        if r.get("status") == "downloaded"
        and Path(r["path"]).is_file()
        and Path(r["path"]).suffix.lower() == ".pdf"
    ]

    unique = {}
    for record in records:
        unique.setdefault(record["sha256"], record)

    return sorted(
        unique.values(),
        key=lambda r: Path(r["path"]).stat().st_size,
        reverse=True,
    )


def compare(path, parser_name, parser_function):
    started = time.perf_counter()

    try:
        parsed = parser_function(path)
        elapsed = time.perf_counter() - started
        return {
            "parser": parser_name,
            "pages": len(parsed.pages),
            "chars": sum(len(page.text) for page in parsed.pages),
            "tables": sum(page.tables for page in parsed.pages),
            "seconds": f"{elapsed:.2f}",
            "result": "OK",
        }
    except Exception as error:
        elapsed = time.perf_counter() - started
        return {
            "parser": parser_name,
            "pages": 0,
            "chars": 0,
            "tables": 0,
            "seconds": f"{elapsed:.2f}",
            "result": f"ERROR: {type(error).__name__}",
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--paths", nargs="*", default=None)
    args = parser.parse_args()

    if not MANIFEST.exists():
        raise SystemExit("data/manifest.jsonl not found")

    records = load_pdfs()

    if args.paths:
        selected = {str(Path(p)) for p in args.paths}
        records = [r for r in records if str(Path(r["path"])) in selected]
    else:
        records = records[: args.limit]

    if not records:
        raise SystemExit("No matching downloaded PDF files found.")

    lines = [
        "| File | Parser | Pages | Characters | Tables | Seconds | Result |",
        "|---|---|---:|---:|---:|---:|---|",
    ]

    print(f"Comparing {len(records)} PDF file(s)")
    print()

    for record in records:
        path = Path(record["path"])
        print(f"FILE: {path} ({path.stat().st_size:,} bytes)")

        for name, function in (
            ("PyMuPDF", parse_pdf_pymupdf),
            ("pypdf", parse_pdf_pypdf),
        ):
            result = compare(path, name, function)
            print(
                f"  {name}: pages={result['pages']} "
                f"chars={result['chars']} tables={result['tables']} "
                f"seconds={result['seconds']} result={result['result']}"
            )
            lines.append(
                f"| {path.name} | {name} | {result['pages']} "
                f"| {result['chars']} | {result['tables']} "
                f"| {result['seconds']} | {result['result']} |"
            )

        print()

    table = "\n".join(lines)
    print("MARKDOWN COMPARISON TABLE")
    print(table)

    notes = Path("NOTES.md")
    if notes.exists():
        with notes.open("a", encoding="utf-8") as file:
            file.write("\n\n### D07 · Parser comparison\n\n")
            file.write(table)
            file.write("\n\n| File | Verdict | Reason |\n|---|---|---|\n")
        print("\nComparison table appended to NOTES.md.")
    else:
        print("\nNOTES.md not found; copy the table above into your notes.")


if __name__ == "__main__":
    main()

import json
from collections import defaultdict
from pathlib import Path

groups = defaultdict(list)
for line in Path("data/manifest.jsonl").read_text(encoding="utf-8").splitlines():
    record = json.loads(line)
    if record.get("status") == "downloaded" and record.get("sha256"):
        groups[record["sha256"]].append(record)

duplicates = {h: records for h, records in groups.items() if len(records) > 1}
for sha, records in duplicates.items():
    print(f"\nSHA256: {sha}")
    for record in records:
        print(f"  {record.get('url')} -> {record.get('path')}")
print(f"\nDuplicate groups: {len(duplicates)}")
print(f"Extra duplicate downloads: {sum(len(r) - 1 for r in duplicates.values())}")

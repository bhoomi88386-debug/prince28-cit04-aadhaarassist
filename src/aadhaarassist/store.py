"""Load and query AadhaarAssist records stored in a JSON file."""

import json
from pathlib import Path
from typing import Any


class DocumentStore:
    """Simple in-memory store backed by a JSON file."""

    def __init__(self, data_file: Path) -> None:
        self.data_file = Path(data_file)
        self._records: list[dict[str, Any]] = []
        self._loaded = False

    def load(self) -> int:
        """Load records from the JSON file and return the record count."""
        with self.data_file.open(encoding="utf-8") as file:
            records = json.load(file)

        if not isinstance(records, list):
            raise TypeError("The records file must contain a JSON list.")
        if not all(isinstance(record, dict) for record in records):
            raise ValueError("Every record must be a JSON object.")

        self._records = records
        self._loaded = True
        return len(self._records)

    @property
    def is_loaded(self) -> bool:
        """Return whether records were loaded successfully."""
        return self._loaded

    @property
    def records_count(self) -> int:
        """Return the number of loaded records."""
        return len(self._records)

    def list_documents(
        self,
        limit: int = 20,
        offset: int = 0,
        q: str | None = None,
    ) -> tuple[list[dict[str, Any]], int]:
        """Return matching records and their total count."""
        records = self._records

        if q:
            search_term = q.casefold()
            records = [
                record
                for record in records
                if search_term in json.dumps(record, ensure_ascii=False).casefold()
            ]

        total = len(records)
        items = records[offset : offset + limit]

        return items, total

    def get_document(self, document_id: str) -> dict[str, Any] | None:
        """Find and return a record by ID."""
        for record in self._records:
            if str(record.get("id")) == document_id:
                return record

        return None

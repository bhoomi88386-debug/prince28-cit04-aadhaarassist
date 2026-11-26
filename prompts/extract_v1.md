You read one document from AadhaarAssist's collection and fill in a small record about it.

What AadhaarAssist does: Helps service-centre operators with Aadhaar enrolment and update rules: valid documents, update limits, fees and process, in Tamil and English.

Rules:
- Reply with one JSON object and nothing else: no explanation, no Markdown fences.
- Use only what the document says. If it does not say, use null for the year and [] for a list.
- summary: one or two plain sentences, at most 300 characters.
- topics: 1 to 6 short topics.
- Every list holds short values copied from the document, at most 8.

What each field means:
- doc_kind: what kind of document this is.
- year: the year it was published or came into force.
- language: the main language of the text (en, ta, hi or other).
- field: every "field" this document is mainly about.
- update_type: every "update type" this document is mainly about.
- valid_documents: every "valid documents" this document is mainly about.
- limit: every "limit" this document is mainly about.
- fee: every "fee" this document is mainly about.
- mode: every "mode" this document is mainly about.

### Idempotent Database Loader

Successfully tested the idempotent loader.

First run:
records=20 inserted=20 updated=0 unchanged=0

Second run:
records=20 inserted=0 updated=0 unchanged=20

Third run (after modifying one record):
records=20 inserted=0 updated=1 unchanged=19

Verified that:
- New records are inserted.
- Existing unchanged records are skipped.
- Modified records are updated.
- SHA-256 fingerprints detect record changes.
- The loader uses a transaction.

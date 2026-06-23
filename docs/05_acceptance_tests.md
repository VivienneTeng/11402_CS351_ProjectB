# 05. Acceptance Tests (驗收測試案例)

This document lists high-level, user-focused acceptance tests and describes how to run them manually or automate them in CI.

General notes:
- Acceptance tests exercise the CLI end-to-end against a temporary `data/` directory and verify both user-visible output and on-disk persistence.
- Automatable via `pytest` using subprocess calls to the CLI or by invoking the CLI entrypoint via `click.testing`/`subprocess`.

### AT-01: Auto-generation of missing data file
- **Pre-condition:** No `data/database.csv` exists in the test directory.
- **Action:** Run `app list` (or `python -m app.main list`) against the test data dir.
- **Expected Result:** CLI prints a message about initializing storage, creates `data/database.csv` with header row, and exits with code 0.
- **Automated check:** Assert file exists and header matches schema; exit code == 0.

### AT-02: Input validation for numeric fields
- **Pre-condition:** Fresh initialized data dir.
- **Action:** Run `app add --title "T" --platform "PC" --price abc` (or call `app` with invalid `--price`).
- **Expected Result:** CLI exits with non-zero code or prints a clear validation error and refuses to write the record.
- **Automated check:** Assert no new record appended and stderr contains validation message.

### AT-03: Delete non-existent ID handling
- **Pre-condition:** Store with some records present.
- **Action:** Run `app delete --id 99999 --force`.
- **Expected Result:** CLI prints "Record not found" (or similar), returns non-zero exit code, and leaves existing data unchanged.
- **Automated check:** Compare pre/post data file contents are identical.

### AT-04: Full CRUD flow (happy path)
- **Pre-condition:** Empty data dir.
- **Action:**
	1. `app add --title "G1" --platform PC --price 0`
	2. `app list` (verify record present)
	3. `app show --id 1` (verify fields)
	4. `app update --id 1 --status playing`
	5. `app delete --id 1 --force`
- **Expected Result:** Each step returns appropriate exit codes; after deletion, `list` shows no records.
- **Automated check:** Assert state after each step matches expectation and final data file contains zero user records.

### AT-05: Atomic write resilience
- **Pre-condition:** data file exists with known content.
- **Action:** Simulate a write failure (test harness monkeypatches `os.replace` to raise) while performing `app update`.
- **Expected Result:** Original file remains unchanged (or a valid backup exists); CLI reports failure and exits non-zero.
- **Automated check:** Assert file checksum unchanged or backup file present.

### AT-06: Export/Import roundtrip
- **Pre-condition:** Store with multiple records.
- **Action:** `app export --format json backup.json` then remove `data/database.csv` and `app import --file backup.json`.
- **Expected Result:** After import, `list` shows the same set of records as before export.
- **Automated check:** Compare record counts and a sample of fields for equality.

## Running acceptance tests

Manual quick checks (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
pytest tests/acceptance -q
```

Or run a single acceptance script using `pytest` or a helper shell script. Acceptance tests should use temporary directories and not modify the repository `data/`.

## Automating in CI
- Add a GitHub Actions job `acceptance-tests` that runs after unit tests, using a matrix for `windows-latest` and `ubuntu-latest`.
- Ensure the job installs dependencies and runs `pytest tests/acceptance`.

## Test Artifacts
- Store JSON export files and any failing CLI stdout/stderr logs as job artifacts for debugging failing acceptance runs.

This file defines concise, automatable acceptance tests to prove the system satisfies the user-facing SRS requirements.
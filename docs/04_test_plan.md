# 04. Test Plan (Verification)

This test plan maps each SRS requirement to one or more verifiable tests (unit, integration, or acceptance), describes environment setup, and shows how to run tests locally and in CI.

## 1. Test Types
- **Unit tests:** Fast, isolated tests for `core/service.py` logic using mocks for `storage`.
- **Integration tests:** End-to-end tests using the real `storage` implementation against a temporary data directory.
- **Acceptance tests / Smoke:** High-level CLI invocations to verify user-visible workflows (add/list/update/delete/export).

## 2. Test Environment
- Python 3.10+ virtual environment.
- Test runner: `pytest`.
- Test fixtures use temporary directories (`tmp_path` / `tmp_path_factory`) and do not modify the repository `data/` directory.
- Sample test resources live under `tests/fixtures/` (e.g., small CSV examples).

## 3. Requirement → Test Mapping (representative)

- **FR-1 (Data Initialization)** — Integration test `tests/test_storage_init.py`:
	- Steps: remove any `data/database.csv` in temp dir, call storage.init(path), assert file exists and header row matches schema.
	- Type: Integration

- **FR-2 (Load on Startup)** — Integration `tests/test_load_on_startup.py`:
	- Steps: create CSV with 3 records, start app service load, assert in-memory count == 3.
	- Type: Integration

- **FR-3 (List & Display)** — Acceptance `tests/test_cli_list.py`:
	- Steps: create known dataset, run `app list` via `subprocess` or `click` runner, assert output contains headers and rows aligned.
	- Type: Acceptance

- **FR-4 (Query)** — Unit+Integration `tests/test_query.py`:
	- Steps: run `service.query()` with filters and assert returned records match expectations; acceptance test executes `app query` CLI.
	- Type: Unit & Integration

- **FR-5 / FR-6 / FR-7 (Create/Read/Update/Delete by ID)** — End-to-end `tests/test_crud_flow.py`:
	- Steps: add record, verify `list` shows id; `show --id` returns fields; `update --id` changes field; `delete --id --force` removes record; after each operation, reload storage and assert persisted state.
	- Type: Integration / Acceptance

- **FR-9 (Atomic Persistence)** — Integration `tests/test_atomic_write.py`:
	- Steps: simulate a failure during write (monkeypatch `os.replace` or raise in write path), assert original `data/database.csv` remains unchanged and backup preserved.
	- Type: Integration

- **FR-10 / FR-11 (Import/Export, Backup/Restore)** — Integration `tests/test_import_export_backup.py`:
	- Steps: export to JSON, clear store, import JSON, assert records restored; take backup, delete file, restore from backup.
	- Type: Integration

- **NFR-1..NFR-7 (Non-functional)** — Mixed tests:
	- Compatibility: run core tests on Windows/Linux in CI matrix.
	- Performance (NFR-2): synthetic dataset generator test `tests/bench/` to measure `list` latency with 10k records (acceptance threshold: sub-second listing on CI runner is optional — document locally measured times).
	- Validation (NFR-5): unit tests for input validators rejecting bad numeric/text fields.

## 4. Example Test Cases (detailed)
- Test: `test_add_assigns_id`
	- Given empty store
	- When `service.add(title="T", platform="PC", price=0)`
	- Then returned id == 1 and persisted file contains id 1

- Test: `test_update_preserves_other_fields`
	- Given record with id 2
	- When `service.update(2, {"status":"completed"})`
	- Then only `status` changed after reload

## 5. Running Tests Locally

Create and activate virtualenv, install dev dependencies, and run pytest:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
pytest -q
```

Or on Unix/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -q
```

`requirements-dev.txt` should include `pytest` and any test utilities (e.g., `pytest-mock`).

## 6. CI Integration (GitHub Actions suggestion)

- Run tests on each PR with a matrix for `ubuntu-latest` and `windows-latest` and Python 3.10.
- Use a job that installs dev requirements and runs `pytest -q`.

## 7. Test Data & Fixtures

- Keep small, deterministic CSV fixtures in `tests/fixtures/` and generate larger synthetic datasets for performance tests under `tests/bench/`.

## 8. Acceptance Criteria

- Each FR in `docs/02_SRS.md` must have at least one passing automated test in `tests/`.
- Integration tests exercising persistence must run in CI and pass on both Windows and Linux runners.

## 9. Next Steps

- Implement test skeletons for the highest-priority FRs (init, add/list, CRUD, atomic write) so developers can run and verify during implementation.

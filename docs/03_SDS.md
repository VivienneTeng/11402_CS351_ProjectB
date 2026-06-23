# 03. Software Design Specification (SDS)

This document describes the internal organization of the system: module boundaries, data model, storage patterns, command flows, and test hooks.

## 1. High-level Architecture

The system follows a small, layered architecture with clear separation of concerns:

- **CLI Layer (`cli/`):** Parses command-line arguments, validates user input, and formats output for the terminal.
- **Application / Orchestration (`app/main.py`):** Implements command dispatch, coordinates use-cases, and invokes the engine.
- **Domain / Business Logic (`core/`):** Contains the `model` (domain types), `service` (CRUD operations, query engine), and `validation` modules.
- **Storage Layer (`storage/`):** Responsible for persistent data access (CSV/JSON), atomic writes (write-to-temp + rename), import/export, and backup/restore.
- **Tests (`tests/`):** Unit and integration tests that exercise core logic and storage invariants.

Physical files (suggested):

- `app/main.py` — entrypoint and CLI wiring
- `cli/args.py` — argument parsing and help text
- `core/model.py` — `GameRecord` dataclass and schema
- `core/service.py` — functions: list, query, add, show, update, delete
- `storage/csv_store.py` — CSV read/write, atomic persistence
- `storage/backup.py` — snapshot and restore utilities
- `tests/test_service.py`, `tests/test_storage.py`

## 2. Data Model

Representative domain type (Python dataclass):

- `GameRecord` fields:
	- `id: int` (auto-increment primary key)
	- `title: str`
	- `platform: str`
	- `genre: Optional[str]`
	- `price: float`
	- `playtime_hours: float`
	- `status: Enum['backlog','playing','completed','dropped']`
	- `tags: List[str]`

Internally the service keeps:

- `records_by_id: dict[int, GameRecord]` — O(1) lookup for CRUD operations
- `next_id: int` — persisted incrementing counter stored with the data file or derived from max existing id on load

## 3. Storage Schema & Persistence

- Default on-disk format: CSV with header row (fields ordered as in `GameRecord`). JSON export/import supported as optional format.
- Persistence must be atomic: write updates to a temporary file then rename into place (POSIX/Windows safe pattern), and optionally create a timestamped backup before destructive operations.
- On startup: attempt to load `data/database.csv`; if missing or malformed, create a new header-only CSV and set `next_id = 1`.

## 4. Command Flow (example sequences)

- Add record:
	1. CLI parses `add` args and validates types.
	2. `service.add()` creates `GameRecord` with `id = next_id`, increments `next_id` in memory.
	3. `storage` persists using atomic write; on success, return created id.

- Update record:
	1. CLI parses `update --id N --field X` and validates.
	2. `service.update(id, changes)` mutates in-memory record.
	3. `storage` persists atomically; partial failures should roll back in-memory change or restore from backup.

- Delete record:
	1. Confirm user intent (unless `--force`).
	2. Remove from `records_by_id` and persist atomically.

## 5. Error Handling & Logging

- Failures in parsing or user validation must return clear, actionable CLI messages and non-zero exit codes.
- Storage I/O errors must be logged and surfaced as safe messages; where possible, preserve the previous data file (do not overwrite on error).
- Use structured logging at `INFO` for normal operations and `ERROR` for unexpected failures; enable `DEBUG` in developer mode.

## 6. Concurrency & Consistency

- The system is single-user and single-process; no file locking beyond atomic rename is required for the course scope. If run concurrently, last-writer-wins behavior applies; document this as a limitation.

## 7. Testing & Validation Hooks

- Unit tests for `core/service.py` should mock `storage` to verify business logic without disk I/O.
- Integration tests should use a temporary data directory and verify persistence, atomicity, and startup behaviors.

## 8. Dependencies & Tooling

- Minimal external dependencies: use standard library where possible (`csv`, `json`, `argparse`, `tempfile`, `logging`).
- Use `pytest` for tests and a simple `tox` or GitHub Actions workflow to run tests on PRs.

## 9. Directory Layout (recommended)

```
./
├─ app/
│  └─ main.py
├─ cli/
│  └─ args.py
├─ core/
│  ├─ model.py
│  └─ service.py
├─ storage/
│  ├─ csv_store.py
│  └─ backup.py
├─ data/
│  └─ database.csv
├─ tests/
└─ docs/
```

This SDS provides a practical, testable internal organization so the team can implement modules in parallel and validate key storage and business invariants.


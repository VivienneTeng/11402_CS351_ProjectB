# 02. Software Requirements Specification (SRS)

This SRS lists the requirements the system must satisfy. Requirements are written as testable statements (MUST/SHOULD/MAY) and include acceptance criteria where applicable.

## 1. Functional Requirements (FR)

- **FR-1 (Data Initialization):** On first run or when `data/database.csv` is missing or corrupt, the system MUST create a valid, empty data file with correct header schema and resetable primary-key state.
	- Acceptance: Running the app in an empty repo creates `data/database.csv` with header row and no records.

- **FR-2 (Load on Startup):** The system MUST load existing records from `data/database.csv` into an in-memory index on startup.
	- Acceptance: After startup, in-memory count equals number of CSV records.

- **FR-3 (List & Display):** The system MUST present stored records in a human-readable aligned table in the terminal when the user issues a `list` command.
	- Acceptance: `list` prints column headers and fixed-width rows; no raw CSV escapes appear.

- **FR-4 (Query):** The system MUST support querying records using keyword matching across defined attributes (title, platform, status, tags) with filters and basic Boolean/substring semantics.
	- Acceptance: `query --title "Zelda" --status backlog` returns only matching rows.

- **FR-5 (Create/Append):** The system MUST allow adding new records with required fields; the storage MUST assign an auto-incrementing unique ID per record.
	- Acceptance: New record appears in `list` with an ID greater than previous max.

- **FR-6 (Read by ID):** The system MUST retrieve a single record by ID and present full field details.
	- Acceptance: `show --id 42` outputs all fields for record 42 or a clear 'not found' message.

- **FR-7 (Update by ID):** The system MUST update one or more fields of an existing record identified by ID while preserving other fields.
	- Acceptance: `update --id 42 --status completed` changes only `status` for ID 42.

- **FR-8 (Delete by ID):** The system MUST delete records by ID after explicit user confirmation (interactive or `--force` flag).
	- Acceptance: `delete --id 42` prompts; `delete --id 42 --force` removes without prompt and record no longer appears.

- **FR-9 (Atomic Persistence):** All create/update/delete operations MUST be persisted atomically to local storage to avoid partial writes (e.g., write-to-temp + rename pattern).
	- Acceptance: Interrupted write never leaves `data/database.csv` in a corrupted, partially-written state.

- **FR-10 (Import/Export):** The system SHOULD support importing from and exporting to common formats (CSV, JSON) for backup and migration.
	- Acceptance: `export --format json path` writes a valid JSON file matching in-memory records.

- **FR-11 (Backup & Restore):** The system SHOULD provide a simple backup command that snapshots the current data file and a restore command to revert to a snapshot.

- **FR-12 (Help & CLI):** The system MUST offer a `--help` or `help` command documenting available commands, arguments, and examples.

## 2. Non-Functional Requirements (NFR)

- **NFR-1 (Platform Compatibility):** The application MUST run on Python 3.10+ and be cross-platform (Windows, macOS, Linux). Build or runtime scripts should not assume platform-specific paths.

- **NFR-2 (Performance & Scale):** The system MUST perform interactive list/query/update operations with acceptable latency for up to 10,000 records (sub-second listing for typical desktop hardware).

- **NFR-3 (Reliability):** The system MUST avoid data loss under normal operation; operations should be transactional on disk with recoverable backups.

- **NFR-4 (Usability):** CLI output MUST be clear and readable; error messages MUST describe the problem and corrective action.

- **NFR-5 (Validation & Robustness):** Inputs must be validated (e.g., numeric fields only accept numbers). Invalid inputs MUST produce descriptive errors and not crash the application.

- **NFR-6 (Security & Privacy):** User data MUST remain local by default. The system MUST not transmit telemetry or user data externally.

- **NFR-7 (Maintainability):** Code SHOULD be modular with separation between storage, business logic, and CLI presentation to enable testing.

## 3. Constraints and Assumptions

- Single-user local application; no multi-user concurrency or network service required.
- Storage format is plain-text CSV (or JSON as optional export/import). Users are responsible for off-site backups.
- Target dataset size is personal-scale (ideally < 10,000 items).

## 4. Acceptance Criteria & Testability

- Each FR must map to one or more automated unit/integration tests (e.g., start with empty data file, perform create/update/delete, verify persisted state).
- CI must run tests for core FRs on each PR.

## 5. Example CLI Commands (for verification)

- `app list`
- `app query --title "Halo" --tag co-op`
- `app add --title "New Game" --platform PC --status backlog --price 0`
- `app show --id 5`
- `app update --id 5 --status playing`
- `app delete --id 5 --force`
- `app export --format json backup.json`

This SRS focuses on verifiable, minimal requirements for a small, local game-record CLI tool while leaving room for optional features (import/export, backups) to be implemented incrementally.
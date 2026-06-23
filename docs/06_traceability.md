# 06. Requirement Traceability Matrix (RTM - 需求追蹤矩陣)

This RTM maps each requirement from `docs/02_SRS.md` to the design artifacts in `docs/03_SDS.md` and to concrete tests (unit/integration/acceptance) described in `docs/04_test_plan.md` and `docs/05_acceptance_tests.md`.

Notes:
- Design targets point to modules/files where the requirement is implemented or enforced.
- Verification points list recommended test files or acceptance test IDs to prove the requirement.

| Requirement ID | Design Module(s) (SDS) | Verification (tests / acceptance) |
| :--- | :--- | :--- |
| **FR-1 (Data Initialization & Load)** | `storage/csv_store.py` (`init()`, `load()`) and `core/service.py` (startup orchestration) | `tests/test_storage_init.py` (integration), `AT-01` in `docs/05_acceptance_tests.md` |
| **FR-2 (List & Display)** | `core/service.py` (`list()`), `cli/output_formatter.py` | `tests/test_cli_list.py` (acceptance), `tests/test_service_list.py` (unit) |
| **FR-3 (Query)** | `core/service.py` (`query()`), `core/model.py` (searchable fields) | `tests/test_query.py` (unit/integration) |
| **FR-4 (Create/Append)** | `core/service.py` (`add()`), `storage/csv_store.py` (append + atomic persist) | `tests/test_crud_flow.py` (integration), `tests/test_add_assigns_id.py` (unit) |
| **FR-5 (Read by ID)** | `core/service.py` (`show()`), `core/model.py` | `tests/test_read_by_id.py` (unit/integration) |
| **FR-6 (Update by ID)** | `core/service.py` (`update()`), `storage/csv_store.py` (atomic write) | `tests/test_crud_flow.py`, `tests/test_update_preserves_other_fields.py` |
| **FR-7 (Delete by ID)** | `core/service.py` (`delete()`), `storage/backup.py` (optional snapshot) | `tests/test_crud_flow.py`, `AT-03` (acceptance) |
| **FR-8 (Atomic Persistence)** | `storage/csv_store.py` (write-to-temp + rename), `storage/backup.py` | `tests/test_atomic_write.py` (integration), `AT-05` (acceptance) |
| **FR-9 (Import/Export)** | `storage/csv_store.py` (CSV), `storage/json_store.py` (export/import) | `tests/test_import_export_backup.py` (integration), `AT-06` (acceptance) |
| **FR-10 (Backup & Restore)** | `storage/backup.py` | `tests/test_import_export_backup.py` (integration) |
| **FR-11 (Help & CLI)** | `cli/args.py`, `app/main.py` | `tests/test_cli_help.py` (unit/acceptance) |
| **NFR-1 (Platform Compatibility)** | Cross-cutting: use stdlib modules in `storage/` and `core/` | CI matrix: GitHub Actions `windows-latest` & `ubuntu-latest` runs (`pytest`) |
| **NFR-2 (Performance / Scale)** | `core/service.py` (efficient in-memory dicts), `storage/csv_store.py` (streamed IO) | `tests/bench/test_list_performance.py` (benchmark); measure with synthetic 10k dataset |
| **NFR-3 (Reliability)** | `storage/csv_store.py`, `storage/backup.py`, `core/service.py` | `tests/test_atomic_write.py`, integration backup/restore tests |
| **NFR-4 (Usability / UX)** | `cli/output_formatter.py`, `cli/args.py` | Acceptance tests: `tests/test_cli_list.py`, manual review |
| **NFR-5 (Validation & Robustness)** | `cli/args.py`, `core/validation.py` | `tests/test_validation.py`, `AT-02` (acceptance) |
| **NFR-6 (Security & Privacy)** | Design decision: local-only storage; no network modules | Policy: code review checklist; tests ensure no external calls in `storage` (unit tests mocking network) |
| **NFR-7 (Maintainability)** | Project structure: `core/`, `storage/`, `cli/`, tests coverage | Code coverage checks in CI; unit tests for core modules |

## How to use this RTM

- When implementing a requirement, update the corresponding module(s) listed above and add/modify the referenced test(s).
- When tests are added, mark the requirement as verified in this document and in the issue tracker by linking PR → issue → test run.

This RTM ties `docs/02_SRS.md` requirements to concrete design locations and test artifacts so every requirement is traceable from spec to code to verification.
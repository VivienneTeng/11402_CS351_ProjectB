# 08. Known Issues & Limitations

## 1. Concurrency Bottleneck
* **Description:** Because the file storage relies on standard synchronous text flat-file overwrites, concurrent data transactions across separate runtime terminals will conflict and result in mutual data overwrites.
* **Mitigation:** Intended only as a local desktop standalone storage node. Real-world upgrades would require a process file-locking model (`fcntl` / `msvcrt`).

## 2. Scaling Latency
* **Description:** For database sizes larger than 50,000 items, serializing the whole in-memory hash map into text formatting strings during save phases creates a measurable lag.
* **Mitigation:** Future upgrades should decouple memory writes into localized streaming chunk appends or interface directly with SQLite.
 
## 3. No Network or Multi-user Support (Design Limitation)
* **Description:** The system intentionally omits networking, authentication, and multi-user features to remain minimal and local-only.
* **Impact:** Cannot be used as a collaborative or remote service; no remote backups by default.
* **Workaround:** Users must manage backups manually (export/import) or use filesystem-level sync (OneDrive/Dropbox) with care.

## 4. Partial Write / Crash Window
* **Description:** While atomic write (temp file + rename) is implemented, abrupt process termination between steps or platform-specific rename failures could still create edge-case corruption.
* **Mitigation:** Test coverage includes atomic-write tests; recommend periodic backups and keeping backups in `data/backups/`.

## 5. Limited Input Validation Coverage
* **Description:** Current validators cover major numeric/text fields but may not validate complex tag formats, long strings, or malformed CSV edge cases.
* **Risks:** Malformed input could lead to display glitches or import failures.
* **Mitigation:** Add more unit tests for validation and sanitize fields on import; reject rows failing schema checks.

## 6. Deferred / Planned Enhancements
* **Feature: Concurrency-safe locking:** Deferred — requires cross-platform file locking design and tests.
* **Feature: Optional SQLite backend:** Deferred — would address scale and transactional guarantees.
* **Feature: GUI front-end:** Deferred — out of scope for current deliverable; could be added as optional module.

## 7. Security & Privacy Notes
* **Design:** Data remains local by default; there is no telemetry. If users add sync or remote export, they should ensure backups are stored securely.

## 8. Recommended Short-term Actions
* Add automated backups before destructive operations (update/delete).
* Harden validation and CSV import to reject malformed records.
* Add a small `data/backups/` rotation policy (retain last N snapshots).

These known issues capture current limitations and proposed mitigations; they should be revisited as features are implemented or the architecture evolves.
import os
import shutil
from datetime import datetime


class BackupError(Exception):
    pass


class BackupManager:
    """提供資料檔案快照與還原機制。"""

    def __init__(self, source_file: str, backup_dir: str = 'data/backups'):
        self.source_file = source_file
        self.backup_dir = backup_dir
        os.makedirs(self.backup_dir, exist_ok=True)

    def create_snapshot(self) -> str:
        """建立資料檔案的快照回存備份，回傳備份檔案路徑。"""
        if not os.path.exists(self.source_file):
            raise BackupError(f"Source file does not exist: {self.source_file}")

        timestamp = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
        backup_name = f"backup-{timestamp}.csv"
        backup_path = os.path.join(self.backup_dir, backup_name)

        try:
            shutil.copy2(self.source_file, backup_path)
        except OSError as exc:
            raise BackupError(f"Failed to create backup: {exc}") from exc

        return backup_path

    def list_snapshots(self) -> list[str]:
        """列出可用的備份快照，依時間排序。"""
        entries = []
        for entry in os.listdir(self.backup_dir):
            if entry.startswith('backup-') and entry.endswith('.csv'):
                entries.append(entry)
        return sorted(entries)

    def restore_snapshot(self, snapshot_name: str) -> None:
        """使用已有快照還原到來源檔案。"""
        snapshot_path = os.path.join(self.backup_dir, snapshot_name)
        if not os.path.exists(snapshot_path):
            raise BackupError(f"Snapshot does not exist: {snapshot_path}")

        try:
            shutil.copy2(snapshot_path, self.source_file)
        except OSError as exc:
            raise BackupError(f"Failed to restore backup: {exc}") from exc

    def rotate_snapshots(self, retain: int = 5) -> None:
        """保留最新 N 個快照，其餘刪除。"""
        snapshots = self.list_snapshots()
        obsolete = snapshots[:-retain]
        for entry in obsolete:
            try:
                os.remove(os.path.join(self.backup_dir, entry))
            except OSError:
                pass

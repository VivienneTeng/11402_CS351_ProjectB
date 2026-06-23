# tests/test_game_app.py
import pytest
import os
from storage.csv_store import CSVStore
from core.service import GameService, ValidationError

# 設定測試用的暫存資料庫路徑
TEST_DB = "data/test_db.csv"

@pytest.fixture
def service():
    """建立一個乾淨的測試服務實例"""
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    storage = CSVStore(TEST_DB)
    return GameService(storage)

def test_add_record(service):
    """測試新增紀錄與自動 ID 分配"""
    record = service.add_record("Test Game", "RPG", 10.0, 5.0, "backlog")
    assert record.id == 1
    assert record.title == "Test Game"

def test_add_invalid_price(service):
    """測試錯誤資料防呆 (NFR-5)"""
    with pytest.raises(ValidationError):
        service.add_record("Bad Game", "Action", -10.0, 5.0, "backlog")

def test_query_records(service):
    """測試搜尋篩選邏輯"""
    service.add_record("Zelda", "Adventure", 60.0, 40.0, "playing")
    service.add_record("Mario", "Platformer", 60.0, 10.0, "backlog")
    
    results = service.query_records(genre="Adventure")
    assert len(results) == 1
    assert results[0].title == "Zelda"

def test_backup_and_restore(service):
    """測試備份與還原機制"""
    from storage.backup import BackupManager
    service.add_record("Backup Test", "RPG", 0.0, 0.0, "backlog")
    
    backup_mgr = BackupManager(TEST_DB, backup_dir="data/backups")
    snapshot = backup_mgr.create_snapshot()
    
    assert os.path.exists(snapshot)
    
    # 刪除紀錄並還原
    service.delete_record(1)
    backup_mgr.restore_snapshot(os.path.basename(snapshot))
    service.reload()
    
    assert 1 in service.records
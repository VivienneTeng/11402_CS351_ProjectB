from __future__ import annotations

from typing import Dict, List, Optional

from core.model import GameRecord
from core.validation import (
    validate_non_negative_float,
    validate_required_text,
    validate_status,
)
from storage.csv_store import CSVStore


class RecordNotFoundError(Exception):
    pass


class ValidationError(Exception):
    pass


class GameService:
    """核心業務服務：管理遊戲紀錄的 CRUD 與查詢邏輯。"""

    def __init__(self, storage: CSVStore):
        self.storage = storage
        self.records: Dict[int, GameRecord] = self.storage.load_all()
        self.next_id = self._compute_next_id()

    def _compute_next_id(self) -> int:
        if not self.records:
            return 1
        return max(self.records.keys()) + 1

    def reload(self) -> None:
        """重新從儲存層讀取最新資料。"""
        self.records = self.storage.load_all()
        self.next_id = self._compute_next_id()

    def list_records(self) -> List[GameRecord]:
        """回傳所有紀錄，依 ID 由小到大排序。"""
        return [self.records[key] for key in sorted(self.records.keys())]

    def query_records(
        self,
        title: Optional[str] = None,
        genre: Optional[str] = None,
        status: Optional[str] = None,
        keyword: Optional[str] = None,
    ) -> List[GameRecord]:
        """依條件查詢紀錄，關鍵字會匹配多個文字欄位。"""
        predicate = self._make_query_predicate(title, genre, status, keyword)
        return [record for record in self.records.values() if predicate(record)]

    def _make_query_predicate(
        self,
        title: Optional[str],
        genre: Optional[str],
        status: Optional[str],
        keyword: Optional[str],
    ):
        title = title.strip().lower() if title else None
        genre = genre.strip().lower() if genre else None
        status = status.strip().lower() if status else None
        keyword = keyword.strip().lower() if keyword else None

        def match(record: GameRecord) -> bool:
            if title and title not in record.title.lower():
                return False
            if genre and genre not in record.genre.lower():
                return False
            if status and status != record.status.lower():
                return False
            if keyword:
                text = " ".join([
                    record.title,
                    record.genre,
                    record.status,
                ]).lower()
                if keyword not in text:
                    return False
            return True

        return match

    def get_record(self, record_id: int) -> GameRecord:
        """根據 ID 取得單筆紀錄，若不存在則拋出錯誤。"""
        record = self.records.get(record_id)
        if record is None:
            raise RecordNotFoundError(f"Record with id {record_id} not found.")
        return record

    def add_record(
        self,
        title: str,
        genre: str,
        price: float,
        playtime: float,
        status: str,
    ) -> GameRecord:
        """新增一筆紀錄並儲存到磁碟。"""
        self._validate_fields(title=title, genre=genre, price=price, playtime=playtime, status=status)

        record = GameRecord(
            id=self.next_id,
            title=title.strip(),
            genre=genre.strip(),
            price=float(price),
            playtime=float(playtime),
            status=status.strip(),
        )
        self.records[record.id] = record
        self.next_id += 1
        self._persist()
        return record

    def update_record(self, record_id: int, **updates) -> GameRecord:
        """更新指定 ID 的欄位，僅變更傳入的欄位。"""
        record = self.get_record(record_id)
        new_data = {
            'id': record.id,
            'title': record.title,
            'genre': record.genre,
            'price': record.price,
            'playtime': record.playtime,
            'status': record.status,
        }

        allowed = {'title', 'genre', 'price', 'playtime', 'status'}
        for key, value in updates.items():
            if key not in allowed:
                continue
            if value is not None:
                new_data[key] = value

        self._validate_fields(
            title=new_data['title'],
            genre=new_data['genre'],
            price=new_data['price'],
            playtime=new_data['playtime'],
            status=new_data['status'],
        )

        updated = GameRecord.from_dict(new_data)
        self.records[record_id] = updated
        self._persist()
        return updated

    def delete_record(self, record_id: int) -> None:
        """刪除指定 ID 的紀錄，找不到時拋出錯誤。"""
        if record_id not in self.records:
            raise RecordNotFoundError(f"Record with id {record_id} not found.")
        del self.records[record_id]
        self._persist()

    def _validate_fields(
        self,
        title: str,
        genre: str,
        price: float,
        playtime: float,
        status: str,
    ) -> None:
        try:
            self.title = validate_required_text('Title', title)
            self.genre = validate_required_text('Genre', genre)
            self.price = validate_non_negative_float('Price', price)
            self.playtime = validate_non_negative_float('Playtime', playtime)
            self.status = validate_status(status)
        except ValueError as exc:
            raise ValidationError(str(exc)) from exc

    def _persist(self) -> None:
        """將目前記憶體資料持久化到儲存層。"""
        self.storage.save_all(self.records)

# storage/csv_store.py
import os
import csv
from core.model import GameRecord

class CSVStore:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.headers = ['id', 'title', 'genre', 'price', 'playtime', 'status']
        self._init_storage()

    def _init_storage(self):
        """FR-1: 如果 CSV 檔案不存在，自動初始化防呆"""
        if not os.path.exists(self.file_path):
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            with open(self.file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(self.headers)

    def load_all(self) -> dict[int, GameRecord]:
        """FR-2 & NFR-2: 載入 CSV 到記憶體中的 Hash Map Index"""
        records = {}
        if not os.path.exists(self.file_path):
            return records
            
        with open(self.file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    game = GameRecord.from_dict(row)
                    records[game.id] = game
                except ValueError:
                    continue  # 跳過損毀的資料列
        return records

    def save_all(self, records: dict[int, GameRecord]):
        """FR-7: 將記憶體中的修改一次性事務寫回硬碟"""
        with open(self.file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(self.headers)
            for game in records.values():
                writer.writerow(game.to_csv_row())
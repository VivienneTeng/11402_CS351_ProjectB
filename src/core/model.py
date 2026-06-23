# core/model.py
from dataclasses import dataclass

@dataclass
class GameRecord:
    id: int
    title: str
    genre: str
    price: float
    playtime: float
    status: str

    @classmethod
    def from_dict(cls, data: dict):
        """從字典建立物件，並進行嚴格的型態防呆與驗證 (NFR-1, NFR-5)"""
        try:
            return cls(
                id=int(data['id']),
                title=str(data['title']).strip(),
                genre=str(data['genre']).strip(),
                price=float(data['price']),
                playtime=float(data['playtime']),
                status=str(data['status']).strip()
            )
        except (ValueError, TypeError) as e:
            raise ValueError(f"Data type validation failed: {e}")

    def to_csv_row(self) -> list:
        """轉換為 CSV 寫入格式"""
        return [self.id, self.title, self.genre, self.price, self.playtime, self.status]
import csv
import os
import tempfile

from core.model import GameRecord
from storage.csv_store import CSVStore


def test_init_storage_creates_file_with_header():
    with tempfile.TemporaryDirectory() as tempdir:
        csv_path = os.path.join(tempdir, 'database.csv')
        store = CSVStore(csv_path)

        assert os.path.exists(csv_path)
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
        assert header == ['id', 'title', 'genre', 'price', 'playtime', 'status']


def test_save_and_load_all_roundtrip():
    with tempfile.TemporaryDirectory() as tempdir:
        csv_path = os.path.join(tempdir, 'database.csv')
        store = CSVStore(csv_path)

        records = {
            1: GameRecord(id=1, title='Record One', genre='Action', price=9.99, playtime=4.5, status='backlog'),
            2: GameRecord(id=2, title='Record Two', genre='RPG', price=19.99, playtime=20.0, status='playing'),
        }
        store.save_all(records)

        loaded = store.load_all()
        assert len(loaded) == 2
        assert loaded[1].title == 'Record One'
        assert loaded[2].status == 'playing'


def test_load_all_skips_invalid_rows():
    with tempfile.TemporaryDirectory() as tempdir:
        csv_path = os.path.join(tempdir, 'database.csv')
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'title', 'genre', 'price', 'playtime', 'status'])
            writer.writerow(['1', 'Good Game', 'Puzzle', '9.99', '5', 'backlog'])
            writer.writerow(['bad', 'Bad Row', 'Arcade', 'x', 'y', 'playing'])

        store = CSVStore(csv_path)
        loaded = store.load_all()

        assert len(loaded) == 1
        assert 1 in loaded
        assert loaded[1].genre == 'Puzzle'


def test_save_all_overwrites_previous_content():
    with tempfile.TemporaryDirectory() as tempdir:
        csv_path = os.path.join(tempdir, 'database.csv')
        store = CSVStore(csv_path)
        initial = {
            1: GameRecord(id=1, title='First', genre='Action', price=5.0, playtime=1.0, status='backlog')
        }
        store.save_all(initial)

        updated = {
            1: GameRecord(id=1, title='First', genre='Action', price=5.0, playtime=1.0, status='completed'),
            2: GameRecord(id=2, title='Second', genre='Strategy', price=15.0, playtime=10.0, status='playing')
        }
        store.save_all(updated)

        loaded = store.load_all()
        assert len(loaded) == 2
        assert loaded[1].status == 'completed'
        assert loaded[2].title == 'Second'

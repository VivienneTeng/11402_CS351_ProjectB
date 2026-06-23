import os
import tempfile

from core.model import GameRecord
from core.service import GameService, RecordNotFoundError, ValidationError
from storage.csv_store import CSVStore


def test_add_and_get_record():
    with tempfile.TemporaryDirectory() as tempdir:
        csv_path = os.path.join(tempdir, 'database.csv')
        storage = CSVStore(csv_path)
        service = GameService(storage)

        record = service.add_record(
            title='Test Game',
            genre='Adventure',
            price=19.99,
            playtime=12.5,
            status='backlog',
        )

        assert record.id == 1
        assert record.title == 'Test Game'

        loaded = service.get_record(1)
        assert loaded.title == 'Test Game'
        assert loaded.price == 19.99


def test_update_record_preserves_other_fields():
    with tempfile.TemporaryDirectory() as tempdir:
        csv_path = os.path.join(tempdir, 'database.csv')
        storage = CSVStore(csv_path)
        service = GameService(storage)

        service.add_record('Test Game', 'Adventure', 19.99, 12.5, 'backlog')
        updated = service.update_record(1, status='completed')

        assert updated.id == 1
        assert updated.status == 'completed'
        assert updated.genre == 'Adventure'
        assert updated.price == 19.99


def test_delete_record_removes_entry():
    with tempfile.TemporaryDirectory() as tempdir:
        csv_path = os.path.join(tempdir, 'database.csv')
        storage = CSVStore(csv_path)
        service = GameService(storage)

        service.add_record('Test Game', 'Adventure', 19.99, 12.5, 'backlog')
        service.delete_record(1)

        try:
            service.get_record(1)
            assert False, 'Expected RecordNotFoundError'
        except RecordNotFoundError:
            pass


def test_invalid_price_raises_validation_error():
    with tempfile.TemporaryDirectory() as tempdir:
        csv_path = os.path.join(tempdir, 'database.csv')
        storage = CSVStore(csv_path)
        service = GameService(storage)

        try:
            service.add_record('Bad Game', 'RPG', 'abc', 5, 'backlog')
            assert False, 'Expected ValidationError'
        except ValidationError as exc:
            assert 'Price must be a numeric value' in str(exc)


def test_list_records_sort_by_id():
    with tempfile.TemporaryDirectory() as tempdir:
        csv_path = os.path.join(tempdir, 'database.csv')
        storage = CSVStore(csv_path)
        service = GameService(storage)

        service.add_record('Game A', 'Action', 10, 2, 'backlog')
        service.add_record('Game B', 'Action', 20, 4, 'playing')
        records = service.list_records()

        assert [record.id for record in records] == [1, 2]

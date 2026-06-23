from __future__ import annotations

import sys
from pathlib import Path

# Ensure `src` directory is importable when running `python src/app/main.py`
ROOT_SRC = Path(__file__).resolve().parents[2]
if str(ROOT_SRC) not in sys.path:
    sys.path.insert(0, str(ROOT_SRC))

from cli.args import build_parser
from cli.output_formatter import format_detail, format_message, format_table
from core.service import GameService, RecordNotFoundError, ValidationError
from storage.csv_store import CSVStore
from storage.backup import BackupManager, BackupError


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    storage_path = args.data

    storage = CSVStore(storage_path)
    service = GameService(storage)
    backup_manager = BackupManager(storage_path)

    try:
        if args.command == 'list':
            records = service.list_records()
            print(format_table(records))

        elif args.command == 'query':
            records = service.query_records(
                title=args.title,
                genre=args.genre,
                status=args.status,
                keyword=args.keyword,
            )
            print(format_table(records))

        elif args.command == 'add':
            record = service.add_record(
                title=args.title,
                genre=args.genre,
                price=args.price,
                playtime=args.playtime,
                status=args.status,
            )
            print(format_message(f"Created record with ID {record.id}"))

        elif args.command == 'show':
            record = service.get_record(args.id)
            print(format_detail(record))

        elif args.command == 'update':
            record = service.update_record(
                args.id,
                title=args.title,
                genre=args.genre,
                price=args.price,
                playtime=args.playtime,
                status=args.status,
            )
            print(format_message(f"Updated record {record.id}."))

        elif args.command == 'delete':
            if not args.force:
                confirm = input(f"Delete record {args.id}? [y/N]: ")
                if confirm.lower() != 'y':
                    print(format_message("Delete cancelled."))
                    return 0
            service.delete_record(args.id)
            print(format_message(f"Deleted record {args.id}."))

        elif args.command == 'export':
            print(format_message("Export command not implemented yet."))
            return 1

        elif args.command == 'import':
            print(format_message("Import command not implemented yet."))
            return 1

        elif args.command == 'backup':
            snapshot_path = backup_manager.create_snapshot()
            backup_manager.rotate_snapshots(retain=args.retain)
            print(format_message(f"Backup created: {snapshot_path}"))

        elif args.command == 'restore':
            backup_manager.restore_snapshot(args.snapshot)
            service.reload()
            print(format_message(f"Restored snapshot {args.snapshot}."))

        else:
            parser.print_help()
            return 1

        return 0

    except RecordNotFoundError as exc:
        print(format_message(str(exc)), file=sys.stderr)
        return 1
    except ValidationError as exc:
        print(format_message(str(exc)), file=sys.stderr)
        return 1
    except BackupError as exc:
        print(format_message(str(exc)), file=sys.stderr)
        return 1
    except Exception as exc:
        print(format_message(f"Unexpected error: {exc}"), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())

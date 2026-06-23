import argparse
from argparse import ArgumentParser


def build_parser() -> ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='game-database',
        description='Personal game collection manager with CSV persistence.',
    )

    parser.add_argument(
        '--data',
        default='data/database.csv',
        help='Path to the CSV database file.',
    )

    subparsers = parser.add_subparsers(dest='command', required=True)

    subparsers.add_parser('list', help='List all stored game records.')

    query_parser = subparsers.add_parser('query', help='Query records by field or keyword.')
    query_parser.add_argument('--title', help='Match title substring.')
    query_parser.add_argument('--genre', help='Match genre substring.')
    query_parser.add_argument('--status', help='Match record status.')
    query_parser.add_argument('--keyword', help='Search across title, genre, status.')

    add_parser = subparsers.add_parser('add', help='Add a new game record.')
    add_parser.add_argument('--title', required=True, help='Game title.')
    add_parser.add_argument('--genre', required=True, help='Game genre.')
    add_parser.add_argument('--price', required=True, help='Game price.')
    add_parser.add_argument('--playtime', required=True, help='Estimated playtime in hours.')
    add_parser.add_argument('--status', required=True, help='Record status (backlog, playing, completed, dropped).')

    show_parser = subparsers.add_parser('show', help='Show a single record by ID.')
    show_parser.add_argument('--id', required=True, type=int, help='Record ID.')

    update_parser = subparsers.add_parser('update', help='Update an existing record by ID.')
    update_parser.add_argument('--id', required=True, type=int, help='Record ID.')
    update_parser.add_argument('--title', help='Game title.')
    update_parser.add_argument('--genre', help='Game genre.')
    update_parser.add_argument('--price', help='Game price.')
    update_parser.add_argument('--playtime', help='Estimated playtime in hours.')
    update_parser.add_argument('--status', help='Record status.')

    delete_parser = subparsers.add_parser('delete', help='Delete a record by ID.')
    delete_parser.add_argument('--id', required=True, type=int, help='Record ID.')
    delete_parser.add_argument('--force', action='store_true', help='Skip confirmation prompt.')

    export_parser = subparsers.add_parser('export', help='Export records to JSON.')
    export_parser.add_argument('--file', required=True, help='Destination export file path.')
    export_parser.add_argument('--format', choices=['json'], default='json', help='Export format.')

    import_parser = subparsers.add_parser('import', help='Import records from JSON.')
    import_parser.add_argument('--file', required=True, help='Source import file path.')
    import_parser.add_argument('--format', choices=['json'], default='json', help='Import format.')

    backup_parser = subparsers.add_parser('backup', help='Create a snapshot backup of the database file.')
    backup_parser.add_argument('--retain', type=int, default=5, help='Number of backups to retain.')

    restore_parser = subparsers.add_parser('restore', help='Restore the database from a backup snapshot.')
    restore_parser.add_argument('--snapshot', required=True, help='Backup snapshot file name to restore.')

    return parser

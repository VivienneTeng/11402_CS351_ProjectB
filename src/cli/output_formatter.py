from __future__ import annotations

from typing import Iterable, List

from core.model import GameRecord


def format_table(records: Iterable[GameRecord]) -> str:
    """將多筆紀錄格式化為固定寬度的表格輸出。"""
    rows = [
        ['ID', 'Title', 'Genre', 'Price', 'Playtime', 'Status'],
    ]
    for record in records:
        rows.append([
            str(record.id),
            record.title,
            record.genre,
            f"{record.price:.2f}",
            f"{record.playtime:.1f}",
            record.status,
        ])

    col_widths = [max(len(str(cell)) for cell in column) for column in zip(*rows)]
    lines: List[str] = []
    header = ' | '.join(str(cell).ljust(width) for cell, width in zip(rows[0], col_widths))
    divider = '-+-'.join('-' * width for width in col_widths)
    lines.append(header)
    lines.append(divider)

    for row in rows[1:]:
        lines.append(' | '.join(str(cell).ljust(width) for cell, width in zip(row, col_widths)))

    return '\n'.join(lines)


def format_detail(record: GameRecord) -> str:
    """格式化單筆紀錄為詳情輸出。"""
    fields = [
        ('ID', record.id),
        ('Title', record.title),
        ('Genre', record.genre),
        ('Price', f"{record.price:.2f}"),
        ('Playtime', f"{record.playtime:.1f}"),
        ('Status', record.status),
    ]
    max_label = max(len(label) for label, _ in fields)
    lines = [f"{label.ljust(max_label)} : {value}" for label, value in fields]
    return '\n'.join(lines)


def format_message(message: str) -> str:
    return message.strip() + '\n'

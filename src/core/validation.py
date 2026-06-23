from __future__ import annotations

from typing import Iterable

VALID_STATUSES = {'backlog', 'playing', 'completed', 'dropped'}


def validate_required_text(field_name: str, value: str) -> str:
    if value is None:
        raise ValueError(f"{field_name} is required.")
    normalized = str(value).strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty.")
    return normalized


def validate_non_negative_float(field_name: str, value) -> float:
    try:
        float_value = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be a numeric value.") from exc
    if float_value < 0:
        raise ValueError(f"{field_name} must not be negative.")
    return float_value


def validate_status(value: str) -> str:
    status = validate_required_text('Status', value).lower()
    if status not in VALID_STATUSES:
        raise ValueError(
            f"Status must be one of: {', '.join(sorted(VALID_STATUSES))}."
        )
    return status


def validate_tags(tags: Iterable[str]) -> list[str]:
    if tags is None:
        return []
    if not isinstance(tags, Iterable) or isinstance(tags, str):
        raise ValueError("Tags must be a list of strings.")
    normalized_tags = []
    for tag in tags:
        tag_text = str(tag).strip()
        if tag_text:
            normalized_tags.append(tag_text)
    return normalized_tags

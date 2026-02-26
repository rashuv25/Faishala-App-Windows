# -*- coding: utf-8 -*-
"""General helper functions."""

from typing import Any, Dict, List
import json


def to_nepali_number(num: int) -> str:
    """Convert integer to Nepali number string."""
    from config.constants import NEPALI_NUMBERS
    return ''.join(NEPALI_NUMBERS.get(d, d) for d in str(num))


def from_nepali_number(nepali_str: str) -> int:
    """Convert Nepali number string to integer."""
    from config.constants import NEPALI_NUMBERS
    reverse_map = {v: k for k, v in NEPALI_NUMBERS.items()}
    english_str = ''.join(reverse_map.get(c, c) for c in nepali_str)
    return int(english_str)


def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def safe_json_loads(json_str: str, default: Any = None) -> Any:
    """Safely load JSON string."""
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return default


def safe_json_dumps(obj: Any) -> str:
    """Safely dump object to JSON string."""
    try:
        return json.dumps(obj, ensure_ascii=False)
    except (TypeError, ValueError):
        return "{}"


def group_by_date(documents: List[Dict]) -> Dict[str, List[Dict]]:
    """Group documents by date."""
    grouped = {}
    for doc in documents:
        date_key = doc.get('nepali_created_date', 'Unknown')
        if date_key not in grouped:
            grouped[date_key] = []
        grouped[date_key].append(doc)
    return grouped
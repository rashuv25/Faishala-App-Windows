# -*- coding: utf-8 -*-
"""Nepali Unicode cleanup utilities."""

from __future__ import annotations
import unicodedata
from typing import Any


# Keep these fixes conservative.
# We only repair patterns we have clear evidence for.
LEGACY_REPLACEMENTS = {
    # Important: this was wrongly mapped to "इ" before.
    # That is why words like "र्इलाका" became "इलाका".
    # The intended Unicode here is "ई".
    "र्इ": "ई",

    # Keep this only if your source data really uses this broken form.
    "र्ी": "ई",

    # These are often seen in malformed legacy-to-Unicode text.
    "र्ु": "उ",
    "र्ू": "ऊ",
    "र्े": "ए",
    "र्ै": "ऐ",
    "र्ो": "ओ",
    "र्ौ": "औ",
}


def sanitize_nepali_text(value: Any) -> str:
    """Normalize and repair common malformed Nepali Unicode text."""
    if value is None:
        return ""

    text = str(value)

    # Normalize first
    text = unicodedata.normalize("NFC", text)

    # Remove accidental BOM
    text = text.replace("\ufeff", "")

    # Apply conservative repairs
    for bad, good in LEGACY_REPLACEMENTS.items():
        text = text.replace(bad, good)

    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    return text


def sanitize_value(value: Any) -> Any:
    """Sanitize strings recursively while preserving non-string types."""
    if isinstance(value, str):
        return sanitize_nepali_text(value)

    if isinstance(value, list):
        return [sanitize_value(v) for v in value]

    if isinstance(value, dict):
        return {k: sanitize_value(v) for k, v in value.items()}

    return value


def sanitize_document_data(data: dict) -> dict:
    """Return a cleaned copy of document data."""
    if not isinstance(data, dict):
        return {}

    return {key: sanitize_value(value) for key, value in data.items()}
"""Kata 1 — Clean messy CSV text into records.

Implement `parse_records` so it turns raw CSV text into a list of dicts.

Rules:
- The first non-blank line is the header.
- Header keys are stripped of surrounding whitespace and lowercased.
- Each value is stripped of surrounding whitespace.
- Skip blank lines (and lines that are only commas/whitespace).
- Each record is a dict mapping header key -> value.

Run `uv run pytest week-01/katas/test_kata1_clean_csv.py` to check.
"""

from __future__ import annotations


def parse_records(raw: str) -> list[dict[str, str]]:
    output = []
    lraw = raw.lstrip()
    cleaned = lraw.replace(" ", "")
    rows = cleaned.split()
    headers = rows[0].lower().split(",")
    for row in rows[1:]:
        parsed_row = row.split(",")
        if any(x != "" for x in parsed_row):
            output.append(dict(zip(headers, parsed_row)))
    return output

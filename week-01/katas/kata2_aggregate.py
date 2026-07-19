"""Kata 2 — Group and aggregate without pandas.

Given rows like {"category": "books", "amount": "12.50"}, implement:

- `total_by_category(rows)` -> dict mapping category -> summed amount (float).
  Amounts arrive as strings; convert them. Categories may repeat.
- `top_categories(rows, n)` -> list of (category, total) tuples, highest total first,
  limited to n. Break ties by category name ascending.

Hint: `collections.defaultdict` keeps this tidy.

Run `uv run pytest week-01/katas/test_kata2_aggregate.py` to check.
"""

from __future__ import annotations
from collections import Counter


def total_by_category(rows: list[dict[str, str]]) -> dict[str, float]:
    output = Counter()
    for row in rows:
        k = row.get("category")
        v = float(row.get(("amount")))
        output.update({k: v})
    return dict(output)


def top_categories(rows: list[dict[str, str]], n: int) -> list[tuple[str, float]]:
    data_dict = total_by_category(rows)
    sorted_by_name = sorted(data_dict.items(), key=lambda item: item[0])
    sorted_dict = dict(sorted(sorted_by_name, reverse=True, key=lambda item: item[1]))
    output = [(k, v) for k, v in sorted_dict.items()]
    return output[:n]

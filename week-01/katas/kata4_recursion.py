"""Kata 4 — Recursion: flatten arbitrarily nested lists.

Implement `flatten` so it returns a single flat list of all non-list elements,
in order, no matter how deeply nested the input is.

  flatten([1, [2, [3, 4], 5], [[6]]]) -> [1, 2, 3, 4, 5, 6]

Treat only `list` as nestable (strings stay intact — don't iterate their chars).

Run `uv run pytest week-01/katas/test_kata4_recursion.py` to check.
"""

from __future__ import annotations

from typing import Any


def flatten(nested: list[Any]) -> list[Any]:
    output = []
    for item in nested:
        if isinstance(item, list):
            output.extend(flatten(item))
        else:
            output.append(item)
    return output

"""Kata 5 — Find and fix the bug.

Unlike the others, this module is fully "implemented" — but a test is failing.
Run the test first, read the failure, and figure out why. Then fix `collect`.

`collect(item, into=...)` is meant to append `item` to a fresh list each call
(unless the caller passes their own list) and return it. Two independent calls
should NOT share state.

This is one of Python's most famous gotchas. Once you see it, you'll never forget it.

Run `uv run pytest week-01/katas/test_kata5_fix_the_bug.py` to check.
"""

from __future__ import annotations

from typing import Any


def collect(item: Any, into: list[Any] | None = None) -> list[Any]:  # noqa: B006  (the bug — fix it)
    if into is None:
        into = []
    into.append(item)
    return into

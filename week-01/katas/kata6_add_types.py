"""Kata 6 — Add type annotations.

This module's logic is correct and its tests already pass. The exercise is typing:
add annotations until a strict type check is clean.

    uv run mypy --strict week-01/katas/kata6_add_types.py

Right now `--strict` will complain that these functions are untyped. Annotate the
parameters and return types (and any locals mypy can't infer) until it reports
"Success: no issues found". Don't change the behavior — the pytest tests must stay green.
"""

from __future__ import annotations


def word_counts(text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for word in text.lower().split():
        cleaned = word.strip(".,!?;:")
        if cleaned:
            counts[cleaned] = counts.get(cleaned, 0) + 1
    return counts


def most_common(text: str, n: int) -> list[tuple[str, int]]:
    ranked = sorted(word_counts(text).items(), key=lambda kv: (-kv[1], kv[0]))
    return ranked[:n]

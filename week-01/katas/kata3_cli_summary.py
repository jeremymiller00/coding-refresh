"""Kata 3 — A typed CLI that summarizes numbers from a file.

Implement `summarize(numbers)` to return a dict with keys:
  count, total, mean, minimum, maximum
For an empty list, count/total are 0 and mean/minimum/maximum are None.

Then wire up `main()` so that:
  uv run python week-01/katas/kata3_cli_summary.py path/to/numbers.txt
reads one number per line (ignoring blank lines) and prints the summary.

The tests exercise `summarize` directly; `main` is yours to wire (argparse).

Run `uv run pytest week-01/katas/test_kata3_cli_summary.py` to check.
"""

from __future__ import annotations

import sys
import argparse
from pathlib import Path
from typing import Optional, TypedDict


class Summary(TypedDict):
    count: int
    total: float
    mean: Optional[float]
    minimum: Optional[float]
    maximum: Optional[float]


def summarize(numbers: list[float]) -> Summary:
    count = len(numbers)
    total = sum(numbers)
    mean = None
    minimum = None
    maximum = None
    if count != 0:
        mean = total / count
        minimum = min(numbers)
        maximum = max(numbers)
    return Summary(
        count=count,
        total=total,
        mean=mean,
        minimum=minimum,
        maximum=maximum
    )


def read_numbers(path: Path) -> list[float]:
    with open(path) as file:
        data = file.readlines()
    return [x for x in data if x is not None]


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Summarize numbers in a file.")
    parser.add_argument("path", type=Path, help="File with one number per line")
    args = parser.parse_args(argv)
    summary = summarize(read_numbers(args.path))
    for key, value in summary.items():
        print(f"{key}: {value}")
    return 0


if __name__ == "__main__":
    main(sys.argv)
    sys.exit()

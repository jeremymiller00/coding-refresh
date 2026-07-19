# Week 1 Katas

Six short exercises to self-assess Python rust. Each has a module with a stub (or a bug) and a
test file that **starts failing**. Your job: make the tests pass.

## Workflow
```bash
cd <repo root>
uv sync                                  # ensure dev deps (pytest, ruff, mypy) are installed
uv run pytest week-01/katas              # see them all RED
# ... edit the kata modules ...
uv run pytest week-01/katas              # get them GREEN
uv run ruff check week-01/katas          # keep it clean
```

## The katas
1. **`kata1_clean_csv.py`** — data wrangling: parse messy CSV text into clean records.
2. **`kata2_aggregate.py`** — group + aggregate without pandas (`collections`).
3. **`kata3_cli_summary.py`** — a typed CLI: summarize numbers from a file (argparse).
4. **`kata4_recursion.py`** — recursion: flatten arbitrarily nested lists.
5. **`kata5_fix_the_bug.py`** — read the failing test, find the bug, fix it. (Classic gotcha.)
6. **`kata6_add_types.py`** — the logic works and tests pass; add type annotations until
   `uv run mypy week-01/katas/kata6_add_types.py` is clean.

As you go, jot what felt rusty in `../DIAGNOSTIC.md` — that drives the Week 1 calibration.

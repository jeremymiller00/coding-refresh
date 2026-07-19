# Week 1 — Diagnostic + Modern Python & Tooling Reset

**Why:** Calibrate how rusty you actually are, and stand up a professional 2026 toolchain so
every later week is friction-free.

## Learn (~3 hrs)
- **uv** for environment + dependency management (replaces pip/venv/poetry for most workflows)
- Python 3.12+ refresher: type hints, dataclasses, f-strings, comprehensions, pathlib
- **ruff** (lint + format), and **pyright** or **mypy** for type checking
- **pytest** basics: test discovery, assertions, fixtures, parametrize
- git refresh: branch → commit → PR hygiene, `.gitignore`

## Build (~2 hrs)
- The repo scaffold is already here (`pyproject.toml`, ruff/pytest config, `.gitignore`). Run `uv sync`.
- Complete 5–6 short katas to self-assess. Put them in `week-01/katas/`. Suggested:
  1. Parse a messy CSV → clean records (data wrangling)
  2. Group + aggregate without pandas (dicts/`collections`)
  3. A small typed CLI (argparse) that reads a file and prints a summary
  4. Write a recursive function + a test for it
  5. A function with a deliberate bug → write the failing test first, then fix
  6. Type-annotate an untyped function until pyright/mypy is clean

## Deliverable
- Repo with passing `uv run pytest` and clean `uv run ruff check .`
- `week-01/DIAGNOSTIC.md` — note which areas felt rusty (revisit in the calibration checkpoint)

## Self-check
You can scaffold a typed, tested Python project from scratch in under 15 minutes.

## Resources
uv · ruff · pytest · Pydantic docs — see [../RESOURCES.md](../RESOURCES.md)

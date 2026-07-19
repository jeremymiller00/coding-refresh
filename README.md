# coding-refresh

# This branch is a stash of the first failed agent integration attempt

An 8-week, project-driven curriculum to resharpen coding skills for **AI engineering and agents**.
You build one agent (the capstone) across the course; each week adds a real capability.

- 📋 **Start here:** [CURRICULUM.md](CURRICULUM.md) — the week-by-week plan + progress checklist.
- 📚 **Reading:** [RESOURCES.md](RESOURCES.md) — curated, docs-first.
- 🗂 **Weeks:** [`week-01/`](week-01/README.md) … [`week-08/`](week-08/README.md)

## Setup (Week 1)

```bash
# Install uv if needed: https://docs.astral.sh/uv
uv sync                 # create venv + install dev deps (pytest, ruff)
cp .env.example .env    # add your API keys (Week 2+)

# Verify the toolchain
uv run ruff check .
uv run pytest
```

## Layout

```
coding-refresh/
├── CURRICULUM.md      # the plan + checklist
├── RESOURCES.md       # curated reading
├── pyproject.toml     # deps, ruff, pytest config
├── week-01/ … week-08/  # one folder per week, each with its own README
└── src/               # shared capstone code accumulates here (created as needed)
```

## How to work each week

1. Read the week's `README.md` (objectives, resources, deliverable, self-check).
2. Build the deliverable. Commit it.
3. Confirm the self-check passes before moving on.

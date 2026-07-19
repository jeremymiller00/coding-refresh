# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository. When asked a question, respond as a tutor. Guide the user to discover the solution on their own, rather than give the solution. If the user is frustrated after many turns, start to offer small parts of the solution to allow continued progress.

## What this is

A personal, 8-week, project-driven curriculum for rebuilding coding skills toward AI engineering
and agents (see [CURRICULUM.md](CURRICULUM.md)). It is **not** a library or service — `pyproject.toml`
sets `[tool.uv] package = false` deliberately. One capstone agent is built incrementally across the
weeks; each `week-NN/` folder holds that week's README (objectives, deliverable, self-check) plus
its own build/test files. Code that later weeks depend on lives in `src/` instead of the week folder.

## Commands

```bash
uv sync                          # install/update the venv from pyproject.toml + uv.lock
uv run ruff check .              # lint (rules: pyflakes, pycodestyle, isort, bugbear, pyupgrade)
uv run pytest                    # run the full suite (all weeks + src)
uv run pytest week-04/           # run one week's tests
uv run pytest week-02/test_llm_client.py::test_name   # run a single test
uv run python week-02/cli.py "prompt text"             # run the Week 2 CLI against the live API
```

Tests run offline by default via dependency-injected fakes (scripted model functions, no network,
no API key). Tests marked `@pytest.mark.integration` (e.g. in `week-02/test_llm_client.py`) hit the
real Anthropic API and need `ANTHROPIC_API_KEY` set in `.env`.

## Architecture

**`src/` vs `week-NN/`:** `src/` holds the modules the curriculum explicitly calls "the capstone" —
code reused by later weeks (`llm_client.py`, `extract.py`, `agent_loop.py`). Everything else
(week-specific CLIs, framework comparisons, tests) lives inside its own `week-NN/` folder. Because
`pyproject.toml` sets `pythonpath = ["src"]` for pytest, tests anywhere in the repo can
`from llm_client import ...` etc. directly. Scripts run outside pytest (like `week-02/cli.py`) do
their own `sys.path.insert(0, ".../src")` bootstrap before importing — follow that pattern for any
new runnable script outside `src/`.

**The agent loop contract (`src/agent_loop.py`):** `Tool` (name/description/JSON-schema/`fn`),
`ToolCall`, and `Turn` (role + text + optional `tool_calls`) are the shared vocabulary every later
week's model integration adapts to. `run_agent` drives `model -> tool calls -> execute -> feed
result back -> repeat` with a `max_steps` guard; the model is injected as a `ModelFn` so the loop
itself is testable without any network call. `execute_tool` never raises — unknown tools and tool
exceptions both become string results fed back to the model.

**`src/llm_client.py`:** A hand-rolled, provider-agnostic-*interface* wrapper around the Anthropic
Messages API using raw `requests` (not the `anthropic` SDK) — that's intentional for the Week 2
learning goal of owning the wire format. `PRICING` is a manually maintained per-model price table;
update it from current provider docs rather than trusting stale values. System-role messages are
extracted out of `messages` and sent via the API's separate `system` field
(`_set_sys_prompt_parameter`), since Anthropic doesn't accept `system` as an inline message role.

**`src/extract.py`:** The structured-extraction pattern used for the capstone's ingestion layer:
`build_extraction_prompt` (pure) -> model call -> `parse_response` (pure, strips ```json fences,
validates against a Pydantic model) -> `extract` (the retry loop, re-prompting the model with its
own bad output on `ValidationError` up to `max_attempts`). New extraction schemas should follow this
three-function split so the parsing/validation stays independently testable.

**Per-week deliverables build on the previous week's contract** — e.g. Week 4's
`week-04/agent_framework.py` is required to solve the *same* task as `src/agent_loop.py` (an `add`
tool + a forced tool call) so the two are a fair comparison; Week 3's `extract()` is designed to take
a `call_model` adapter built from Week 2's `LLMClient`. When editing one week's file, check whether
neighboring weeks assume its current interface before changing signatures.

**Katas (`week-01/katas/`):** small, self-contained kata + test pairs (`kataN_*.py` /
`test_kataN_*.py`) used for the Week 1 skills diagnostic — independent of the `src/` capstone code.

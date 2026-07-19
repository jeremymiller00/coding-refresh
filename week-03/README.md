# Week 3 — Prompt & Context Engineering + Structured Output

**Why:** An agent's reliability is mostly the reliability of its prompts and its structured I/O.

## Learn (~3 hrs)
- Prompt patterns: clear role/context setting, few-shot examples, task decomposition
- Context-window budgeting: what to include, what to drop, ordering effects
- **Pydantic v2** schemas for validated structured output
- Tool/function-calling as a structured-output mechanism (preview of Week 4)
- When structured output beats free text — and when it doesn't

## Build (~2 hrs)
- An extractor that turns messy unstructured input (customer feedback / meeting notes) into
  **validated Pydantic objects** — this becomes the capstone's ingestion layer
- Handle malformed model output: validate → re-prompt on failure (don't crash)

## Deliverable
- `src/extract.py` with a Pydantic schema + validation/retry loop
- `week-03/test_extract.py` — a small fixture set proving it parses reliably

## Self-check
Malformed model output is caught and re-prompted, not crashed on.

## Resources
Pydantic docs · Anthropic tool-use docs · "Building effective agents" — see [../RESOURCES.md](../RESOURCES.md)
Pydantic tutoorial [https://realpython.com/python-pydantic/]

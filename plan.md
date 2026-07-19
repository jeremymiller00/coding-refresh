# Curriculum: Resharpening Coding Skills for AI Engineering & Agents

## Context

The user is a data scientist who moved into a product role and whose hands-on coding has gone rusty. They want to rebuild engineering skill with a focus on **AI engineering and agents**, with the explicit goal of being able to **ship real agentic systems** — not just understand them conceptually.

Constraints gathered from the user:
- **Time:** ~5 hrs/week over **8 weeks** (~40 hrs total). The curriculum must be high-ROI and avoid re-teaching what a data scientist already knows (ML theory, stats, numpy/pandas basics).
- **Outcome:** Ship real agents end-to-end.
- **Stack:** Framework-agnostic — concepts that transfer across providers, with concrete tools named so the work stays hands-on.
- **Starting point:** Self-described as mixed/unsure → Week 1 includes a short diagnostic to calibrate.

**Design philosophy:** A single **project spine**. The user builds *one* agent across the whole course; each week adds a real capability and ends in a runnable deliverable. This beats disconnected tutorials for a "ship real agents" goal and keeps motivation high. Theory is introduced only in service of the next build step.

## Recommended capstone (the spine)

**A "Product Research & Prioritization Agent"** — relevant to the user's PM role and CLAUDE.md framing (validated, prioritized backlog). The agent ingests unstructured inputs (customer feedback, notes, docs), retrieves from a knowledge base, reasons over them with tools, and outputs a prioritized recommendation / draft PR-FAQ.

This is chosen because it (a) exercises every core agent capability — structured output, tools, RAG, multi-step reasoning, evals — and (b) produces something the user would actually use. Two fallback capstones if they prefer: a **codebase/PR review assistant** or a **personal research agent** (search → synthesize → cite). Final choice confirmed at kickoff.

## The 8-Week Curriculum

Each week: ~5 hrs = ~3 hrs learning/reading + ~2 hrs building. Each ends with a **Deliverable** (committed to the repo) and a **Self-check** (how you know it worked).

### Week 1 — Diagnostic + Modern Python & Tooling Reset
- **Why:** Calibrate the rust and stand up a professional 2026 toolchain so every later week is friction-free.
- **Learn:** Modern environment management with **uv** (replaces pip/venv/poetry for most workflows), Python 3.12+, **ruff** (lint+format), type hints + **pyright/mypy**, **pytest** basics, git refresh (branch, commit, PR hygiene).
- **Build:** Repo scaffold (`uv init`, ruff, pytest, pre-commit). Complete 5–6 short katas (data wrangling + a small CLI) to self-assess.
- **Deliverable:** Clean repo with passing `pytest` + `ruff check`; a `DIAGNOSTIC.md` noting which areas felt rusty (to revisit).
- **Self-check:** You can scaffold a typed, tested Python project from scratch in <15 min.

### Week 2 — LLM APIs From First Principles
- **Why:** Everything agentic is built on raw model calls. Own the primitives before any framework hides them.
- **Learn:** Messages/chat API shape, tokens & context windows, system vs user vs assistant roles, temperature, streaming, structured/JSON output, retries & error handling, the cost+latency mental model.
- **Build:** A CLI that calls an LLM, streams output, handles rate-limit/timeout errors with backoff, and logs token usage + cost per call.
- **Deliverable:** `llm_client.py` wrapper used by all later weeks.
- **Self-check:** You can estimate the cost of a call before running it and explain where latency comes from.

### Week 3 — Prompt & Context Engineering + Structured Output
- **Why:** Reliability of an agent is mostly reliability of its prompts and its structured I/O.
- **Learn:** Prompt patterns (few-shot, decomposition, role/context setting), context-window budgeting, **Pydantic** schemas for validated structured output, when structured output beats free text.
- **Build:** An extractor that turns messy unstructured input (feedback/notes) into validated Pydantic objects — the capstone's ingestion layer.
- **Deliverable:** `extract.py` with schema validation + a small test set proving it parses reliably.
- **Self-check:** Malformed model output is caught and re-prompted, not crashed on.

### Week 4 — Tool Use & The Agent Loop (the core week)
- **Why:** The agent loop (model → tool call → execute → feed result back → repeat) IS what an agent is. Build it by hand, then see what a framework abstracts.
- **Learn:** Tool/function calling spec, the control loop, stop conditions, error recovery within the loop. Then introduce **one** framework (LangGraph or the Claude Agent SDK) and rebuild the same loop to compare.
- **Build:** A from-scratch tool-using agent with 2–3 real tools (e.g., web search, calculator, file read), then the framework version.
- **Deliverable:** `agent_loop.py` (hand-rolled) + `agent_framework.py` (framework), both passing the same task.
- **Self-check:** You can explain exactly what the framework does for you — and what it hides.

### Week 5 — Retrieval (RAG) & Memory
- **Why:** Agents need grounding in your data. Know when to use RAG vs long-context vs tools.
- **Learn:** Embeddings, chunking strategies, a vector store (Chroma or pgvector/SQLite-vec), retrieval quality, the RAG-vs-long-context tradeoff, simple agent memory.
- **Build:** Give the capstone agent a knowledge base it retrieves from before answering.
- **Deliverable:** `retrieval.py` + an ingested corpus; agent answers cite retrieved sources.
- **Self-check:** You can articulate why a given query did/didn't retrieve the right chunk.

### Week 6 — Multi-Step Patterns & MCP
- **Why:** Real agents plan, reflect, and compose tools — and the industry is standardizing tool/context integration on **MCP**.
- **Learn:** Planning, reflection, orchestrator-worker, and routing patterns; **MCP** (Model Context Protocol) as the standard for connecting tools/data to agents.
- **Build:** Extend the capstone with a multi-step workflow (e.g., plan → retrieve → score → draft) and connect at least one capability via an MCP server.
- **Deliverable:** Multi-step capstone that produces a structured prioritized output.
- **Self-check:** The agent recovers from a failed step instead of derailing.

### Week 7 — Evals, Testing, Observability & Guardrails
- **Why:** This discipline separates demos from shipped products — and it's the highest-leverage skill for a PM who ships agents.
- **Learn:** Building an eval set, **LLM-as-judge**, regression testing of prompts, tracing/observability (Langfuse or similar), cost/latency tracking, failure-mode taxonomy, basic safety guardrails (input/output validation, injection awareness).
- **Build:** An eval harness that scores the capstone on a fixed test set and fails CI on regression.
- **Deliverable:** `evals/` with a dataset, judge, and a score report.
- **Self-check:** You can quantify whether a prompt change made the agent better or worse.

### Week 8 — Deployment + Capstone Ship
- **Why:** "Ship real agents" means it runs somewhere other than your laptop.
- **Learn:** Packaging, a **FastAPI** endpoint (or serverless), secrets/env management, minimal monitoring + logging in production.
- **Build:** Wrap the capstone behind an API, deploy it, write a short README + demo.
- **Deliverable:** Deployed capstone agent + README with architecture diagram, costs, eval results, and known limitations.
- **Self-check:** A second person can hit your endpoint and get a useful, grounded result.

## What gets created on approval

1. A `CURRICULUM.md` in the working directory (`coding-refresh/`) containing the full 8-week plan above as a trackable checklist.
2. A `week-01/` … `week-08/` directory structure with a per-week `README.md` stub (objectives, resources, deliverable, self-check).
3. The Week 1 repo scaffold (`uv`, ruff, pytest config, `.gitignore`) so the user can start immediately.
4. A short curated `RESOURCES.md` (docs-first: provider API docs, MCP spec, a small number of high-signal references) — kept lean, not a link dump.

No code beyond scaffolding is pre-written — the point is for the user to build it.

## Verification / how we'll know it's working

- **Per week:** the listed Deliverable is committed and its Self-check passes. Weeks 1, 4, 7 have concrete runnable gates (`pytest`/`ruff` green; both agent loops solve the same task; eval harness produces a score).
- **End-to-end:** the capstone is deployed and returns a grounded, structured result to an external caller, with eval scores and cost recorded in the README.
- **Calibration checkpoint:** after Week 1's diagnostic, we revisit and, if needed, compress or expand early weeks (e.g., skip the Python reset if fundamentals are solid, or add a remedial half-week if rustier than expected).

## Open choice (confirm at kickoff, not blocking)

- Capstone domain: **Product Research & Prioritization Agent** (recommended) vs PR/code-review assistant vs personal research agent.
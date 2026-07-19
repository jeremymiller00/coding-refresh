# Week 7 — Evals, Testing, Observability & Guardrails

**Why:** This discipline separates demos from shipped products — and it's the highest-leverage
skill for a PM who ships agents. (This is your competitive edge given your DS background.)

## Learn (~3 hrs)
- Building an eval set: inputs + expected behavior, golden examples
- **LLM-as-judge**: scoring rubrics, pairwise comparison, its failure modes
- Regression testing of prompts (a prompt change is a code change)
- Tracing / observability (**Langfuse** or similar): spans, cost, latency per step
- Failure-mode taxonomy for agents (hallucination, tool misuse, loops, refusal)
- Basic guardrails: input/output validation, prompt-injection awareness

## Build (~2 hrs)
- An eval harness that scores the capstone on a **fixed test set**
- Wire it so a regression **fails CI** (or a local `pytest`/make target)

## Deliverable
- `evals/` with a dataset, a judge, and a score report
- A baseline score recorded for the capstone

## Self-check
You can quantify whether a prompt change made the agent better or worse.

## Resources
Langfuse docs · Anthropic cookbook `evaluations/` — see [../RESOURCES.md](../RESOURCES.md)

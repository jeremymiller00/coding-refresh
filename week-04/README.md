# Week 4 — Tool Use & The Agent Loop (the core week)

**Why:** The agent loop — model → tool call → execute → feed result back → repeat — *is* what an agent is. Build it by hand first, then see exactly what a framework abstracts away.

## Learn (~3 hrs)
- The tool/function-calling spec (tool schemas, tool_use / tool_result message turns)
- The control loop: when to call a tool, when to stop, max-iteration guards
- Error recovery *within* the loop (a tool throws → feed the error back, don't crash)
- One framework for comparison: **LangGraph** or the **Claude Agent SDK**

## Build (~2 hrs)
- A from-scratch tool-using agent with 2–3 real tools (e.g., web search, calculator, file read)
- Then rebuild the **same** task with a framework

## Deliverable
- `src/agent_loop.py` — hand-rolled loop
- `week-04/agent_framework.py` — framework version, solving the same task

## Self-check
You can explain exactly what the framework does for you — and what it hides.

## Resources
Anthropic tool-use docs · Anthropic cookbook · LangGraph docs · "Building effective agents"
— see [../RESOURCES.md](../RESOURCES.md)

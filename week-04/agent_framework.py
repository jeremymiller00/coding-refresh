"""Week 4 deliverable (part 2) — the SAME task, rebuilt on a framework.

The point of this file is comparison, not novelty. Solve the identical task you solved with the
hand-rolled loop in src/agent_loop.py, but let a framework own the loop, tool-calling, and message
bookkeeping. Then answer for yourself: what did the framework do for me, and what did it hide?

Pick ONE framework and install it:
    LangGraph:          uv add langgraph langchain-anthropic
    Claude Agent SDK:   uv add anthropic   (agents/tools via the SDK)

The shared task (keep it identical to your manual run so the comparison is fair):
    Tools:  `add(a, b)`  and one that can fail, e.g. `lookup(term)`.
    Prompt: something that forces at least one tool call, e.g.
            "What is 2 + 3, and then look up the result?"

This file is exercised manually (it needs a live model), so there's no unit test — the deliverable
is a working run plus a short written comparison (put it in week-04/COMPARISON.md).

Fill in the two TODOs below.
"""

from __future__ import annotations


def add(a: int, b: int) -> int:
    """The same tool your hand-rolled agent used — reuse it here so the task matches."""
    return a + b


def build_agent():  # return type depends on the framework you choose
    """TODO: construct a framework agent with the tool(s) above registered.

    LangGraph: build a graph / prebuilt ReAct agent bound to a ChatAnthropic model + tools.
    Agent SDK: define the tool(s) and create the agent with your model.
    """
    raise NotImplementedError("Build the framework agent")


def main() -> int:
    """TODO: run the agent on the shared prompt and print the final answer + any tool calls made."""
    _agent = build_agent()
    raise NotImplementedError("Run the framework agent on the shared task")


if __name__ == "__main__":
    raise SystemExit(main())

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
import argparse

from deepagents import create_deep_agent


DEFAULT_MODEL = "anthropic:claude-haiku-4-5"

def add(a: int, b: int) -> int:
    """The same tool your hand-rolled agent used — reuse it here so the task matches."""
    return a + b


def build_agent(
        model: str,
        tools: list[callable] = None,
        system_prompt: str = None
        ):
    """TODO: construct a framework agent with the tool(s) above registered.

    LangGraph: build a graph / prebuilt ReAct agent bound to a ChatAnthropic model + tools.
    Agent SDK: define the tool(s) and create the agent with your model.
    """
    agent = create_deep_agent(
        model=model,
        tools=tools,
        system_prompt=system_prompt
    )
    return agent


def main(argv: list[str] | None = None) -> int:
    """TODO: run the agent on the shared prompt and print the final answer + any tool calls made."""
    parser = argparse.ArgumentParser(description="Stream a completion from an LLM.")
    parser.add_argument("prompt", help="The user prompt")
    parser.add_argument("--system", default=None, help="Optional system prompt")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    args = parser.parse_args(argv)
    
    agent = create_deep_agent(
        model=args.model,
        tools=[add],
        system_prompt=args.system
    )
    # result = agent.invoke({"messages": [{"role": "user", "content": args.prompt}]})
    input = {"messages": [{"role": "user", "content": args.prompt}]}
    stream = agent.stream_events(input, version="v3")

    stream = agent.stream_events(input, version="v3")
    
    for message in stream.messages:
        print(f"[{message.node}] ", end="")
        for delta in message.text:
            print(delta, end="", flush=True)
    
        full_message = message.output
        usage = full_message.usage_metadata
        if usage:
            print(usage)
    
    # Print the agent's response
    # print(result["messages"][-1].content)
    

if __name__ == "__main__":
    raise SystemExit(main())

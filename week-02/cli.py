"""Week 2 deliverable — a streaming CLI on top of src/llm_client.py.

Goal:
  uv run python week-02/cli.py "Explain tokens like I'm five"
  uv run python week-02/cli.py --no-stream --model claude-... "..."

Behaviour to implement in `main`:
  1. Build messages from the prompt (and optional --system).
  2. If streaming (default): print chunks from client.stream(...) as they arrive.
     If --no-stream: call client.complete(...) and print the text.
  3. After the response, print a usage line to stderr: tokens in/out and cost in USD.

Keep the LLM logic in llm_client.py — this file is just the I/O shell.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

# Make the shared src/ package importable when running this script directly.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from llm_client import LLMClient, LLMResponse, build_messages  # noqa: E402  (after sys.path bootstrap)
from agent_loop import Tool, run_agent


DEFAULT_MODEL = "claude-haiku-4-5"  # adjust to whatever you're targeting


# tools
def _add(a: int, b: int) -> str:
    return str(a + b)


ADD = Tool(
    name="add",
    description="Add two integers. Use this tool when the user is asking to add two numbers. Do not guess. Use only this tool in this case.",
    input_schema={"type": "object", "properties": {"a": {"type": "integer"}, "b": {"type": "integer"}}},
    fn=_add,
)
TOOLS = [ADD]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Stream a completion from an LLM.")
    parser.add_argument("prompt", help="The user prompt")
    parser.add_argument("--system", default=None, help="Optional system prompt")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument(
        "--agent",
        dest="agent",
        action="store_true",
        help="Run in agent mode")
    parser.add_argument(
        "--no-stream",
        dest="stream",
        action="store_false",
        help="Use a single complete() call instead of streaming",
    )
    parser.add_argument("--max-tokens", type=int, default=1024)
    parser.add_argument("--temperature", type=float, default=1.0)
    args = parser.parse_args(argv)

    _client = LLMClient(args.model)
    _messages = build_messages(args.prompt, system=args.system)
    # print(_messages)
    # TODO: implement the stream / no-stream branches and the usage line (to stderr).
    if args.agent:
        # for now just pass the prompt
        # will need to figure out how to incude system prompt
        run_agent(prompt=args.prompt, tools=[TOOLS], model=_client.stream)

    if args.stream:
        for chunk in _client.stream(_messages, tools=TOOLS):
            if type(chunk) is not LLMResponse:
                print(chunk, end="", flush=True)
            else:
                llm_response = chunk
                print("\n")
                print(f"Cost: {llm_response.cost_usd}", file=sys.stderr)
                print(f"Input Tokens: {llm_response.input_tokens}", file=sys.stderr)
                print(f"Output Tokens: {llm_response.output_tokens}", file=sys.stderr)
    else:
        llm_response = _client.complete(_messages, tools=TOOLS)
        print(llm_response.text)
        print()
        print(f"Cost: {llm_response.cost_usd}", file=sys.stderr)
        print(f"Input Tokens: {llm_response.input_tokens}", file=sys.stderr)
        print(f"Output Tokens: {llm_response.output_tokens}", file=sys.stderr)


if __name__ == "__main__":
    main()
    SystemExit(0)

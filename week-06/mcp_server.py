"""Week 6 deliverable (part 2) — expose a capstone capability over MCP.

MCP (Model Context Protocol) is the emerging standard for connecting tools/data to any MCP-aware
client (Claude Desktop, Claude Code, IDEs, your own agent). The goal here: take ONE capability you
already built and serve it over MCP, so it's reusable outside your own loop.

Good candidates to expose (reuse your existing src/ code — don't reimplement):
- `search_feedback(query)`  -> retrieval over your Week 5 VectorStore + corpus.
- `prioritize(items)`       -> your Week 6 pipeline.

Setup:   uv add "mcp[cli]"
Run:     uv run mcp dev week-06/mcp_server.py        # opens the MCP Inspector to poke the tool
Wire it: register this server with an MCP client (e.g. Claude Desktop / Claude Code) and call it.

This file is exercised manually via an MCP client / the Inspector — no unit test. The deliverable is
a working tool call through MCP, plus a note in week-06/README on what MCP gave you over a plain
Python function (discovery, transport, reuse across clients).

Sketch with the FastMCP helper from the SDK:

    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("capstone")

    @mcp.tool()
    def search_feedback(query: str, k: int = 4) -> str:
        # build your VectorStore from the corpus, search, return build_context(results)
        ...

    if __name__ == "__main__":
        mcp.run()

Fill in the TODO below.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Make the shared src/ package importable when running this script directly.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from dotenv import load_dotenv
from mcp.server.mcpserver import MCPServer

import llm_client as llm
import pipeline as pl

load_dotenv()


client = llm.LLMClient(model="claude-haiku-4-5")
mcp = MCPServer("prioritize-pipeline")

def write(prompt: str) -> str:
    messages = llm.build_messages(prompt=prompt)
    response = client.complete(messages=messages)
    return response.text


def score(text: str) -> tuple[float, str]:
    """Generic scoring function.
    A valid scoring function depends on the use case"""
    return float(len(text)), f"len={len(text)}"


@mcp.tool()
def draft_summary(items: list[str]) -> str:
    prioritized_items = pl.prioritize(items=items, score_fn=score)
    summary = pl.draft_summary(
        priorities=prioritized_items,
        top_n=5,
        write_fn=write
        )
    return summary


if __name__ == "__main__":
    mcp.run()

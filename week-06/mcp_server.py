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


def main() -> None:
    # TODO: build a FastMCP server, register one capability that reuses your src/ code, and run it.
    raise NotImplementedError("Expose a capstone capability over MCP")


if __name__ == "__main__":
    main()

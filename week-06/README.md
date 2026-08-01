# Week 6 — Multi-Step Patterns & MCP
**Why:** Real agents plan, reflect, and compose tools — and the industry is standardizing
tool/context integration on **MCP** (Model Context Protocol).

## Learn (~3 hrs)
- Agent patterns: planning, reflection, orchestrator-worker, routing
- When a deterministic *workflow* beats an autonomous *agent* (cost/reliability)
- **MCP**: what it is, client vs server, why it matters for tool/data integration
- Connecting an existing MCP server, and the shape of writing your own

## Build (~2 hrs)
- Extend the capstone with a multi-step workflow: e.g. **plan → retrieve → score → draft**
- Connect at least one capability via an **MCP server**

## Deliverable
- Multi-step capstone that produces a **structured prioritized output**
- One capability wired through MCP

## Self-check
The agent recovers from a failed step instead of derailing.

## Resources
MCP docs (modelcontextprotocol.io) · "Building effective agents" (patterns) — see [../RESOURCES.md](../RESOURCES.md)

## What MCP give you over plain python tools
Using MCP, the tools can be written as straightforward python functions. The framework provides the schema, interface between the client application and the tools the MCP contains, and the MCP inspector tool for isolated testing of the MCP.

Using MCP facilitates re-use across tools such as Claude Code, or the Claude desktop app, or really any application that can interact with MCPs. It does this through a standardized discovery mechanism, such as `tools/list`.

The MCP framework also handles the setup and operation of the standard transport protocol so that the client can invoke the MCP tools without custom glue code. 

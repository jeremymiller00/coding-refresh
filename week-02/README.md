# Week 2 — LLM APIs From First Principles

**Why:** Everything agentic is built on raw model calls. Own the primitives before any framework
hides them.

## Learn (~3 hrs)
- Messages/chat API shape: system vs user vs assistant roles
- Tokens & context windows; how to count/estimate before you call
- Sampling params: temperature, top_p, max_tokens, stop sequences
- Streaming responses
- Structured / JSON output basics (full treatment in Week 3)
- Retries, timeouts, rate limits, exponential backoff
- The cost + latency mental model (price per input/output token; where latency comes from)

## Build (~2 hrs)
- A CLI that calls an LLM and **streams** output
- Robust error handling: retry with backoff on rate-limit/timeout
- Log **token usage + cost per call** to stdout or a file

## Deliverable
- `src/llm_client.py` — a thin wrapper (provider-agnostic interface) reused by all later weeks
- `week-02/cli.py` — the streaming CLI that uses it

## Self-check
You can estimate the cost of a call before running it, and explain where latency comes from.

## Resources
Anthropic API docs (Messages, streaming) · OpenAI docs for comparison — see [../RESOURCES.md](../RESOURCES.md)

# Week 5 — Retrieval (RAG) & Memory

**Why:** Agents need grounding in your data. Know when to reach for RAG vs long-context vs tools.

## Learn (~3 hrs)
- Embeddings: what they are, how similarity search works
- Chunking strategies and why they matter
- A vector store: **Chroma** (simplest local) or **sqlite-vec** (zero-infra)
- Retrieval quality: top-k, re-ranking, why a query misses
- The **RAG vs long-context vs tools** tradeoff — when each wins
- Simple agent memory (conversation + retrieved facts)

## Build (~2 hrs)
- Give the capstone agent a knowledge base it retrieves from before answering
- Agent answers should **cite** the retrieved sources

## Deliverable
- `src/retrieval.py` + an ingested corpus (your own notes/docs work well)
- Capstone answers grounded in retrieved chunks, with citations

## Self-check
You can articulate why a given query did or didn't retrieve the right chunk.

## Resources
Chroma docs · sqlite-vec · Anthropic embeddings/RAG guidance — see [../RESOURCES.md](../RESOURCES.md)

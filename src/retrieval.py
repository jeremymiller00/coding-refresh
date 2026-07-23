"""Week 5 deliverable — retrieval (RAG), hand-rolled.

Give the capstone agent a knowledge base it can search before answering, and make answers cite
their sources. Build the pieces yourself first (chunk -> embed -> cosine search -> context) so you
understand what a vector DB does; swapping in Chroma / sqlite-vec is then a drop-in extension.

Design note — the embedder is injected so everything here is testable OFFLINE:
    EmbedFn = (list[str]) -> list[vector]
    In tests you pass a deterministic fake (bag-of-words), so retrieval logic is verifiable with no
    network and no key. In real use you plug in a provider embeddings API or a local model.

    Heads up: Anthropic has NO embeddings endpoint — they recommend Voyage AI. So this is genuinely
    provider-agnostic. Options for the real EmbedFn:
        Voyage:               uv add voyageai
        OpenAI embeddings:    uv add openai
        Local (no API):       uv add sentence-transformers

What you implement (the dataclasses/types below are given):
- `chunk_text(text, *, source, ...)`  pure — split a document into overlapping chunks.
- `cosine_similarity(a, b)`           pure — the ranking math. Do this FIRST (tests pin it).
- `VectorStore.add` / `.search`       embed + store, then embed-query + rank top-k.
- `build_context(results)`            pure — format retrieved chunks WITH citations for the prompt.

Test:  uv run pytest week-05/test_retrieval.py     (offline — deterministic fake embedder)
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from math import sqrt

# Embed a batch of texts into a list of equal-length float vectors.
EmbedFn = Callable[[list[str]], list[list[float]]]


@dataclass(frozen=True)
class Chunk:
    text: str
    source: str  # where it came from, so answers can cite it
    id: str | None = None


@dataclass(frozen=True)
class SearchResult:
    chunk: Chunk
    score: float


def chunk_text(
    text: str,
    *,
    source: str,
    max_chars: int = 500,
    overlap: int = 50,
) -> list[Chunk]:
    """Split `text` into chunks of at most `max_chars`, advancing by (max_chars - overlap).

    Every chunk carries `source`. Short text -> a single chunk. Overlap keeps context from being
    severed at boundaries. (Real systems chunk on tokens/sentences; chars keep this testable.)
    """
    text_length = len(text)
    if text_length < max_chars:
        return [Chunk(text=text, source=source)]

    start_of_chunk = 0
    chunks = []
    while start_of_chunk < text_length:
        last = start_of_chunk + max_chars
        if last > text_length:
            last = text_length
        
        text_chunk = text[start_of_chunk:last]
        chunks.append(Chunk(text=text_chunk, source=source))
        start_of_chunk += (max_chars - overlap)

    return chunks


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Cosine similarity of two equal-length vectors: dot(a, b) / (||a|| * ||b||).

    Pure math, no dependencies. Return 0.0 if either vector has zero magnitude (avoid dividing by 0).
    
    compute magnitudes
    if one is 0, return 0.0
    compute dot product
    compute cosine sim
    """
    norm_a = l2_norm(a)
    norm_b = l2_norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    
    dot_product = dot(a, b)

    return dot_product / (norm_a * norm_b)


def l2_norm(x: list[float]) -> float:
    '''
    Compute the l2 norm of a vector
    '''
    x_squared = [n**2 for n in x]
    x_sum = sum(x_squared)
    l2_norm_a = sqrt(x_sum)

    return l2_norm_a


def dot(x: list[float], y: list[float]) -> float:
    '''
    Compute the dot product of two vectors
    '''
    if not len(x) == len(y):
        raise ValueError("The two vectors must be the same length")
    
    dot_product = 0.0
    for i in range(len(x)):
        dot_product += (x[i] * y[i])
    
    return dot_product


def build_context(results: list[SearchResult]) -> str:
    """Format retrieved chunks into a context block the model can quote and CITE.

    Include each chunk's source so the agent can attribute its answer (that's the week's self-check).
    e.g.  "[source: feedback_042.md]\\n<chunk text>\\n\\n[source: ...]\\n..."
    """
    context = ""
    for result in results:
        context += f"[source: {result.chunk.source}]: {result.chunk.text}\\n"

    return context


class VectorStore:
    """A minimal in-memory vector store. Later: swap the internals for Chroma / sqlite-vec."""

    def __init__(self) -> None:
        # Store (chunk, vector) pairs. A real store persists these and indexes them for speed.
        self._entries: list[tuple[Chunk, list[float]]] = []

    def add(self, chunks: list[Chunk], embed: EmbedFn) -> None:
        """Embed the chunks (batch the texts through `embed`) and store them with their vectors."""
        embeddings = embed([chunk.text for chunk in chunks])
        for i in range(len(chunks)):
            self._entries.append((chunks[i], embeddings[i]))
        return None

    def search(self, query: str, embed: EmbedFn, k: int = 4) -> list[SearchResult]:
        """Embed the query, score every stored chunk by cosine similarity, return the top-k.

        Results sorted by score descending. If the store is empty, return [].

        check empty
        embed query
        calculate score for each pair(query, chunk)
        sort by highest score
        return top k
        """
        if self._entries == []:
            return []
        
        query_embedding = embed([query])[0]
        results = []
        for entry in self._entries:
            results.append(
                SearchResult(
                    chunk=entry[0],
                    score=cosine_similarity(query_embedding, entry[1])
                    )
                )
            
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:k]

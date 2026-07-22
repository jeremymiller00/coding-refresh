"""Offline tests for Week 5 retrieval — no API key, no network.

The fake embedder is a deterministic bag-of-words over a fixed vocabulary, so cosine similarity is
meaningful: a query sharing words with a chunk scores higher. That lets us assert real retrieval
behaviour (the right chunk comes back) without any embedding model.
"""

import pytest

from retrieval import (
    Chunk,
    VectorStore,
    build_context,
    chunk_text,
    cosine_similarity,
)

VOCAB = ["cat", "dog", "tax", "invoice", "login", "slow"]


def fake_embed(texts: list[str]) -> list[list[float]]:
    vectors = []
    for text in texts:
        words = text.lower().split()
        vectors.append([float(words.count(term)) for term in VOCAB])
    return vectors


# --- cosine_similarity (pure) ----------------------------------------------

def test_cosine_identical():
    assert cosine_similarity([1.0, 0.0], [1.0, 0.0]) == pytest.approx(1.0)


def test_cosine_orthogonal():
    assert cosine_similarity([1.0, 0.0], [0.0, 1.0]) == pytest.approx(0.0)


def test_cosine_scale_invariant():
    assert cosine_similarity([1.0, 1.0], [2.0, 2.0]) == pytest.approx(1.0)


def test_cosine_zero_vector_is_zero():
    assert cosine_similarity([0.0, 0.0], [1.0, 2.0]) == 0.0


# --- chunk_text (pure) ------------------------------------------------------

def test_chunk_short_text_single_chunk():
    chunks = chunk_text("hello world", source="s.md", max_chars=40, overlap=10)
    assert len(chunks) == 1
    assert chunks[0].text == "hello world"
    assert chunks[0].source == "s.md"


def test_chunk_respects_max_chars_and_overlap():
    text = "abcdefghij" * 10  # 100 chars
    chunks = chunk_text(text, source="s.md", max_chars=40, overlap=10)
    assert all(len(c.text) <= 40 for c in chunks)
    assert chunks[0].text == text[:40]
    assert all(c.source == "s.md" for c in chunks)
    # step = max_chars - overlap = 30 -> starts at 0, 30, 60, 90 -> 4 chunks
    assert len(chunks) == 4


# --- VectorStore.search -----------------------------------------------------

CORPUS = [
    Chunk(text="the cat sat on the mat", source="a.md"),
    Chunk(text="the dog ran in the park", source="b.md"),
    Chunk(text="pay your tax invoice on time", source="c.md"),
    Chunk(text="login is slow slow slow on mobile", source="d.md"),
]


def _store() -> VectorStore:
    store = VectorStore()
    store.add(CORPUS, fake_embed)
    return store


def test_search_returns_most_relevant_chunk_first():
    results = _store().search("cat", fake_embed, k=1)
    assert len(results) == 1
    assert results[0].chunk.source == "a.md"


def test_search_ranks_by_similarity():
    results = _store().search("login slow", fake_embed, k=4)
    assert results[0].chunk.source == "d.md"
    scores = [r.score for r in results]
    assert scores == sorted(scores, reverse=True)


def test_search_respects_k():
    assert len(_store().search("tax", fake_embed, k=2)) == 2


def test_search_empty_store():
    assert VectorStore().search("anything", fake_embed) == []


# --- build_context ----------------------------------------------------------

def test_build_context_includes_text_and_sources():
    results = _store().search("cat", fake_embed, k=1)
    context = build_context(results)
    assert "the cat sat on the mat" in context
    assert "a.md" in context  # citation present

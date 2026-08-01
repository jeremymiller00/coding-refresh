"""Offline tests for the Week 6 multi-step pipeline — no API key, no network.

Steps are injected as deterministic fakes, so we can verify orchestration AND the failure-recovery
contract (one item's scoring raises; the pipeline must recover it and keep going).
"""


from pipeline import (
    Priority,
    Scored,
    draft_summary,
    prioritize,
    rank_items,
    score_items,
)


def score_by_length(text: str) -> tuple[float, str]:
    return float(len(text)), f"len={len(text)}"


def score_that_explodes_on(bad: str):
    def score_fn(text: str) -> tuple[float, str]:
        if text == bad:
            raise ValueError("scorer blew up")
        return score_by_length(text)

    return score_fn


# --- score_items ------------------------------------------------------------

def test_score_items_basic():
    scored = score_items(["ab", "abcd"], score_fn=score_by_length)
    assert scored == [Scored("ab", 2.0, "len=2"), Scored("abcd", 4.0, "len=4")]


def test_score_items_recovers_from_failure():
    # "boom" makes the scorer raise; the batch must survive and keep all items in order.
    scored = score_items(["ok", "boom", "fine"], score_fn=score_that_explodes_on("boom"))
    assert [s.text for s in scored] == ["ok", "boom", "fine"]  # nothing dropped, order kept
    failed = next(s for s in scored if s.text == "boom")
    assert failed.score == 0.0
    assert "error" in failed.rationale.lower()


# --- rank_items -------------------------------------------------------------

def test_rank_orders_by_score_desc_and_assigns_ranks():
    scored = [Scored("a", 1.0, ""), Scored("b", 3.0, ""), Scored("c", 2.0, "")]
    ranked = rank_items(scored)
    assert [(p.rank, p.text) for p in ranked] == [(1, "b"), (2, "c"), (3, "a")]


def test_rank_breaks_ties_by_text():
    scored = [Scored("beta", 5.0, ""), Scored("alpha", 5.0, "")]
    ranked = rank_items(scored)
    assert [p.text for p in ranked] == ["alpha", "beta"]


# --- prioritize (end to end, offline) --------------------------------------

def test_prioritize_composes_score_and_rank():
    ranked = prioritize(["short", "much longer text"], score_fn=score_by_length)
    assert ranked[0].text == "much longer text"
    assert ranked[0].rank == 1


# --- draft_summary ----------------------------------------------------------

def test_draft_summary_uses_top_n_only():
    priorities = [
        Priority(1, "top item", 9.0, "r1"),
        Priority(2, "mid item", 5.0, "r2"),
        Priority(3, "low item", 1.0, "r3"),
    ]
    captured = {}

    def echo_write(prompt: str) -> str:
        captured["prompt"] = prompt
        return "DRAFT"

    result = draft_summary(priorities, top_n=2, write_fn=echo_write)
    assert result == "DRAFT"
    assert "top item" in captured["prompt"]
    assert "mid item" in captured["prompt"]
    assert "low item" not in captured["prompt"]  # excluded by top_n

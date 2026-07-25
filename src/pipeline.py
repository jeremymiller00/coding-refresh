"""Week 6 deliverable (part 1) — a multi-step prioritization workflow.

This is where the capstone stops being a single model call and becomes a *pipeline*:

    ingest -> score -> rank -> draft

A key lesson of the week: a workflow with fixed steps is often more reliable and cheaper than a
fully autonomous agent. And a robust pipeline must RECOVER from a failed step (one bad item
shouldn't sink the whole run) — that's this week's self-check, pinned by the tests here.

Design note — the "expensive" steps are injected functions, so the orchestration is testable
OFFLINE with deterministic fakes:
    ScoreFn = (item text) -> (score, rationale)     # in real use: LLM-as-judge, or a heuristic
    WriteFn = (prompt) -> draft text                # in real use: your Week 2 client

What you implement (types/dataclass below are given):
- `score_items(items, *, score_fn)`   apply score_fn to each item; RECOVER from per-item failures.
- `rank_items(scored)`                pure — sort by score desc, assign ranks (deterministic ties).
- `prioritize(items, *, score_fn)`    compose the two above.
- `draft_summary(priorities, *, top_n, write_fn)`  take the top N and ask write_fn to draft.

Test:  uv run pytest week-06/test_pipeline.py     (offline — deterministic fake steps)
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

# item text -> (score, rationale)
ScoreFn = Callable[[str], tuple[float, str]]
# prompt -> drafted text
WriteFn = Callable[[str], str]


@dataclass(frozen=True)
class Scored:
    text: str
    score: float
    rationale: str


@dataclass(frozen=True)
class Priority:
    rank: int  # 1 = highest priority
    text: str
    score: float
    rationale: str


def score_items(items: list[str], *, score_fn: ScoreFn) -> list[Scored]:
    """Score every item with `score_fn`, recovering from per-item failures.

    Recovery contract (the self-check): if `score_fn` raises for an item, do NOT propagate. Record
    that item with score 0.0 and rationale ``f"error: {e}"`` and keep going. One bad item must not
    sink the batch. Every input item appears in the output, in input order.
    """
    result = []
    for item in items:
        try:
            score = score_fn(item)
            scored_item = Scored(text=item, score=score[0], rationale=score[1])
        except Exception as e:
            scored_item = Scored(text=item, score=0.0, rationale=f"error:{e}")
        result.append(scored_item)
    return result


def rank_items(scored: list[Scored]) -> list[Priority]:
    """Sort by score descending and assign ranks 1..N. Pure.

    Break ties deterministically by text ascending, so runs are reproducible.
    """
    sorted_by_text = sorted(
        scored,
        key=lambda x: x.text
    )
    sorted_by_score = sorted(
        sorted_by_text,
        key=lambda x: x.score,
        reverse=True
    )

    result = []
    for index, item in enumerate(sorted_by_score):
        result.append(Priority(
            rank=index+1,
            text=item.text,
            score=item.score,
            rationale=item.rationale
            )
        )
    return result


def prioritize(items: list[str], *, score_fn: ScoreFn) -> list[Priority]:
    """The workflow: score all items (with recovery), then rank them."""
    return rank_items(score_items(items, score_fn=score_fn))
    

def draft_summary(priorities: list[Priority], *, top_n: int, write_fn: WriteFn) -> str:
    """Build a prompt from the top-N priorities and ask `write_fn` to draft the recommendation.

    The prompt should include each top item's text/score/rationale so the draft is grounded.
    Returns whatever `write_fn` produces.
    """
    keepers = priorities[:top_n]
    priorities_prompt = ""
    for k in keepers:
        priorities_prompt += f"Rank: {str(k.rank)}\nText: {k.text}\nScore: {str(k.score)}\nRationale: {k.rationale}"

    prompt = f"""
    You are an expert analyst. 
    Draft your recommendation based on the top priorities discovered during research:

    Top Priorities:
    {priorities_prompt}"""

    return write_fn(prompt)

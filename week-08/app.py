"""Week 8 deliverable — wrap the capstone in a FastAPI service and ship it.

"Ship real agents" means it runs somewhere other than your laptop. This file is the web layer:
a typed request in, a structured result out, with an input guardrail — thin, because all the real
logic already lives in src/ (pipeline, llm_client, evals). Keep it that way.

Design note — the capstone is a FastAPI DEPENDENCY, so the app is testable OFFLINE:
    `get_capstone` provides the function that does the work. In production it returns the real,
    LLM-backed capstone (`build_capstone`). In tests you override the dependency with a fake, so
    TestClient exercises routing, validation, and the guardrail with no network. This is the same
    dependency-injection idea you've used since Week 2 — now at the HTTP boundary.

What you implement:
- `GET  /health`     -> {"status": "ok"}   (liveness probe for your host)
- `POST /prioritize` -> guardrail the inputs, call the capstone, return a PrioritizeResponse.
- `build_capstone`   -> the real wiring (pipeline + LLM). Networked; exercised manually.

Setup:  uv add "fastapi[standard]"
Run:    uv run uvicorn week-08.app:app --reload      (then POST to http://127.0.0.1:8000/prioritize)
Test:   uv run pytest week-08/test_app.py            (offline — dependency override, no network)
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from pathlib import Path

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from evals import detect_prompt_injection  # noqa: E402  (input guardrail from Week 7)
from pipeline import prioritize, draft_summary, Priority
import llm_client as llm
# import pipeline as pl

load_dotenv()

client = llm.LLMClient(model="claude-haiku-4-5")


def write(prompt: str) -> str:
    messages = llm.build_messages(prompt=prompt)
    response = client.complete(messages=messages)
    return response.text


def score(text: str) -> tuple[float, str]:
    """Generic scoring function.
    A valid scoring function depends on the use case"""
    return float(len(text)), f"len={len(text)}"


class PrioritizeRequest(BaseModel):
    items: list[str]
    top_n: int = 3


class PriorityOut(BaseModel):
    rank: int
    text: str
    score: float
    rationale: str


class PrioritizeResponse(BaseModel):
    summary: str
    priorities: list[PriorityOut]


# The capstone: items + top_n -> a structured response.
Capstone = Callable[[list[str], int], PrioritizeResponse]


def convert_priority_to_priority_out(priority: Priority) -> PriorityOut:
    return PriorityOut(
        rank=priority.rank,
        text=priority.text,
        score=priority.score,
        rationale=priority.rationale
    )


def build_capstone() -> Capstone:
    """TODO (manual/networked): return a function that runs the REAL capstone.

    Wire src/pipeline (prioritize + draft_summary) with an LLM score_fn/write_fn built from your
    Week 2 client, and shape the result into a PrioritizeResponse.
    """
    def run(items: list[str], top_n: int) -> PrioritizeResponse:
        priorities = prioritize(
            items=items,
            score_fn=score
        )

        priority_outs = [convert_priority_to_priority_out(x) for x in priorities]

        summary = draft_summary(
            priorities=priorities,
            top_n=top_n,
            write_fn=write
        )

        # do I need to cast each Priority from pipeline to PriorityOut?
        # the signatures are the same
        return PrioritizeResponse(
            summary=summary,
            priorities=priority_outs
        )

    return run


def get_capstone() -> Capstone:
    """FastAPI dependency. Overridden in tests; returns the real capstone in production."""
    return build_capstone()


app = FastAPI(title="Product Research & Prioritization Agent")


@app.get("/health")
def health() -> dict[str, str]:
    """TODO: return {"status": "ok"} so your host's liveness probe passes."""
    return {"status": "ok"}


@app.post("/prioritize", response_model=PrioritizeResponse)
def prioritize_endpoint(
    request: PrioritizeRequest,
    capstone: Capstone = Depends(get_capstone),
) -> PrioritizeResponse:
    """TODO:
    1. Guardrail: if any item trips `detect_prompt_injection`, raise HTTPException(status_code=400).
    2. Otherwise call `capstone(request.items, request.top_n)` and return its result.
    """
    all_text = ""
    for item in request.items:
        all_text += item
    if detect_prompt_injection(all_text):
        raise HTTPException(status_code=400)

    return capstone(request.items, request.top_n)

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

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from evals import detect_prompt_injection  # noqa: E402  (input guardrail from Week 7)


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


def build_capstone() -> Capstone:
    """TODO (manual/networked): return a function that runs the REAL capstone.

    Wire src/pipeline (prioritize + draft_summary) with an LLM score_fn/write_fn built from your
    Week 2 client, and shape the result into a PrioritizeResponse.
    """
    raise NotImplementedError("Wire the real capstone")


def get_capstone() -> Capstone:
    """FastAPI dependency. Overridden in tests; returns the real capstone in production."""
    return build_capstone()


app = FastAPI(title="Product Research & Prioritization Agent")


@app.get("/health")
def health() -> dict[str, str]:
    """TODO: return {"status": "ok"} so your host's liveness probe passes."""
    raise NotImplementedError("Implement /health")


@app.post("/prioritize", response_model=PrioritizeResponse)
def prioritize_endpoint(
    request: PrioritizeRequest,
    capstone: Capstone = Depends(get_capstone),
) -> PrioritizeResponse:
    """TODO:
    1. Guardrail: if any item trips `detect_prompt_injection`, raise HTTPException(status_code=400).
    2. Otherwise call `capstone(request.items, request.top_n)` and return its result.
    """
    raise NotImplementedError("Implement the /prioritize handler")

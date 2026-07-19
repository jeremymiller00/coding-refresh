"""Week 3 deliverable — reliable structured extraction with Pydantic + a validation/retry loop.

This is the capstone's ingestion layer: messy text in → a validated `Feedback` object out.
The whole point of the week is *reliability*: models return almost-JSON, wrapped in prose or code
fences, occasionally invalid. Your job is to parse defensively and re-prompt on failure instead
of crashing.

Design note — dependency injection makes this testable offline:
    `extract()` takes a `call_model` function (str prompt -> str response). In tests you pass a
    scripted fake (no network, no key). In real use you adapt your Week 2 client in one line:

        from llm_client import LLMClient, build_messages
        client = LLMClient("claude-haiku-4-5")
        call_model = lambda prompt: client.complete(build_messages(prompt)).text
        item = extract(raw_text, call_model=call_model)

What you implement (schema below is given — it's the contract the tests pin):
- `build_extraction_prompt(raw_text)`   pure — instruct the model to emit JSON matching the schema.
- `parse_response(text)`                pure — pull JSON out of the model's text and validate it.
- `extract(raw_text, *, call_model, ...)`  the loop — call, parse, and re-prompt on failure.

Setup:  uv add pydantic
Test:   uv run pytest week-03/test_extract.py     (offline — scripted fake model)
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Literal
import json

from pydantic import BaseModel, Field
import pydantic_core


# A function that takes a prompt and returns the model's raw text response.
ModelCall = Callable[[str], str]


class Feedback(BaseModel):
    """One piece of processed customer feedback — the capstone's atomic ingestion unit."""
    summary: str = Field(description="One-sentence summary of the feedback")
    sentiment: Literal["positive", "neutral", "negative"]
    themes: list[str] = Field(description="Short topical tags, e.g. 'onboarding', 'pricing'")
    feature_requests: list[str] = Field(
        default_factory=list, description="Explicit asks, empty if none"
    )
    severity: int = Field(ge=1, le=5, description="1 = trivial, 5 = blocking/critical")


class ExtractionError(RuntimeError):
    """Raised when extraction fails to produce a valid Feedback within the attempt budget."""


def build_extraction_prompt(raw_text: str) -> str:
    """Build a prompt instructing the model to return JSON matching the Feedback schema.

    Pure function. Tips: state the exact fields + allowed values, ask for JSON only, and consider
    including the schema (``Feedback.model_json_schema()``) so the model knows the shape.
    """
    feedback_schema = Feedback.model_json_schema()
    prompt_addition = f"""
    You are an expert data parser.
    You will receive customer feedback in raw text form.
    Your job is to return a correctly parsed and validated structured json object.
    You MUST return only valid JSON in the format of {feedback_schema}.
    The following fields are the only ones allowed:
    summary: (string)
    sentiment: Enum["positive", "neutral", "negative"]
    themes: List[string]
    feature_requests: List[string]
    severity (int)
    """
    return prompt_addition + "\nHere is the raw text:\n" + raw_text


def parse_response(text: str) -> Feedback:
    """Extract JSON from the model's raw text and validate it into a Feedback.

    Must tolerate real-world messiness: leading/trailing prose and ```json code fences. On invalid
    or missing JSON, let it raise (pydantic's ValidationError or a JSON error) — the loop handles it.
    """
    if "```json" in text:
        split_text = text.split("```")
        json_text = split_text[1][5:]
    else:
        json_text = text

    try:
        parsed_feedback = Feedback.model_validate_json(json_text)
        return parsed_feedback
    except pydantic_core._pydantic_core.ValidationError:
        raise


def extract(
    raw_text: str,
    *,
    call_model: ModelCall,
    max_attempts: int = 3,
) -> Feedback:
    """Extract a validated Feedback, re-prompting on parse/validation failure.    """
    prompt = build_extraction_prompt(raw_text)
    last_error = None
    for _ in range(max_attempts):
        response = call_model(prompt)
        try:
            return parse_response(response)
        except pydantic_core._pydantic_core.ValidationError as e:
            last_error = e
            prompt += f"You sent {response}, but that is wrong, please fix it. Check the instructions carefully"
    raise ExtractionError from last_error
    

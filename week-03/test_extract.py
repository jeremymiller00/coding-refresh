"""Offline tests for Week 3 extraction — no API key, no network.

A `scripted` fake model returns a canned sequence of responses, so you can drive the parser and
the validation/retry loop purely with fixtures. The real model path is exercised manually.
"""

import pytest

from extract import (
    ExtractionError,
    Feedback,
    build_extraction_prompt,
    extract,
    parse_response,
)

VALID_JSON = """
{
  "summary": "Login is slow on mobile",
  "sentiment": "negative",
  "themes": ["performance", "mobile"],
  "feature_requests": [],
  "severity": 4
}
"""

FENCED = f"Sure, here is the extraction:\n```json\n{VALID_JSON}\n```\nLet me know if you need more."

# severity out of range (6) -> must fail schema validation
INVALID_JSON = VALID_JSON.replace('"severity": 4', '"severity": 6')


def scripted(*responses: str):
    """Return a call_model that yields the given responses in order (StopIteration if overused)."""
    it = iter(responses)
    return lambda _prompt: next(it)


# --- schema (given) ---------------------------------------------------------

def test_schema_accepts_valid():
    fb = Feedback(summary="x", sentiment="neutral", themes=["a"], severity=3)
    assert fb.feature_requests == []  # default


def test_schema_rejects_bad_sentiment():
    with pytest.raises(Exception):
        Feedback(summary="x", sentiment="angry", themes=[], severity=3)


def test_schema_rejects_out_of_range_severity():
    with pytest.raises(Exception):
        Feedback(summary="x", sentiment="neutral", themes=[], severity=9)


# --- build_extraction_prompt (pure) ----------------------------------------

def test_prompt_mentions_the_text_and_fields():
    prompt = build_extraction_prompt("The app keeps crashing on upload.")
    assert "The app keeps crashing on upload." in prompt
    # It should tell the model what to produce — at least the field names.
    assert "sentiment" in prompt and "severity" in prompt


# --- parse_response (pure) --------------------------------------------------

def test_parse_plain_json():
    fb = parse_response(VALID_JSON)
    assert fb.sentiment == "negative"
    assert fb.severity == 4


def test_parse_tolerates_prose_and_code_fences():
    fb = parse_response(FENCED)
    assert fb.summary == "Login is slow on mobile"


def test_parse_raises_on_invalid():
    with pytest.raises(Exception):
        parse_response(INVALID_JSON)


# --- extract loop -----------------------------------------------------------

def test_extract_succeeds_first_try():
    fb = extract("whatever", call_model=scripted(VALID_JSON))
    assert fb.severity == 4


def test_extract_retries_then_succeeds():
    # first response invalid, second valid -> should recover
    fb = extract("whatever", call_model=scripted(INVALID_JSON, VALID_JSON), max_attempts=3)
    assert fb.sentiment == "negative"


def test_extract_gives_up_after_max_attempts():
    with pytest.raises(ExtractionError):
        extract("whatever", call_model=scripted(INVALID_JSON, INVALID_JSON), max_attempts=2)

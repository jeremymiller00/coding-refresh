"""Week 7 deliverable — an eval harness, a regression gate, and a guardrail.

This is the engineering discipline that separates a demo from a shipped product, and it's the
highest-leverage skill for a PM who ships agents: you can't manage what you can't measure.

Three offline-testable pieces here:
- `run_evals`               run the system under test over a dataset and score each case.
- `check_regression`        did a change make the mean score WORSE (beyond tolerance)? -> gate CI.
- `detect_prompt_injection` one input guardrail (injection awareness).

Design note — both the system and the judge are injected, so the harness is testable OFFLINE:
    RunFn   = (input) -> output          # in real use: your capstone agent
    JudgeFn = (output, reference) -> score in [0, 1]
                                         # in real use: LLM-as-judge (a model scoring the output)
    In tests you pass deterministic fakes. The manual runner (week-07/run_evals.py) wires the real
    agent + a real LLM judge and hits your dataset.

Test:  uv run pytest week-07/test_evals.py     (offline — deterministic fake system + judge)
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

RunFn = Callable[[str], str]  # system under test: input -> output
JudgeFn = Callable[[str, str], float]  # (output, reference) -> score in [0, 1]


@dataclass(frozen=True)
class EvalCase:
    id: str
    input: str
    reference: str  # the expected answer / grading rubric anchor


@dataclass(frozen=True)
class CaseResult:
    id: str
    output: str
    score: float
    passed: bool


@dataclass(frozen=True)
class Report:
    results: list[CaseResult]
    mean_score: float
    pass_rate: float  # fraction of cases that passed, in [0, 1]


def run_evals(
    cases: list[EvalCase],
    *,
    run_fn: RunFn,
    judge_fn: JudgeFn,
    threshold: float = 0.5,
) -> Report:
    """Run every case through `run_fn`, grade it with `judge_fn`, and aggregate.

    Per case: output = run_fn(input); score = judge_fn(output, reference); passed = score >= threshold.
    Report: mean_score = average score, pass_rate = fraction passed. Empty input -> (0.0, 0.0).
    """
    raise NotImplementedError("Implement run_evals")


def check_regression(report: Report, *, baseline: float, tolerance: float = 0.0) -> bool:
    """Return True if the run REGRESSED: mean_score dropped below (baseline - tolerance).

    This is the CI gate — a prompt change that lowers the score beyond tolerance should fail the
    build. It's also the week's self-check: quantifying better-or-worse instead of eyeballing it.
    """
    raise NotImplementedError("Implement check_regression")


# A few common prompt-injection markers. Real guardrails are fuzzier; this teaches the idea.
_INJECTION_MARKERS = (
    "ignore previous instructions",
    "ignore all previous",
    "disregard the above",
    "reveal your system prompt",
    "reveal your instructions",
)


def detect_prompt_injection(text: str) -> bool:
    """Return True if `text` looks like a prompt-injection attempt (case-insensitive marker match).

    An input guardrail: you'd run this before feeding untrusted text (e.g. scraped feedback) to the
    model, and flag/quarantine rather than execute it.
    """
    raise NotImplementedError("Implement detect_prompt_injection")

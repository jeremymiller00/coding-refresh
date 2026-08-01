"""Week 7 manual runner — score the real capstone against the dataset and gate on regression.

Offline logic lives in src/evals.py (unit-tested). This script is the networked wiring: it loads the
dataset, runs your real agent as `run_fn`, uses a real LLM-as-judge as `judge_fn`, prints a report,
and exits non-zero if the score regressed against a stored baseline — so it can gate CI.

Setup:  (uses your Week 2 client; no extra deps)
Run:    uv run python week-07/run_evals.py

Fill in the TODOs.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from evals import EvalCase, check_regression, run_evals  # noqa: E402

DATASET = Path(__file__).parent / "evals" / "dataset.jsonl"
BASELINE = 0.75  # update this when a genuine improvement raises the bar


def load_cases(path: Path) -> list[EvalCase]:
    cases = []
    for line in path.read_text().splitlines():
        if line.strip():
            row = json.loads(line)
            cases.append(EvalCase(id=row["id"], input=row["input"], reference=row["reference"]))
    return cases


def run_fn(text: str) -> str:
    """TODO: run the real capstone on `text` and return its output string.

    e.g. extract(text, call_model=...) and return the sentiment, or run the full agent.
    """
    raise NotImplementedError("Wire run_fn to your capstone")


def judge_fn(output: str, reference: str) -> float:
    """TODO: LLM-as-judge — ask a model whether `output` matches `reference`, return a score in [0,1].

    Keep the judge prompt tight (rubric + 'reply only 0 or 1'). Parse its reply into a float.
    """
    raise NotImplementedError("Wire judge_fn to an LLM judge")


def main() -> int:
    cases = load_cases(DATASET)
    report = run_evals(cases, run_fn=run_fn, judge_fn=judge_fn, threshold=0.5)

    print(f"mean_score={report.mean_score:.3f}  pass_rate={report.pass_rate:.0%}  (baseline={BASELINE})")
    for r in report.results:
        print(f"  {'PASS' if r.passed else 'FAIL'}  {r.id:20s} score={r.score:.2f}")

    regressed = check_regression(report, baseline=BASELINE, tolerance=0.05)
    if regressed:
        print("REGRESSION: score dropped below baseline.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

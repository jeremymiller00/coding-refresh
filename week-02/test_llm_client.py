"""Offline tests for the pure parts of the Week 2 client — no API key needed.

These pin the cost math and message assembly so you can TDD them before touching the network.
The `complete`/`stream` methods need a live provider and are exercised manually via cli.py.
"""

import pytest

from llm_client import Message, build_messages, estimate_cost
import cli


def test_estimate_cost_basic():
    # 1000 input @ $3/Mtok + 500 output @ $15/Mtok = 0.003 + 0.0075
    cost = estimate_cost(1000, 500, input_per_mtok=3.0, output_per_mtok=15.0)
    assert cost == pytest.approx(0.0105)


def test_estimate_cost_zero():
    assert estimate_cost(0, 0, input_per_mtok=3.0, output_per_mtok=15.0) == 0.0


def test_build_messages_user_only():
    assert build_messages("hi") == [Message(role="user", content="hi")]


def test_build_messages_with_system():
    msgs = build_messages("hi", system="be terse")
    assert msgs == [
        Message(role="system", content="be terse"),
        Message(role="user", content="hi"),
    ]


@pytest.mark.integration
def test_cli():
    """Convenience test for debugger"""
    prompt = ["what is 2 plus 3"]
    cli.main(prompt)


@pytest.mark.integration
def test_cli_agent():
    """Convenience test for debugger"""
    prompt = ["what is 2 plus 3", "--agent"]
    cli.main(prompt)

"""Offline tests for the hand-rolled agent loop — no API key, no network.

Tools are real (tiny) Python functions. The "model" is a fake function that inspects the
conversation and decides what to do next, which lets us prove the loop actually feeds tool
results back into the conversation.
"""

import pytest

from agent_loop import AgentError, Tool, ToolCall, Turn, execute_tool, run_agent

# --- real tools -------------------------------------------------------------

def _add(a: int, b: int) -> str:
    return str(a + b)


def _boom() -> str:
    raise ValueError("kaboom")


ADD = Tool(
    name="add",
    description="Add two integers",
    input_schema={"type": "object", "properties": {"a": {"type": "integer"}, "b": {"type": "integer"}}},
    fn=_add,
)
BOOM = Tool(name="boom", description="Always fails", input_schema={"type": "object"}, fn=_boom)
TOOLS = [ADD, BOOM]


def _last_tool_result(convo: list[Turn]) -> str | None:
    results = [t.content for t in convo if t.role == "tool"]
    return results[-1] if results else None


# --- execute_tool -----------------------------------------------------------

def test_execute_tool_success():
    assert execute_tool(ToolCall("c1", "add", {"a": 2, "b": 3}), TOOLS) == "5"


def test_execute_tool_unknown_name_returns_error_not_raise():
    out = execute_tool(ToolCall("c1", "nope", {}), TOOLS)
    assert "nope" in out.lower() or "unknown" in out.lower()


def test_execute_tool_captures_exception():
    out = execute_tool(ToolCall("c1", "boom", {}), TOOLS)
    assert "kaboom" in out  # error fed back as a string, not raised


# --- run_agent --------------------------------------------------------------

def test_returns_final_answer_immediately():
    def model(convo, tools):
        return Turn(role="assistant", content="done")

    assert run_agent("hi", tools=TOOLS, model=model) == "done"


def test_tool_result_is_fed_back():
    # First turn asks for add(2,3); second turn echoes the tool result it received.
    def model(convo, tools):
        if _last_tool_result(convo) is None:
            return Turn(role="assistant", tool_calls=[ToolCall("c1", "add", {"a": 2, "b": 3})])
        return Turn(role="assistant", content=f"the answer is {_last_tool_result(convo)}")

    assert run_agent("add 2 and 3", tools=TOOLS, model=model) == "the answer is 5"


def test_recovers_from_tool_error():
    def model(convo, tools):
        result = _last_tool_result(convo)
        if result is None:
            return Turn(role="assistant", tool_calls=[ToolCall("c1", "boom", {})])
        return Turn(role="assistant", content=f"handled: {result}")

    out = run_agent("do the thing", tools=TOOLS, model=model)
    assert out.startswith("handled:") and "kaboom" in out


def test_raises_after_max_steps():
    def never_finishes(convo, tools):
        return Turn(role="assistant", tool_calls=[ToolCall("c", "add", {"a": 1, "b": 1})])

    with pytest.raises(AgentError):
        run_agent("loop forever", tools=TOOLS, model=never_finishes, max_steps=3)

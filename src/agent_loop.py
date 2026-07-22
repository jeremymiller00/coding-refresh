"""Week 4 deliverable (part 1) — the agent loop, hand-rolled.

The whole of "an agent" is this cycle:
    model -> (maybe) tool call -> execute tool -> feed result back -> repeat -> final answer

Build it yourself here so you understand exactly what a framework does for you. Next, rebuild the
same task with a framework in week-04/agent_framework.py and compare.

Design note — the model is injected as a function so the loop is testable OFFLINE:
    ModelFn = (conversation, tools) -> assistant Turn
    A `Turn` with tool_calls means "run these"; a Turn with no tool_calls is the final answer.
    In tests you pass a scripted fake (no network). In real use you adapt your Week 2 client:
    enable tools in the request, and translate Anthropic `tool_use` content blocks into ToolCall
    objects (and ToolResult turns back into `tool_result` blocks). That translation is the
    "wire it up" exercise — see week-04/README.

What you implement (the dataclasses and types below are given):
- `execute_tool(call, tools)`   pure — look up + run one tool, returning a string. Errors become
                                strings (so the model can see them and recover), never exceptions.
- `run_agent(prompt, *, tools, model, max_steps)`  the loop itself, with a max-steps guard.

Test:  uv run pytest week-04/test_agent_loop.py     (offline — scripted fake model + real tools)
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Literal

Role = Literal["user", "assistant", "tool"]


@dataclass(frozen=True)
class Tool:
    """A tool the agent can call: a JSON-schema description plus the Python function behind it."""
    name: str
    description: str
    input_schema: dict[str, Any]  # JSON schema for the arguments
    fn: Callable[..., str]  # called as fn(**arguments); returns a string result


@dataclass(frozen=True)
class ToolCall:
    id: str
    name: str
    arguments: dict[str, Any]


@dataclass
class Turn:
    """One entry in the running conversation.

    - user/assistant content turns use `content`.
    - an assistant turn that wants tools carries `tool_calls` (and is NOT final).
    - a tool-result turn has role="tool", the result in `content`, and the originating `tool_call_id`.
    """
    role: Role
    content: str | list[dict] = None
    tool_calls: list[ToolCall] = field(default_factory=list)
    tool_call_id: str | None = None


# Given a conversation and the available tools, return the assistant's next Turn.
ModelFn = Callable[[list[Turn], list[Tool]], Turn]


class AgentError(RuntimeError):
    """Raised when the agent can't reach a final answer within the step budget."""


def execute_tool(call: ToolCall, tools: list[Tool]) -> str:
    """Run the tool named by `call` with its arguments and return a string result.

    Rules:
    - Unknown tool name -> return an error string (list what IS available). Do not raise.
    - The tool function raising -> catch it and return an error string containing the message.
      (Feeding errors back lets the model recover instead of the whole agent crashing.)
    """
    available_tools = [tool.name for tool in tools]
    for tool in tools:
        if call.name == tool.name:
            try:
                return tool.fn(**call.arguments)
            except Exception as e:
                return str(e)
         
    return f"Unknown tool call: {call.name}\nAvailable tools: {available_tools}"


def run_agent(
    prompt: str,
    *,
    tools: list[Tool],
    model: ModelFn,
    max_steps: int = 10,
) -> str:
    """Drive the agent loop to a final answer.

    Sketch:
        convo = [Turn(role="user", content=prompt)]
        for _ in range(max_steps):
            assistant = model(convo, tools)
            convo.append(assistant)
            if not assistant.tool_calls:      # no tools requested -> final answer
                return assistant.content
            for call in assistant.tool_calls:
                result = execute_tool(call, tools)
                convo.append(Turn(role="tool", content=result, tool_call_id=call.id))
        raise AgentError(f"No final answer within {max_steps} steps")
    """
    convo = [Turn(role="user", content=prompt)]
    for _ in range(max_steps):
        assistant_response = model(convo, tools)
        convo.append(assistant_response)
        if not assistant_response.tool_calls:
            return assistant_response.content
        for call in assistant_response.tool_calls:
            tool_result = execute_tool(call, tools)
            convo.append(Turn(role="tool", content=tool_result, tool_call_id=call.id))
    raise AgentError(f"No final answer withing {max_steps} steps")

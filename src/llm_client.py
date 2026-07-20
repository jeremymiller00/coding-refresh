"""Week 2 deliverable — a thin, provider-agnostic LLM client.

This wrapper is reused by every later week, so keep the *interface* portable even though the
first implementation will target one provider (Anthropic is the default for this curriculum).

What you implement here:
- `estimate_cost`     pure function — token math. Testable offline (no API key). Do this FIRST.
- `build_messages`    pure helper — assemble the messages list. Also offline-testable.
- `LLMClient.complete`  one-shot call returning text + usage + cost.
- `LLMClient.stream`    streaming call yielding text chunks as they arrive.
- `_call_with_retries`  wrap a request with exponential backoff on rate-limit/timeout.

Run the offline tests first:  uv run pytest week-02/test_llm_client.py
Then wire the real calls and try the CLI:  uv run python week-02/cli.py "Hello"

Notes:
- Load the API key from the environment (`.env` via python-dotenv). Never hardcode it.
- `PRICING` below is a placeholder — look up *current* per-million-token prices in the provider
  docs (see RESOURCES.md) and fill it in. Prices change; don't trust memory.
"""

from __future__ import annotations

from agent_loop import Tool, ToolCall, Turn

import time
from collections.abc import Iterator
from dataclasses import dataclass, asdict
from typing import Literal, Any
from os import getenv
import json
from functools import wraps
import requests
from dotenv import load_dotenv
load_dotenv()

Role = Literal["system", "user", "assistant"]


@dataclass(frozen=True)
class Message:
    role: Role
    content: str


@dataclass(frozen=True)
class Pricing:
    """Per-million-token prices in USD."""
    input_per_mtok: float
    output_per_mtok: float


# TODO: fill in from current provider docs (per *million* tokens).
PRICING: dict[str, Pricing] = {
    "claude-haiku-4-5": Pricing(input_per_mtok=1, output_per_mtok=5),
    "claude-sonnet-5": Pricing(input_per_mtok=3, output_per_mtok=15)
}


@dataclass(frozen=True)
class LLMResponse:
    text: str
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float


def estimate_cost(
    input_tokens: int,
    output_tokens: int,
    *,
    input_per_mtok: float,
    output_per_mtok: float,
) -> float:
    """Return the USD cost of a call given token counts and per-million-token prices.

    Pure function — no I/O. This is the first thing to implement (the tests pin the math).
    """
    return ((input_tokens * input_per_mtok) + (output_tokens * output_per_mtok)) / 1000000


def build_messages(prompt: str, *, system: str | None = None) -> list[Message]:
    """Assemble the message list for a single-turn prompt.

    If `system` is given, it should be the first message with role "system".
    Pure function — offline-testable.
    """
    messages = []
    if system is not None:
        messages.append(Message(role="system", content=system))
    messages.append(Message(role="user",  content=prompt))
    return messages


def call_with_retries(fn):  # type: ignore[no-untyped-def]
    """Run `fn()` with exponential backoff on transient errors (rate limit / timeout)."""

    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        for attempt in range(self.max_retries):
            try:
                return fn(self, *args, **kwargs)
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                if attempt == self.max_retries - 1:
                    raise
                time.sleep(self.base_delay * 2**attempt)
    return wrapper


class LLMClient:
    """Provider-agnostic client. The public methods are the stable contract later weeks rely on."""

    def __init__(
        self,
        model: str,
        *,
        max_retries: int = 5,
        base_delay: float = 0.5,
        api_key: str = None
    ) -> None:
        self.model = model
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.headers = {
            'anthropic-version': '2023-06-01',
            'X-Api-Key': getenv("ANTHROPIC_API_KEY")
            }

    @call_with_retries
    def agent_complete(
        self,
        convo: list[Turn],
        tools: list[Tool] = []
    ) -> LLMResponse:
        """
        One-shot agentic completion.
        May return tool calls.
        """
       
        payload = self._build_payload(
            messages=convo,
            max_tokens=1024,
            temperature=1.0,
            tools=tools,
            stream=False
        )

        # anthropic api requires sys prompt as a separate parameter
        payload = self._set_sys_prompt_parameter(
            payload=payload,
            messages=convo,
        )

        try:
            response = requests.post(
                url="https://api.anthropic.com/v1/messages",
                headers=self.headers,
                json=payload
                )
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            raise

        json_response = response.json()
        stop_reason = json_response.get("stop_reason")
        # if tool call, return tool call
        if stop_reason == "tool_use":
            id = json_response.get("content")[-1].get("id")
            name = json_response.get("content")[-1].get("name")
            input = json_response.get("content")[-1].get("input")

            return Turn(
                role="assistant",
                content=[{
                    "type": "tool_use",
                    "id": id,
                    "name": name,
                    "input": input
                    }],
                tool_calls=[ToolCall(id=id, name=name, arguments=input)]
            )

        elif stop_reason in ["end_turn", "stop_sequence", "max_tokens", "refusal"]:
            return Turn(
                role="assistant",
                content=json_response.get("content")[-1].get("text")
            )

    @call_with_retries
    def complete(
        self,
        messages: list[Message],
        *,
        max_tokens: int = 1024,
        temperature: float = 1.0
    ) -> LLMResponse:
        """One-shot completion. Returns text plus token usage and computed cost."""

        payload = self._build_payload(
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=False
        )

        # anthropic api requires sys prompt as a separate parameter
        payload = self._set_sys_prompt_parameter(
            payload=payload,
            messages=messages,
        )

        try:
            response = requests.post(
                url="https://api.anthropic.com/v1/messages",
                headers=self.headers,
                json=payload
                )
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            raise

        json_response = response.json()
        input_tokens = json_response.get("usage").get("input_tokens")
        output_tokens = json_response.get("usage").get("output_tokens")
        cost = estimate_cost(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            input_per_mtok=PRICING.get(self.model).input_per_mtok,
            output_per_mtok=PRICING.get(self.model).output_per_mtok
        )
        text_response = json_response.get("content")[0].get("text")
        return LLMResponse(
            text=text_response,
            model=self.model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=cost)

    @call_with_retries
    def stream(
        self,
        messages: list[Message],
        *,
        max_tokens: int = 1024,
        temperature: float = 1.0,
    ) -> Iterator[str]:
        """Stream the completion, yielding text chunks as they arrive."""

        payload = self._build_payload(
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            )

        # anthropic api requires sys prompt as a separate parameter
        payload = self._set_sys_prompt_parameter(
            payload=payload,
            messages=messages,
        )

        try:
            response = requests.post(
                url="https://api.anthropic.com/v1/messages",
                headers=self.headers,
                json=payload,
                stream=True
                )
        except requests.exceptions.HTTPError:
            raise

        for line in response.iter_lines(decode_unicode=True):
            if line:
                # print(line + "\n")
                if line[:4] == "data":
                    clean_line = json.loads(line[6:])

                    # yield text response chunk
                    if clean_line.get("type") == "content_block_delta":
                        if clean_line.get("delta").get("type") == "text_delta":
                            yield clean_line.get("delta").get("text")
    
                    # end of message summary
                    elif clean_line.get("type") == "message_delta":
                        input_tokens = clean_line.get("usage").get("input_tokens")
                        output_tokens = clean_line.get("usage").get("output_tokens")
                        cost = estimate_cost(
                            input_tokens=input_tokens,
                            output_tokens=output_tokens,
                            input_per_mtok=PRICING.get(self.model).input_per_mtok,
                            output_per_mtok=PRICING.get(self.model).output_per_mtok
                        )
                        yield LLMResponse(
                            text="",
                            model=self.model,
                            input_tokens=input_tokens,
                            output_tokens=output_tokens,
                            cost_usd=cost
                        )

    def _build_payload(
        self,
        messages: list[Turn],
        max_tokens: int = 1024,
        temperature: float = 1.0,
        tools: list[Tool] = None,
        stream: bool = True
    ) -> dict[str, any]:
        payload = {
            "max_tokens": max_tokens,
            "temperature": temperature,
            "model": self.model,
            "stream": stream,
            # "messages": messages
            "messages": [{"role": message.role, "content": message.content} for message in messages if message.role.lower() != "system"]
        }

        if tools:
            prepped_tools = self._prep_tools_for_payload(tools)
            payload.update({"tools": prepped_tools})

        return payload

    def _prep_tools_for_payload(self, tools: list[Tool]):
        prepped_tools = []
        for tool in tools:
            tool_as_dict = asdict(tool)
            prepped = {k: v for k, v in tool_as_dict.items() if k != "fn"}
            prepped_tools.append(prepped)
        return prepped_tools

    def _set_sys_prompt_parameter(
            self,
            payload: dict[str, Any],
            messages: list[Message],
            sys_prompt: None = None
    ) -> dict[str, Any]:
        """ Required for Anthropic messages API"""
        for message in messages:
            if message.role.lower() == "system":
                sys_prompt = message.content
                break

        if sys_prompt:
            payload.update({"system": [{"text": sys_prompt, "type": "text"}]})

        return payload

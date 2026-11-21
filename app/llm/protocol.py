from typing import Any

from pydantic import BaseModel, Field


class ToolCall(BaseModel):
    """
    Represents a request from the LLM to execute a tool.
    """

    id: str
    name: str
    arguments: dict[str, Any] = Field(default_factory=dict)


class ToolResult(BaseModel):
    """
    Represents the result of executing a tool.
    """

    tool_call_id: str
    tool_name: str

    success: bool

    result: Any = None
    error: str | None = None


class LLMResponse(BaseModel):
    """
    Standardized response returned by any LLM provider.
    """

    content: str | None = None

    tool_calls: list[ToolCall] = Field(
        default_factory=list
    )

    finish_reason: str | None = None

    provider: str
    model: str | None = None

    raw_response: Any = None
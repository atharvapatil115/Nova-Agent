from typing import Any, Callable

from app.llm.protocol import ToolResult


class ToolRegistry:

    def __init__(self):
        self._tools: dict[str, Callable] = {}
        self._definitions: dict[str, dict[str, Any]] = {}

    def register(
        self,
        name: str,
        function: Callable,
        definition: dict[str, Any],
    ):
        """
        Register a tool that the agent can use.
        """

        self._tools[name] = function
        self._definitions[name] = definition

    def get_definitions(self) -> list[dict[str, Any]]:
        """
        Return tool definitions that can be sent to the LLM.
        """

        return list(self._definitions.values())

    async def execute(
        self,
        tool_call_id: str,
        name: str,
        arguments: dict[str, Any],
    ) -> ToolResult:

        tool = self._tools.get(name)

        if tool is None:
            return ToolResult(
                tool_call_id=tool_call_id,
                tool_name=name,
                success=False,
                error=f"Unknown tool: {name}",
            )

        try:

            result = tool(**arguments)

            if hasattr(result, "__await__"):
                result = await result

            return ToolResult(
                tool_call_id=tool_call_id,
                tool_name=name,
                success=True,
                result=result,
            )

        except Exception as exc:

            return ToolResult(
                tool_call_id=tool_call_id,
                tool_name=name,
                success=False,
                error=str(exc),
            )
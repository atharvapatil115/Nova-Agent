import json
import os

from groq import AsyncGroq

from app.llm.base import LLMAdapter
from app.llm.protocol import LLMResponse, ToolCall


class GroqAdapter(LLMAdapter):

    def __init__(self):
        self.client = AsyncGroq(
            api_key=os.getenv("GROQ_API_KEY")
        )

        self.model = "openai/gpt-oss-120b"

    @property
    def name(self) -> str:
        return "groq"

    async def generate(
        self,
        messages,
        tools=None,
    ) -> LLMResponse:

        kwargs = {
            "model": self.model,
            "messages": messages,
        }

        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"

        response = await self.client.chat.completions.create(
            **kwargs
        )

        message = response.choices[0].message

        tool_calls = []

        if message.tool_calls:

            for tool_call in message.tool_calls:

                try:
                    arguments = json.loads(
                        tool_call.function.arguments
                    )
                except json.JSONDecodeError:
                    arguments = {}

                tool_calls.append(
                    ToolCall(
                        id=tool_call.id,
                        name=tool_call.function.name,
                        arguments=arguments,
                    )
                )

        return LLMResponse(
            content=message.content,
            tool_calls=tool_calls,
            finish_reason=response.choices[0].finish_reason,
            provider=self.name,
            model=self.model,
            raw_response=response,
        )

    async def health_check(self) -> bool:

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": "Reply with OK.",
                    }
                ],
                max_tokens=5,
            )

            return bool(response.choices)

        except Exception as exc:

            print(
                f"[Groq] health check failed: {exc}"
            )

            return False
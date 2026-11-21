import json
import os

from openai import AsyncOpenAI

from app.llm.base import LLMAdapter
from app.llm.protocol import LLMResponse, ToolCall


class OpenRouterAdapter(LLMAdapter):

    def __init__(self):
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
        )

        self.model = "openai/gpt-6.2-astra-pro"

    @property
    def name(self) -> str:
        return "openrouter"

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
                f"[OpenRouter] health check failed: {exc}"
            )

            return False
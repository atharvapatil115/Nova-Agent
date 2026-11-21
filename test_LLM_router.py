import asyncio

from app.llm.router import LLMRouter
from app.llm.providers.groq import GroqAdapter
from app.llm.providers.openrouter import OpenRouterAdapter
from app.llm.providers.antigravity import AntigravityAdapter


async def main():

    providers = [
        AntigravityAdapter(),
        GroqAdapter(),
        OpenRouterAdapter(),
    ]

    router = LLMRouter(providers)

    provider = await router.get_available_provider()

    print()
    print("=" * 50)
    print(f"SELECTED PROVIDER: {provider.name}")
    print("=" * 50)

    response = await provider.generate(
        messages=[
            {
                "role": "user",
                "content": "In one sentence, explain what an AI agent is."
            }
        ]
    )

    print()
    print()
    print("LLM RESPONSE:")
    print(response.content)

    print()
    print("TOOL CALLS:")
    print(response.tool_calls)


if __name__ == "__main__":
    asyncio.run(main())
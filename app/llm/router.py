from app.llm.base import LLMAdapter


class LLMRouter:

    def __init__(
        self,
        providers: list[LLMAdapter],
    ):
        self.providers = providers

    async def get_available_provider(self):
        for provider in self.providers:

            print(
                f"[LLM Router] Checking {provider.name}..."
            )

            available = await provider.health_check()

            if available:
                print(
                    f"[LLM Router] Selected {provider.name}"
                )

                return provider

            print(
                f"[LLM Router] {provider.name} unavailable"
            )

        raise RuntimeError(
            "No LLM providers are currently available."
        )
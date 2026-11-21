from app.llm.base import LLMAdapter


class AntigravityAdapter(LLMAdapter):

    @property
    def name(self) -> str:
        return "antigravity"

    async def generate(
        self,
        messages,
        tools=None,
    ):
        raise NotImplementedError(
            "Antigravity adapter will be implemented "
            "after authentication/runtime verification."
        )

    async def health_check(self) -> bool:
        return False
from abc import ABC, abstractmethod
from typing import Any


class LLMAdapter(ABC):

    @abstractmethod
    async def generate(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ):
        """
        Generate a response from the LLM.
        """
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """
        Check whether the provider is currently available.
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Human-readable provider name.
        """
        pass
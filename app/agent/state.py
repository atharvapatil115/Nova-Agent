from pydantic import BaseModel, Field


class AgentState(BaseModel):
    user_input: str = ""

    conversation_history: list[dict] = Field(
        default_factory=list
    )

    pending_action: str | None = None

    pending_confirmation: bool = False

    pending_data: dict = Field(
        default_factory=dict
    )
import json

from app.agent.tools.registry import ToolRegistry
from app.agent.prompts import SYSTEM_PROMPT
from app.agent.state import AgentState

from app.gmail.definitions import (
    READ_UNREAD_EMAILS_DEFINITION,
    COMPOSE_EMAIL_TOOL,
)

from app.gmail.tools import (
    read_unread_emails,
    compose_email,
)

from app.llm.protocol import LLMResponse, ToolResult
from app.llm.router import LLMRouter
from app.llm.providers.groq import GroqAdapter
from app.llm.providers.openrouter import OpenRouterAdapter
from app.llm.providers.antigravity import AntigravityAdapter


class MailAgent:

    def __init__(self):

        # -------------------------------------------------
        # TOOL REGISTRY
        # -------------------------------------------------

        self.tool_registry = ToolRegistry()

        self.tool_registry.register(
            name="read_unread_emails",
            function=read_unread_emails,
            definition=READ_UNREAD_EMAILS_DEFINITION,
        )

        self.tool_registry.register(
            name="compose_email",
            function=compose_email,
            definition=COMPOSE_EMAIL_TOOL,
        )

        # -------------------------------------------------
        # LLM ROUTER
        # -------------------------------------------------

        self.llm_router = LLMRouter(
            providers=[
                AntigravityAdapter(),
                GroqAdapter(),
                OpenRouterAdapter(),
            ]
        )

        self.provider = None

        # -------------------------------------------------
        # PERSISTENT AGENT STATE
        # -------------------------------------------------

        self.state = AgentState()

        # Conversation history survives wake-word cycles.
        self.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]

    async def start(self, user_input: str):

        # -------------------------------------------------
        # UPDATE STATE
        # -------------------------------------------------

        self.state.user_input = user_input

        # Add user's message to persistent conversation.
        self.messages.append(
            {
                "role": "user",
                "content": user_input,
            }
        )

        # -------------------------------------------------
        # ADD PENDING TASK CONTEXT
        # -------------------------------------------------

        if self.state.pending_action:

            pending_context = {
                "pending_action": self.state.pending_action,
                "pending_data": self.state.pending_data,
            }

            self.messages.append(
                {
                    "role": "system",
                    "content": (
                        "IMPORTANT: The user is continuing a previously "
                        "started task.\n\n"
                        f"Pending task state:\n"
                        f"{json.dumps(pending_context, indent=2)}\n\n"
                        "Interpret the user's latest message as a continuation "
                        "of this task unless the user clearly starts a new task."
                    ),
                }
            )

        # -------------------------------------------------
        # GET LLM PROVIDER
        # -------------------------------------------------

        if self.provider is None:
            self.provider = (
                await self.llm_router.get_available_provider()
            )

        # -------------------------------------------------
        # AGENT LOOP
        # -------------------------------------------------

        while True:

            response: LLMResponse = await self.provider.generate(
                messages=self.messages,
                tools=self.tool_registry.get_definitions(),
            )

            # -------------------------------------------------
            # NO TOOL CALL
            # -------------------------------------------------

            if not response.tool_calls:

                assistant_message = {
                    "role": "assistant",
                    "content": response.content,
                }

                self.messages.append(assistant_message)

                return response.content

            # -------------------------------------------------
            # ASSISTANT TOOL CALL MESSAGE
            # -------------------------------------------------

            assistant_message = {
                "role": "assistant",
                "content": response.content,
                "tool_calls": [
                    {
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_call.name,
                            "arguments": json.dumps(
                                tool_call.arguments
                            ),
                        },
                    }
                    for tool_call in response.tool_calls
                ],
            }

            self.messages.append(
                assistant_message
            )

            # -------------------------------------------------
            # EXECUTE TOOLS
            # -------------------------------------------------

            for tool_call in response.tool_calls:

                print(
                    f"[Agent] Calling tool: {tool_call.name}"
                )

                tool_result: ToolResult = (
                    await self.tool_registry.execute(
                        tool_call_id=tool_call.id,
                        name=tool_call.name,
                        arguments=tool_call.arguments,
                    )
                )

                # ---------------------------------------------
                # STORE PENDING EMAIL INFORMATION
                # ---------------------------------------------

                if (
                    tool_call.name == "compose_email"
                    and tool_result.success
                ):

                    # Task is complete.
                    self.state.pending_action = None
                    self.state.pending_data = {}

                # ---------------------------------------------
                # TOOL RESULT
                # ---------------------------------------------

                self.messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_result.tool_call_id,
                        "name": tool_result.tool_name,
                        "content": str(
                            tool_result.result
                            if tool_result.success
                            else tool_result.error
                        ),
                    }
                )
import asyncio

from app.agent.tools.registry import ToolRegistry
from app.gmail.tools import read_unread_emails
from app.gmail.definitions import (
    READ_UNREAD_EMAILS_DEFINITION,
    COMPOSE_EMAIL_TOOL,
)

from app.gmail.tools import (
    read_unread_emails,
    compose_email,
)

async def main():

    registry = ToolRegistry()

    registry.register(
        name="read_unread_emails",
        function=read_unread_emails,
        definition=READ_UNREAD_EMAILS_DEFINITION,
    )
    registry.register(
    name="compose_email",
    function=compose_email,
    definition=COMPOSE_EMAIL_TOOL,
)

    print("=" * 60)
    print("AVAILABLE TOOLS")
    print("=" * 60)

    for tool in registry.get_definitions():
        print(tool)

    print()
    print("=" * 60)
    print("EXECUTING GMAIL TOOL")
    print("=" * 60)

    result = await registry.execute(
        tool_call_id="gmail_test_001",
        name="read_unread_emails",
        arguments={
            "limit": 2,
        },
    )

    print(result)


if __name__ == "__main__":
    asyncio.run(main())
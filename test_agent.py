import asyncio

from app.agent.agent import MailAgent


async def main():

    agent = MailAgent()

    response = await agent.start(
        "Check my unread emails and tell me what I have."
    )

    print()
    print("=" * 60)
    print("FINAL AGENT RESPONSE")
    print("=" * 60)
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
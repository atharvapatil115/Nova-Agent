import asyncio
from dotenv import load_dotenv

from app.voice.wake_word import WakeWordListener
from app.voice.input import VoiceInput
from app.agent.agent import MailAgent
from app.voice.output import VoiceOutput

load_dotenv()


async def handle_command(agent, voice, voice_output):

    print()
    print("🎙️ Nova is listening for your command...")

    filename = voice.record(duration=5)

    text = await voice.transcribe(filename)

    print()
    print("=" * 60)
    print("YOU SAID")
    print("=" * 60)
    print(text)

    if not text:
        print("No command detected.")
        return

    print()
    print("🧠 Nova is thinking...")

    response = await agent.start(text)

    print()
    print("=" * 60)
    print("NOVA")
    print("=" * 60)
    print(response)

    print()
    print("🔊 Nova is speaking...")

    voice_output.speak(response)

async def main():

    agent = MailAgent()
    voice = VoiceInput()
    voice_output = VoiceOutput()
    listener = WakeWordListener(
        wake_word="hey_jarvis",
        threshold=0.5,
    )

    while True:

        listener.wait_for_wake()

        await handle_command(
            agent,
            voice,
            voice_output
        )

        print()
        print("🔄 Returning to wake-word listening...")


if __name__ == "__main__":
    asyncio.run(main())
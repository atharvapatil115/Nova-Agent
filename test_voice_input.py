import asyncio

from dotenv import load_dotenv

from app.voice.input import VoiceInput


async def main():

    load_dotenv()

    voice = VoiceInput()

    filename = voice.record(duration=5)

    text = await voice.transcribe(filename)

    print()
    print("=" * 60)
    print("TRANSCRIPTION")
    print("=" * 60)
    print(text)


if __name__ == "__main__":
    asyncio.run(main())
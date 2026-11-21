import os
import wave

import sounddevice as sd
from groq import AsyncGroq
from dotenv import load_dotenv

load_dotenv()

class VoiceInput:

    def __init__(self):
        self.client = AsyncGroq(
            api_key=os.getenv("GROQ_API_KEY")
        )

        self.sample_rate = 16000
        self.channels = 1

    def record(
        self,
        filename: str = "input.wav",
        duration: int = 5,
    ):
        print()
        print("🎤 Listening...")

        audio = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="int16",
        )

        sd.wait()

        print("🎤 Recording finished.")

        with wave.open(filename, "wb") as wav_file:
            wav_file.setnchannels(self.channels)
            wav_file.setsampwidth(2)
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(audio.tobytes())

        return filename

    async def transcribe(self, filename: str) -> str:

        with open(filename, "rb") as audio_file:

            transcription = (
                await self.client.audio.transcriptions.create(
                    file=audio_file,
                    model="whisper-large-v3-turbo",
                    response_format="json",
                    language="en",
                    temperature=0.0,
                )
            )

        return transcription.text.strip()
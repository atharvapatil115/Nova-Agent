import os
from pathlib import Path

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
import soundfile as sf
import sounddevice as sd

load_dotenv()


class VoiceOutput:

    def __init__(self):
        self.client = ElevenLabs(
            api_key=os.getenv("ELEVENLABS_API_KEY")
        )

        self.model = "eleven_v4_turbo"

        # Keep your currently selected voice ID
        self.voice_id = "pFZP5JQG7iQjIQuC4Bku"

        self.output_dir = Path("audio")
        self.output_dir.mkdir(exist_ok=True)

    def generate(self, text: str, filename: str):
        output_path = self.output_dir / filename

        audio = self.client.text_to_speech.convert(
            text=text,
            voice_id=self.voice_id,
            model_id=self.model,
            output_format="mp3_44100_128",
        )

        with open(output_path, "wb") as f:
            for chunk in audio:
                f.write(chunk)

        return output_path

    def play(self, audio_path):
        print(f"🔊 Playing: {audio_path}")

        data, sample_rate = sf.read(
            audio_path,
            dtype="float32"
        )

        sd.play(data, sample_rate)
        sd.wait()

    def speak(self, text: str):
        if not text:
            return

        print("🔊 Nova is speaking...")

        audio_path = self.generate(
            text,
            "nova_response.mp3"
        )

        self.play(audio_path)
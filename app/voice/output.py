import os
from pathlib import Path

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from kokoro_onnx import Kokoro
import soundfile as sf
import sounddevice as sd

load_dotenv()


class VoiceOutput:

    def __init__(self):

        # =========================
        # ElevenLabs - Primary
        # =========================

        self.primary_client = ElevenLabs(
            api_key=os.getenv("ELEVENLABS_API_KEY")
        )

        self.primary_model = "eleven_v4_turbo"

        # Your current ElevenLabs voice
        self.voice_id = "pFZP5JQG7iQjIQuC4Bku"


        # =========================
        # ElevenLabs - Fallback
        # =========================

        self.fallback_client = ElevenLabs(
            api_key=os.getenv("ELEVENLABS_FALLBACK_API")
        )

        # Put your fallback ElevenLabs model ID here
        self.fallback_model = "pFZP5JQG7iQjIQuC4Bku"


        # =========================
        # Kokoro - Local Fallback
        # =========================

        self.kokoro = Kokoro(
            "models/kokoro/kokoro-v1.0.onnx",
            "models/kokoro/voices-v1.0.bin",
        )

        self.kokoro_voice = "af_heart"
        self.kokoro_speed = 1.0


        # =========================
        # Audio
        # =========================

        self.output_dir = Path("audio")
        self.output_dir.mkdir(exist_ok=True)


    def generate_elevenlabs(
        self,
        client,
        model,
        text: str,
        filename: str,
    ):

        output_path = self.output_dir / filename

        audio = client.text_to_speech.convert(
            text=text,
            voice_id=self.voice_id,
            model_id=model,
            output_format="mp3_44100_128",
        )

        with open(output_path, "wb") as f:
            for chunk in audio:
                f.write(chunk)

        return output_path


    def play_file(self, audio_path):

        print(f"🔊 Playing: {audio_path}")

        data, sample_rate = sf.read(
            audio_path,
            dtype="float32"
        )

        sd.play(data, sample_rate)
        sd.wait()


    def speak_kokoro(self, text: str):

        print("🧠 Using local Kokoro...")
        print(f"🎙️ Kokoro voice: {self.kokoro_voice}")

        samples, sample_rate = self.kokoro.create(
            text,
            voice=self.kokoro_voice,
            speed=self.kokoro_speed,
            lang="en-us",
        )

        sd.play(samples, sample_rate)
        sd.wait()


    def speak(self, text: str):

        if not text:
            return

        print("🔊 Nova is speaking...")


        # =====================================
        # 1. Try Primary ElevenLabs
        # =====================================

        try:

            print("☁️ Trying ElevenLabs primary...")

            audio_path = self.generate_elevenlabs(
                self.primary_client,
                self.primary_model,
                text,
                "nova_response.mp3",
            )

            self.play_file(audio_path)

            print("✅ Primary ElevenLabs succeeded")

            return

        except Exception as e:

            print(f"⚠️ Primary ElevenLabs failed: {e}")


        # =====================================
        # 2. Try Fallback ElevenLabs
        # =====================================

        try:

            print("🔄 Trying ElevenLabs fallback...")

            audio_path = self.generate_elevenlabs(
                self.fallback_client,
                self.fallback_model,
                text,
                "nova_response_fallback.mp3",
            )

            self.play_file(audio_path)

            print("✅ Fallback ElevenLabs succeeded")

            return

        except Exception as e:

            print(f"⚠️ Fallback ElevenLabs failed: {e}")


        # =====================================
        # 3. Final Local Fallback — Kokoro
        # =====================================

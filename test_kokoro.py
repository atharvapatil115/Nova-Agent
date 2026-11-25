import sounddevice as sd
from kokoro_onnx import Kokoro


MODEL_PATH = "models/kokoro/kokoro-v1.0.onnx"
VOICES_PATH = "models/kokoro/voices-v1.0.bin"

print("🧠 Loading Kokoro...")

kokoro = Kokoro(
    MODEL_PATH,
    VOICES_PATH,
)

print("✅ Kokoro loaded")

text = (
    "Hello Sir, Systems in check , properly working, nothing is pending from last night ... just one question........ did you forget your breakfast?"
)

print("🔊 Generating speech...")

samples, sample_rate = kokoro.create(
    text,
    voice="af_heart",
    speed=1.0,
    lang="en-us",
)

print(f"✅ Generated audio")
print(f"Sample rate: {sample_rate}")
print(f"Samples: {len(samples)}")

print("🔊 Playing...")

sd.play(samples, sample_rate)
sd.wait()

print("✅ Playback finished")
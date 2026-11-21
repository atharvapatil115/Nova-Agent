from app.voice.output import VoiceOutput

voice = VoiceOutput()

audio_path = voice.generate(
    "Good morning, Boss. I'm Nova. How can I help you?",
    "eleven_test.mp3"
)

print()
print("Generated:")
print(audio_path)

voice.play(audio_path)
from app.voice.output import VoiceOutput


def main():

    print("1. Creating VoiceOutput...")

    voice = VoiceOutput()

    print("2. Generating audio...")

    audio_path = voice.generate(
        "Hello Boss. Nova is online and ready.",
        "debug.wav"
    )

    print("3. Audio generated:")
    print(audio_path)

    print("4. Playing audio...")

    voice.play(audio_path)

    print("5. Playback finished.")


if __name__ == "__main__":
    main()
import time

import numpy as np
import sounddevice as sd
from openwakeword.model import Model


class WakeWordListener:

    def __init__(
        self,
        wake_word="hey_jarvis",
        threshold=0.5,
    ):
        self.wake_word = wake_word
        self.threshold = threshold
        self.model = Model(
            wakeword_models=[wake_word]
        )

    def wait_for_wake(self):

        print()
        print("=" * 60)
        print("NOVA IS LISTENING")
        print("=" * 60)
        print('Say: "Hey Jarvis"')
        print("Press Ctrl+C to stop.")
        print("=" * 60)

        wake_detected = False

        def audio_callback(indata, frames, time_info, status):
            nonlocal wake_detected

            if status:
                # Ignore normal overflow/underflow status messages.
                pass

            if wake_detected:
                return

            audio = np.squeeze(indata.copy())

            predictions = self.model.predict(audio)

            score = predictions.get(
                self.wake_word,
                0.0
            )

            if score >= self.threshold:
                wake_detected = True

                print()
                print("⚡ WAKE WORD DETECTED!")
                print(f"Score: {score:.3f}")

        with sd.InputStream(
            samplerate=16000,
            channels=1,
            dtype="int16",
            blocksize=1280,
            callback=audio_callback,
        ):
            while not wake_detected:
                time.sleep(0.05)

        self.model.reset()

        return True
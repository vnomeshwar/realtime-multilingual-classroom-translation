import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write


SAMPLE_RATE = 16000
BLOCK_SIZE = 1024

THRESHOLD = 0.02
SILENCE_LIMIT = 1.5
MIN_SPEECH_TIME = 0.3


def record_speech(output_file="speech_auto.wav"):

    audio_data = []

    recording = False
    silence_time = 0
    speech_time = 0
    stop_recording = False

    print("Waiting for you to speak...")

    def audio_callback(indata, frames, time, status):

        nonlocal recording
        nonlocal silence_time
        nonlocal speech_time
        nonlocal stop_recording

        if status:
            print(status)

        volume = np.sqrt(np.mean(indata ** 2))

        if volume > THRESHOLD:

            speech_time += BLOCK_SIZE / SAMPLE_RATE

            if not recording:

                if speech_time >= MIN_SPEECH_TIME:

                    print("Speech detected! Recording...")
                    recording = True

            if recording:

                audio_data.append(indata.copy())
                silence_time = 0

        else:

            speech_time = 0

            if recording:

                audio_data.append(indata.copy())

                silence_time += BLOCK_SIZE / SAMPLE_RATE

                if silence_time >= SILENCE_LIMIT:

                    stop_recording = True

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        blocksize=BLOCK_SIZE,
        dtype="float32",
        callback=audio_callback
    ):

        while not stop_recording:
            sd.sleep(100)

    if audio_data:

        audio = np.concatenate(audio_data)

        write(
            output_file,
            SAMPLE_RATE,
            audio
        )

        print("Recording stopped.")

        return output_file

    print("No speech detected.")

    return None
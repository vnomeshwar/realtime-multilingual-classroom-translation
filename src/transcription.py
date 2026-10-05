import whisper


def load_whisper_model():

    print("Loading Whisper model...")

    model = whisper.load_model("base")

    print("Whisper model loaded!")

    return model


def transcribe_audio(model, audio_file):

    result = model.transcribe(
        audio_file,
        temperature=0,
        condition_on_previous_text=False
    )

    text = result["text"].strip()
    language = result["language"]

    return text, language
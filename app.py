import streamlit as st
import sys

from src.recorder import record_speech
from src.transcription import (
    load_whisper_model,
    transcribe_audio
)
from src.translator import (
    load_translation_model,
    translate_text
)
from src.language_config import (
    LANGUAGES,
    LANGUAGE_MAPPING
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Classroom Translator",
    page_icon="🌍",
    layout="centered"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #9ca3af;
        margin-bottom: 35px;
    }

    .section-title {
        font-size: 24px;
        font-weight: 600;
        margin-top: 25px;
        margin-bottom: 10px;
    }

    .result-box {
        padding: 20px;
        border-radius: 12px;
        background-color: #262730;
        border: 1px solid #3d3d48;
        margin-top: 10px;
        margin-bottom: 20px;
        font-size: 18px;
    }

    .history-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #262730;
        border: 1px solid #3d3d48;
        margin-bottom: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SESSION STATE
# =========================================================

if "history" not in st.session_state:

    st.session_state.history = []


# =========================================================
# LOAD MODELS
# =========================================================

@st.cache_resource
def get_whisper_model():

    return load_whisper_model()


@st.cache_resource
def get_translation_model():

    return load_translation_model()


whisper_model = get_whisper_model()

tokenizer, translation_model = get_translation_model()


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🌍 Classroom Translator</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
    Real-time multilingual speech translation for classrooms
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# TARGET LANGUAGE
# =========================================================

st.markdown(
    '<div class="section-title">🌐 Target Language</div>',
    unsafe_allow_html=True
)

selected_language = st.selectbox(
    "Choose the language students should receive:",
    list(LANGUAGES.keys())
)

target_language = LANGUAGES[selected_language]


# =========================================================
# SPEECH INPUT
# =========================================================

st.markdown(
    '<div class="section-title">🎤 Speech Input</div>',
    unsafe_allow_html=True
)

st.write(
    "Click the button and speak. Recording automatically "
    "stops after you stop speaking."
)


start_button = st.button(
    "🎤 Start Listening",
    use_container_width=True
)


# =========================================================
# MAIN PIPELINE
# =========================================================

if start_button:

    st.info(
        "🎤 Listening... Please speak clearly."
    )

    # -----------------------------------------------------
    # STEP 1: RECORD
    # -----------------------------------------------------

    audio_file = record_speech(
        "speech_auto.wav"
    )

    if audio_file is None:

        st.warning(
            "⚠️ No speech detected. Please try again."
        )

        st.stop()

    st.success(
        "✅ Recording completed!"
    )

    st.audio(audio_file)


    # -----------------------------------------------------
    # STEP 2: TRANSCRIBE
    # -----------------------------------------------------

    with st.spinner(
        "🧠 Understanding your speech..."
    ):

        text, source_language = transcribe_audio(
            whisper_model,
            audio_file
        )


    if not text:

        st.warning(
            "⚠️ I couldn't understand the speech. "
            "Please try again."
        )

        st.stop()


    # -----------------------------------------------------
    # STEP 3: FIND SOURCE LANGUAGE
    # -----------------------------------------------------

    source_nllb_language = LANGUAGE_MAPPING.get(
        source_language
    )


    if source_nllb_language is None:

        st.error(
            f"Sorry, {source_language} is not supported yet."
        )

        st.stop()


    # -----------------------------------------------------
    # STEP 4: SHOW ORIGINAL SPEECH
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">📝 Original Speech</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="result-box">
        {text}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write(
        f"🔍 Detected language: **{source_language}**"
    )


    # -----------------------------------------------------
    # STEP 5: TRANSLATE
    # -----------------------------------------------------

    with st.spinner(
        f"🌍 Translating to {selected_language}..."
    ):

        translation = translate_text(
            tokenizer,
            translation_model,
            text,
            source_nllb_language,
            target_language
        )


    # -----------------------------------------------------
    # STEP 6: SHOW TRANSLATION
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">🌍 Translation</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="result-box">
        {translation}
        </div>
        """,
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # STEP 7: SAVE HISTORY
    # -----------------------------------------------------

    st.session_state.history.append(
        {
            "source": text,
            "translation": translation,
            "source_language": source_language,
            "target_language": selected_language
        }
    )


# =========================================================
# TRANSLATION HISTORY
# =========================================================

if st.session_state.history:

    st.markdown(
        '<div class="section-title">📚 Translation History</div>',
        unsafe_allow_html=True
    )

    for index, item in enumerate(
        reversed(st.session_state.history),
        start=1
    ):

        st.markdown(
            f"""
            <div class="history-box">

            <b>Translation {index}</b>

            <br><br>

            📝 <b>Original:</b><br>
            {item["source"]}

            <br><br>

            🌍 <b>{item["target_language"]}:</b><br>
            {item["translation"]}

            <br><br>

            🔍 Language detected:
            {item["source_language"]}

            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# CLEAR HISTORY
# =========================================================

if st.session_state.history:

    if st.button(
        "🗑️ Clear Translation History"
    ):

        st.session_state.history = []

        st.rerun()
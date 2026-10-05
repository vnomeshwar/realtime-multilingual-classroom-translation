# Real-Time Multilingual Classroom Translation System

## 1. Project Overview

The Real-Time Multilingual Classroom Translation System is a speech-based translation application designed to help teachers communicate with students who speak different languages.

The application captures speech through a microphone, automatically detects when the speaker starts and stops speaking, converts the speech into text using OpenAI Whisper, detects the source language, and translates the resulting text into a selected target language using Meta's NLLB-200 model.

The application is implemented using Python and Streamlit and provides an interactive interface for recording speech, viewing the transcription, viewing the translated output, and maintaining translation history during the current session.

## 2. Problem Statement

In multilingual classrooms, language differences can make communication between teachers and students difficult.

Traditional translation workflows require users to manually record speech, convert it into text, and translate the text using separate tools.

This project combines these steps into a single application:

```text
Speech
   |
   v
Automatic Speech Detection
   |
   v
Audio Recording
   |
   v
Speech-to-Text
   |
   v
Language Detection
   |
   v
Machine Translation
   |
   v
Translated Text
```

The goal is to provide a simple and automated workflow for classroom speech translation.

## 3. Key Features

- Automatic speech detection using microphone audio levels
- Automatic recording start when speech is detected
- Automatic recording stop after a configurable silence period
- Speech-to-text conversion using OpenAI Whisper
- Automatic source-language detection
- Multilingual translation using Meta NLLB-200
- Support for Hindi, Kannada, Tamil, and Telugu as target languages
- Streamlit-based interactive web interface
- Translation history within the current application session
- Cached ML models to avoid repeated model initialization
- Modular Python project structure

## 4. System Architecture

```text
                         User
                           |
                           v
                  Streamlit Web UI
                           |
                           v
                  Speech Recorder
                           |
                           v
                    Audio File
                           |
                           v
                    OpenAI Whisper
                     /          \
                    /            \
                   v              v
             Transcribed       Detected
                Text            Language
                   \              /
                    \            /
                     v          v
                   Language Mapping
                           |
                           v
                     NLLB-200
                           |
                           v
                  Target Language
                           |
                           v
                  Translated Text
                           |
                           v
                    Streamlit UI
                           |
                           v
                 Translation History
```

## 5. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application and ML pipeline development |
| Streamlit | Web-based user interface |
| OpenAI Whisper | Speech recognition and language detection |
| NLLB-200 | Multilingual machine translation |
| Hugging Face Transformers | Loading and running the NLLB model |
| PyTorch | Deep learning model execution |
| SoundDevice | Microphone audio capture |
| NumPy | Numerical and audio signal processing |
| SciPy | Saving recorded audio as WAV files |
| FFmpeg | Audio processing required by Whisper |

## 6. Project Structure

```text
realtime-multilingual-classroom-translation/
|
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
|
├── src/
│   ├── __init__.py
│   ├── recorder.py
│   ├── transcription.py
│   ├── translator.py
│   └── language_config.py
|
├── tests/
|
├── assets/
|
└── old_experiments/
```

### `app.py`

The main Streamlit application.

It is responsible for:

- Rendering the user interface
- Allowing the user to select a target language
- Starting the speech-recording process
- Calling the transcription module
- Calling the translation module
- Displaying the original speech
- Displaying the detected language
- Displaying the translated text
- Maintaining translation history

### `src/recorder.py`

Responsible for microphone input and automatic speech detection.

The recorder continuously monitors the microphone and calculates the audio signal volume.

When the volume crosses the configured speech threshold, recording begins.

When the speaker stops talking and the audio remains below the threshold for the configured silence duration, recording stops automatically.

Important configuration parameters include:

```python
SAMPLE_RATE = 16000
BLOCK_SIZE = 1024
THRESHOLD = 0.02
SILENCE_LIMIT = 1.5
MIN_SPEECH_TIME = 0.3
```

### `src/transcription.py`

Responsible for speech recognition.

The module:

1. Loads the Whisper model.
2. Accepts a recorded WAV file.
3. Converts speech into text.
4. Returns the detected source language.

The application currently uses the Whisper `base` model.

### `src/translator.py`

Responsible for machine translation.

The module loads:

```text
facebook/nllb-200-distilled-600M
```

It accepts:

- Source text
- Source language
- Target language

and returns the translated text.

### `src/language_config.py`

Contains the supported target languages and the mapping between Whisper language codes and NLLB language codes.

Example:

```text
Whisper code     NLLB code
--------------------------------
en               eng_Latn
hi               hin_Deva
kn               kan_Knda
ta               tam_Taml
te               tel_Telu
```

## 7. Supported Languages

The current version supports the following target languages:

| Language | NLLB Language Code |
|---|---|
| Hindi | `hin_Deva` |
| Kannada | `kan_Knda` |
| Tamil | `tam_Taml` |
| Telugu | `tel_Telu` |

The language configuration is separated into its own module so that additional languages can be added without modifying the main application logic.

## 8. Application Workflow

### Step 1: Select Target Language

The user selects the language in which the translated output should be displayed.

### Step 2: Start Listening

The user selects the Start Listening button.

The application starts monitoring microphone input.

### Step 3: Detect Speech

The recorder calculates the audio volume for each incoming audio block.

If the volume exceeds the configured threshold for the minimum speech duration, the application considers this to be speech.

### Step 4: Record Speech

The audio is continuously collected while the user is speaking.

### Step 5: Detect End of Speech

When the audio volume remains below the threshold for the configured silence duration, recording stops automatically.

The recorded audio is saved as a WAV file.

### Step 6: Transcribe Speech

The WAV file is passed to Whisper.

Whisper returns:

```text
Transcribed text
Detected language
```

For example:

```text
Input speech:
"Good morning students"

Detected language:
English

Transcription:
"Good morning students"
```

### Step 7: Map Language Codes

Whisper and NLLB use different language-code formats.

The application maps the Whisper language code to the corresponding NLLB language code.

For example:

```text
Whisper:
en

NLLB:
eng_Latn
```

### Step 8: Translate

The transcription is passed to NLLB along with the source and target language codes.

For example:

```text
Source:
English

Target:
Kannada

Input:
Good morning students

Output:
ಶುಭೋದಯ ವಿದ್ಯಾರ್ಥಿಗಳೇ
```

### Step 9: Display Results

The Streamlit interface displays:

- Original speech
- Detected source language
- Translated text
- Translation history

## 9. Performance Optimization

One of the important optimization considerations in this project is ML model initialization.

Whisper and NLLB are large machine learning models. Loading these models repeatedly for every user interaction would introduce significant unnecessary overhead.

The application therefore uses Streamlit's resource caching:

```python
@st.cache_resource
```

The models are loaded once and reused for subsequent interactions.

Conceptually:

```text
Without caching:

Request
   |
   v
Load Whisper
   |
   v
Process audio
   |
   v
Request again
   |
   v
Load Whisper again


With caching:

First request
   |
   v
Load Whisper
   |
   v
Keep model in memory
   |
   v
Subsequent requests
   |
   v
Reuse existing model
```

This reduces repeated model-loading overhead and improves application responsiveness.

## 10. Installation

### Prerequisites

The following software is required:

- Python 3.x
- FFmpeg
- Git
- A working microphone

### Clone the Repository

```bash
git clone <your-github-repository-url>
cd realtime-multilingual-classroom-translation
```

The GitHub repository URL will be added after the repository is created.

### Create a Virtual Environment

Windows:

```powershell
python -m venv venv
```

Activate the environment:

```powershell
venv\Scripts\Activate.ps1
```

### Install Dependencies

```powershell
pip install -r requirements.txt
```

### Verify FFmpeg

Run:

```powershell
ffmpeg -version
```

FFmpeg must be available from the system PATH.

## 11. Running the Application

After installing the dependencies, run:

```powershell
streamlit run app.py
```

Streamlit will start a local web server.

The application can then be accessed through the local URL displayed in the terminal, typically:

```text
http://localhost:8501
```

## 12. Translation History

The application maintains translation history using Streamlit session state.

Each translation stores:

```text
Original text
Translated text
Detected source language
Selected target language
```

The history exists for the current application session.

A Clear Translation History option is also available in the interface.

## 13. Error Handling

The application includes basic validation for common conditions such as:

- No speech detected
- Empty transcription
- Unsupported source language
- Missing translation mapping

For example, if Whisper detects a language that has not been configured for NLLB translation, the application displays an appropriate error instead of attempting the translation.

## 14. Design Decisions

### Why Whisper?

Whisper provides speech recognition and automatic language identification in a single model.

It supports multiple languages and is suitable for converting classroom speech into text before translation.

### Why NLLB-200?

NLLB-200 is designed for multilingual machine translation and supports a large number of languages.

It is particularly useful for this project because the application is intended to support multiple Indian languages.

### Why Streamlit?

Streamlit provides a simple way to build an interactive Python-based interface without requiring a separate frontend framework.

This allows the ML pipeline and user interface to be developed within the same Python project.

### Why Modularize the Application?

The application separates recording, transcription, translation, and language configuration into different modules.

This improves:

- Maintainability
- Readability
- Testing
- Reusability
- Debugging
- Future development

## 15. Current Limitations

The current implementation is a working prototype and has several limitations:

- Translation is processed after recording rather than continuously during speech.
- Audio is currently stored as a temporary WAV file.
- The application is designed primarily for local execution.
- The current voice activity detection approach is based on audio volume thresholds.
- GPU acceleration has not yet been configured.
- Translation history is stored only for the current Streamlit session.
- The current application does not provide translated speech output.

## 16. Future Improvements

Potential improvements include:

1. Implement true streaming speech recognition and translation.
2. Replace basic volume-based detection with a dedicated Voice Activity Detection model.
3. Add more Indian and international languages.
4. Add text-to-speech output for translated text.
5. Add persistent translation history using a database.
6. Add GPU support for faster model inference.
7. Add model quantization or optimized inference for CPU environments.
8. Add automated unit and integration tests.
9. Containerize the application using Docker.
10. Deploy the application to a cloud environment.
11. Add authentication and multi-user classroom support.
12. Add monitoring and performance metrics.

## 17. Project Status

Current status: Working Prototype

The current implementation successfully demonstrates the complete pipeline:

```text
Microphone Input
       |
       v
Automatic Speech Detection
       |
       v
Audio Recording
       |
       v
Whisper Speech Recognition
       |
       v
Language Detection
       |
       v
NLLB-200 Translation
       |
       v
Streamlit Interface
       |
       v
Translation History
```

The project is structured so that individual components can be independently improved and tested as development continues.

## 18. Author

Nomeshwar V
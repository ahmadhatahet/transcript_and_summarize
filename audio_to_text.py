import speech_recognition as sr
from pathlib import Path
import arabic_reshaper
from log_config import init_logger
import logging

# initaite logger
init_logger()
logger = logging.getLogger('audio-to-text')


# get base folder
base = Path(__file__).parent
path_audio_files = base / 'audio_files' / '2023-04-22_11-37'

# Initialize the recognizer
r = sr.Recognizer()

# read audio file
for audio_file in path_audio_files.iterdir():

    # Load the audio file
    with sr.AudioFile(audio_file.__str__() ) as source:
        audio = r.record(source)

    # Convert audio to text
    text = r.recognize_google(audio, language="ar")
    text = arabic_reshaper.reshape(text)
    # Print the recognized text
    print(text[::-1])
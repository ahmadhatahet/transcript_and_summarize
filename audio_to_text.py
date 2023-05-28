import speech_recognition as sr
from speech_recognition import exceptions as sr_exception
from pathlib import Path
import arabic_reshaper
from log_config import init_logger
import logging


# initaite logger
init_logger()
logger = logging.getLogger('audio-to-text')

languages = {
    'English': 'en',
    'German': 'de',
    'Arabic': 'ar',
}

def start_transcript(file_name, language):
    # get base folder
    base = Path(__file__).parent
    path_audio_files = base / 'audio_files' / file_name

    # folder to save text files
    path_text_files = base / 'text_files' / file_name
    path_text_files.mkdir(exist_ok=True, parents=True)

    # Initialize the recognizer
    r = sr.Recognizer()

    # read audio file
    for audio_file in path_audio_files.iterdir():

        # Load the audio file
        with sr.AudioFile(audio_file.__str__() ) as source:
            audio = r.record(source)

        try:
            # Convert audio to text
            text = r.recognize_google(audio, language=languages[language])
        except sr_exception.UnknownValueError:
            text = '' # if empty or currupted audio file

        if language == 'Arabic':
            text = arabic_reshaper.reshape(text)

        # create text file
        file = path_text_files / f'{audio_file.name}.txt'
        file.touch()

        # save text
        file.write_text(text, 'utf-8')

    return path_text_files
import streamlit as st
import time
from log_config import init_logger
import logging
from capture_audio import start_recording
from audio_to_text import start_transcript

# initaite logger
init_logger()
logger = logging.getLogger('audio-to-text')

def record_audio():
    print('Recording ... !')
    return start_recording(
        recording_duration=10,
        interval_duration=0,
        total_duration=0.5
    )

def convert_to_text(file_name):
    print('Converting to text ... !')

    if file_name is None: raise ValueError('No file name was passed!')

    return start_transcript(file_name)

# Streamlit app code
def main():
    st.title("Audio Recording and Conversion")

    # Record audio
    st.header("Record Audio")
    file_name = None
    if st.button("Start Recording"):
        file_name = record_audio()
        st.success("Recording finished!")

    # Convert audio to text
    st.header("Convert to Text")
    if st.button("Convert"):

        try:

            text_files_path = convert_to_text(file_name)
            st.success("Text: {}".format(str(text_files_path)))

        except ValueError:

            st.error('No file name was passed!')

if __name__ == "__main__":
    main()

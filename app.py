import streamlit as st
import time
from log_config import init_logger
import logging
from capture_audio import start_recording
from audio_to_text import start_transcript
from summarize_bot import summarize

# initaite logger
init_logger()
logger = logging.getLogger('audio-to-text')

keys = ['file_name', 'text_files_path']
for k in keys:
    if k not in st.session_state:
        st.session_state[k] = None

def record_audio():
    print('Recording ... !')
    return start_recording(
        recording_duration=10,
        interval_duration=0,
        total_duration=1
    )

def convert_to_text(file_name):
    print('Converting to text ... !')

    if file_name is None: raise ValueError('No file name was passed!')

    return start_transcript(file_name)

# Streamlit app code
def main():
    st.title("Audio Recording and Conversion")

    # # Record audio
    # st.header("Record Audio")
    # if st.button("Start Recording"):

    #     try:

    #         st.session_state['file_name'] = record_audio()
    #         st.success("Recording finished!")

    #     except:
    #         st.warning('Recording was interrupted!')

    # st.info(file_name)

    # Convert audio to text
    st.header("Convert to Text")
    if st.button("Convert"):

        try:

            st.session_state['text_files_path'] = convert_to_text('2023-05-17_20-00')
            st.success("Text: {}".format(str(st.session_state['text_files_path'])))

        except ValueError:

            st.error('No file name was passed!')


    st.header("Summarize Text:")
    if st.button("Summarize"):
        st.write(summarize(st.session_state['text_files_path']))

if __name__ == "__main__":
    main()

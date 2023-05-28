import streamlit as st
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

def record_audio(recording_duration=10,total_duration=1):
    logger.info('Recording ... !')
    return start_recording(
        recording_duration=10,
        total_duration=1
    )

def convert_to_text(file_name, language):
    logger.info('Converting to text ... !')
    logger.debug(f'Langauge: {language} ... !')

    if file_name is None: raise ValueError('No file name was passed!')

    return start_transcript(file_name, language)

# Streamlit app code
def main():
    st.title("Audio Recording and Conversion")


    # Input boxes for record and total duration
    col1, col2, col3 = st.columns(3)
    with col1:
        lang = st.selectbox("Language", ['English', 'German', 'Arabic'])

    with col2:
        recording_duration = st.number_input("Per Record Duration (seconds)", value=10, min_value=10)

    with col3:
        total_duration = st.number_input("Total Duration (minutes)", value=1, min_value=1)

    # Record audio
    st.header("Record Audio")
    if st.button("Start Recording"):
        with st.spinner(text="Recording..."):
            try:

                st.session_state['file_name'] = record_audio(recording_duration=recording_duration,total_duration=total_duration)
                st.success("Recording finished!")

            except:
                st.warning('Recording was interrupted!')


    # Convert audio to text
    st.header("Convert to Text")
    if st.button("Transcript"):
        with st.spinner(text="Transcripting..."):
            try:

                st.session_state['text_files_path'] = convert_to_text(st.session_state['file_name'], lang)
                st.success("Text: {}".format(str(st.session_state['text_files_path'])))

            except ValueError:

                st.error('No file name was passed!')


    st.header("Summarize Text:")
    if st.button("Summarize"):
        with st.spinner(text="Summarizing..."):
            success, reponse = summarize(st.session_state['text_files_path'], lang)

            if success:
                st.balloons()
                st.success(reponse)
            else:
                st.error('Server load is too high!')


if __name__ == "__main__":
    main()

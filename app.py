import streamlit as st
import time

def record_audio():
    print('Recording ... !')
    time.sleep(20)

def convert_to_text(audio_file):
    print('Converting to text ... !')

# Streamlit app code
def main():
    st.title("Audio Recording and Conversion")

    # Record audio
    st.header("Record Audio")
    if st.button("Start Recording"):
        record_audio()
        st.success("Recording finished!")

    # Convert audio to text
    st.header("Convert to Text")
    audio_file = st.file_uploader("Upload an audio file")
    if audio_file is not None:
        if st.button("Convert"):
            text = convert_to_text(audio_file)
            st.success("Text: {}".format(text))

if __name__ == "__main__":
    main()

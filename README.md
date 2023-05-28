# Transcript and Summarize:
Recording long conversation, trancipting, then summarize, has became much simpler and affordable with new LLMs.

This is a small project to utilize OpenAI and  Speech recognizer ([supports various models](https://pypi.org/project/SpeechRecognition/)) APIs.

Using the user primary microphone and a streamlit web UI, the user could choose one of three languages [English, German, Arabic], total duration of the recording time in minutes, and how many seconds to save as a file as the time goes.

### Todos:
1. ✔ Multi language support (EN, DE, AR).
2. ✔ Add options to the UI for faster modifications.


### Notes:
Arabic language is one of the Semitic language , thus, it is not well recognized by the models used yet.
Transcripting works fairly well, but summarizing is less than average. Maybe a better prompt could help increase the quality of the summarized text.


### Screenshot:
![Screenshot of the streamlit UI](https://github.com/ahmadhatahet/transcript_and_summarize/blob/master/home_screen.png?raw=true)
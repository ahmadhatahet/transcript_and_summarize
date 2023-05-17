import pyaudio
import wave
import datetime
import time
from pathlib import Path
from log_config import init_logger
import logging

# initaite logger
init_logger()
logger = logging.getLogger('audio-to-text')


def start_recording(*, recording_duration=10, interval_duration=0, total_duration=2):
    # save audio to folder
    now = datetime.datetime.now()
    file_name = now.strftime("%Y-%m-%d_%H-%M")

    base = Path(__file__).parent
    path_audio_files = base / 'audio_files' / file_name

    path_audio_files.mkdir(exist_ok=True, parents=True)


    # Set the duration of each recording in seconds
    # recording_duration = 10

    # Set the duration of the interval between recordings in seconds
    # interval_duration = 0

    # Set the format and number of channels for the audio recording
    audio_format = pyaudio.paInt16
    channels = 2
    sample_rate = 44100
    chunk_size = 1024

    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Open a new stream for recording
    stream = audio.open(format=audio_format, channels=channels, rate=sample_rate, input=True, frames_per_buffer=chunk_size)

    # Starting Podcast time
    start_podacst = datetime.datetime.now()

    # End Podcast time
    end_podcast = start_podacst + datetime.timedelta(minutes=total_duration)


    # Record and save audio every interval_duration seconds
    while True:
        # Get the current time for the filename
        now = datetime.datetime.now()
        file_name = path_audio_files / now.strftime("%Y-%m-%d_%H-%M-%S.wav")

        file_name.touch()

        with open(file_name, 'wb') as f:

            # Open a new wave file for writing
            wave_file = wave.open(f)
            wave_file.setnchannels(channels)
            wave_file.setsampwidth(audio.get_sample_size(audio_format))
            wave_file.setframerate(sample_rate)

            # Record audio for recording_duration seconds
            for i in range(0, int(sample_rate / chunk_size * recording_duration)):
                data = stream.read(chunk_size)
                wave_file.writeframes(data)

            # Close the wave file
            wave_file.close()

        # Terminate if end podcast time
        if datetime.datetime.now() >= end_podcast:
            break

        # Wait for the next interval_duration seconds
        time.sleep(interval_duration)

    # Stop and close the audio stream
    stream.stop_stream()
    stream.close()
    audio.terminate()


if __name__ == "__main__":

    start_recording()
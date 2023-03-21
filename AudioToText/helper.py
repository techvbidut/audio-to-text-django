import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks
from django.conf import settings
import os, glob


def handle_uploaded_file(f):
    destination = open(settings.MEDIA_ROOT + str(f), "wb+")
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()


def extract_txt_frm_audio(filename="", foldername=""):
    audio_file = AudioSegment.from_file(
        settings.MEDIA_ROOT + "/" + foldername + "/" + filename, format="wav"
    )

    # Split the audio file into mono tracks
    audio_file = audio_file.split_to_mono()[0]
    # Split the audio file into chunks of 10 seconds each
    chunk_duration = 10000  # milliseconds
    chunks = make_chunks(audio_file, chunk_duration)

    r = sr.Recognizer()

    long_txt = ""
    for i, chunk in enumerate(chunks):
        # Export audio chunk as WAV file
        chunk_name = f"{settings.MEDIA_ROOT}/{foldername}/chunk{i}.wav"
        chunk.export(chunk_name, format="wav")

        # Recognize speech in the audio chunk
        with sr.AudioFile(chunk_name) as source:
            audio_data = r.record(source)
        try:
            text = r.recognize_google(audio_data)
            print(f"Chunk {i}: {text}")
            with open(
                settings.MEDIA_ROOT + "/" + foldername + "/file.txt", "a"
            ) as file:
                # Append some text to the file
                file.write("\n Chunk" + str(text))
            long_txt += "\n Chunk " + str(i) + ": " + str(text)
        except sr.UnknownValueError:
            print(f"Speech recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Error: {0}".format(e))

    return long_txt


def clear_directory_with_startswith(directory_path="", startswith=""):
    for filename in glob.glob(directory_path + "/" + startswith + "*"):
        os.remove(filename)

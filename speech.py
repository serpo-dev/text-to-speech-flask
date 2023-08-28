import os
import random
import re
import string
from TTS.api import TTS
from pydub import AudioSegment

def generate_random_string(length):
    letters = string.ascii_letters
    return "".join(random.choice(letters) for _ in range(length))

def check_letters_and_digits(string):
    pattern = r"[a-zA-Z0-9]"
    match = re.search(pattern, string)
    return bool(match)


def combine_wav(file_names):
    output_filename = generate_random_string(20)
    combined = sum((AudioSegment.from_wav(f + ".wav") for f in file_names))
    combined.export(output_filename + ".wav", format="wav")
    return output_filename


def split_punctuation(text):
    text = text.replace("...", ".")
    text = text.replace("..", ".")
    pattern = r"(?<!\.)[.!?]"
    replaced = re.sub(pattern, ".", text)
    return replaced.split(".")

def delete_wav_files():
    for fn in os.listdir():
        if fn.endswith(".wav"):
            os.remove(fn)

async def get_speech_file_name(text):
    delete_wav_files()
    
    text = split_punctuation(text)
    file_names = []

    model_name = TTS.list_models()[9]
    tts = TTS(model_name)

    for t in text:
        if not check_letters_and_digits(t):
            continue
        if len(t) < 12:
            t = " - - - - - - - - - - - - " + t
        file_name = generate_random_string(20)

        tts.tts_to_file(text=t, file_path="%s.wav" % file_name)
        file_names.append(file_name)
        
    return combine_wav(file_names)
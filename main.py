from moviepy import VideoFileClip
from os import listdir
from os.path import isfile, join
import sys
import subprocess
import os
import whisper
import json

MODEL_NAME: str = "small"   # "tiny", "base", "small", "medium", or "large-v2"
DEVICE: str = "cpu"         # force CPU
TMP_AUDIO: str = "tmp_audio.wav"

model = whisper.load_model(MODEL_NAME, device=DEVICE)

results: dict[str, str] = {}

def transcribe_audio(audio_path: str):
    global model
    
    if not os.path.exists(audio_path):
        print("File not found:", audio_path)
        sys.exit(1)

    # Transcribe
    result = model.transcribe(audio_path)

    return result["text"].strip()

files: dict = { "personal": [f for f in listdir("./personal") if isfile(join("./personal", f))], "visual": [f for f in listdir("./visual") if isfile(join("./visual", f))] }

for group in files:
    for file in files[group]:
        clip = VideoFileClip(f"./{group}/{file}")
        clip.audio.write_audiofile(f"./audio-{group}/{file}.mp3")

        results[f"{group}/{file}"] = transcribe_audio(f"./audio-{group}/{file}.mp3")


with open('data.json', 'w') as f:
    json.dump(results, f)

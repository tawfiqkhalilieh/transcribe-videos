from moviepy import VideoFileClip
from os import listdir
from os.path import isfile, join
import sys
import os
import whisper
import json
import yt_dlp

MODEL_NAME: str = "small"   # "tiny", "base", "small", "medium", or "large-v2"
DEVICE: str = "cpu"         # force CPU
TMP_AUDIO: str = "tmp_audio.wav"

model = whisper.load_model(MODEL_NAME, device=DEVICE)

results: dict[str, str] = {}

files: dict = { "personal": [f for f in listdir("./personal") if isfile(join("./personal", f))], "visual": [f for f in listdir("./visual") if isfile(join("./visual", f))] }
youtube_urls: list[str] = [
    'https://www.youtube.com/embed/d7iSFl5cp84?si=8NIZsWwe1URvFuYe',
    'https://www.youtube.com/embed/JMLsHI8aV0g?si=l2lTxw6SQNt9Zl2_',
    'https://www.youtube.com/embed/n1iUT1QXDIc?si=BWfa_Iyjo2wBlxPA',
    'https://www.youtube.com/embed/LxigsXJCeLU?si=u3mjsLQs9Xsk7zds',
    'https://www.youtube.com/embed/QdDa2outstI?si=zp3t4jC7a8ZvQ34s',
    'https://www.youtube.com/embed/987VSNBw558?si=8clQWTkG89t9GkTg',
    'https://www.youtube.com/embed/yyVMZHjaY40?si=IxFJ2vPTHxKzLMr1',
    'https://www.youtube.com/embed/l_NYrWqUR40?si=YAju-r-Oa-yvctGX',
    'https://www.youtube.com/embed/c9F5kMUfFKk?si=NGMX2z-AcoqUPOd9',
    'https://www.youtube.com/embed/BCHhwxvQqxg?si=YKolbpPybZqJPMk_',
    'https://www.youtube.com/embed/Yomf5pBN8dY?si=3S9qsv-be6usSrLV'
]

def transcribe_audio(audio_path: str):
    global model
    
    if not os.path.exists(audio_path):
        print("File not found:", audio_path)
        sys.exit(1)

    # Transcribe
    result = model.transcribe(audio_path)

    return result["text"].strip()


def extract_text_from_files():
    global files
    for group in files:
        for file in files[group]:
            clip = VideoFileClip(f"./{group}/{file}")
            clip.audio.write_audiofile(f"./audio-{group}/{file}.mp3")

            results[f"{group}/{file}"] = transcribe_audio(f"./audio-{group}/{file}.mp3")


    with open('data.json', 'w') as f:
        json.dump(results, f)

def download_as_mp3(url, output_path=".", count=1):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_path}/{count}.%(ext)s',
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }
        ],
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        # The title from info_dict is the video title
        title = info_dict.get("title", "output")
        filename = os.path.join(output_path, f"{count}.mp3")
        return filename
    
def extract_text_from_youtube():
    for i, url in enumerate(youtube_urls):
        file: str = download_as_mp3(url, "./youtube-audio", count=i+1)

        results[file] = transcribe_audio(file)
        
    with open('youtube.json', 'w') as f:
        json.dump(results, f)

extract_text_from_youtube()




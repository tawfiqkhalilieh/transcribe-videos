# This is two basic challenge I faced today at work, That I'd love to share here

### Challenge 1: You have the two directories `personal/` `visual/` that contain .mp4 files, start with extracting the audio from the files in `.mp3` format, and then transcribe it and save it in `data.json`

I have data as follows:

```
personal/*.mp4
visual/*.mp4
```

```
personal/*.mp4 -> audio-personal/*.mp3 -> [insert to] data.json
visual/*.mp4 -> audio-visual/*.mp3 -> [insert to] data.json
```

### Challenge 2: You have a list of youtube videos `youtube_urls`, tart with extracting the audio from the files in `.mp3` format, and then transcribe it and save it in `data.json`

The approach for these two challenges is simple, I need to build two functions to extract audio from both `mp4` files and youtube videos,

1. Loop over the directories, loop over the files in each directory, and extract the audio using `moviepy`.

```py
files: dict = { "personal": [f for f in listdir("./personal") if isfile(join("./personal", f))], "visual": [f for f in listdir("./visual") if isfile(join("./visual", f))] }

def extract_text_from_files():
    global files
    for group in files:
        for file in files[group]:
            clip = VideoFileClip(f"./{group}/{file}")
            clip.audio.write_audiofile(f"./audio-{group}/{file}.mp3")
```

2. Download videos as audio files from youtube, using `yt_dlp`, a python library that uses ffmpeg and the youtube API

```py
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
```

3. Transcribe Audio from these files, I chose to ues wisper, but any speech recognition model.

- setup the model:

```py
MODEL_NAME: str = "small"   # "tiny", "base", "small", "medium", or "large-v2"
DEVICE: str = "cpu"         # force CPU
TMP_AUDIO: str = "tmp_audio.wav"

model = whisper.load_model(MODEL_NAME, device=DEVICE)
```

- write the transcribe_audio function

```py
def transcribe_audio(audio_path: str):
    global model

    if not os.path.exists(audio_path):
        print("File not found:", audio_path)
        sys.exit(1)

    # Transcribe
    result = model.transcribe(audio_path)

    return result["text"].strip()

```

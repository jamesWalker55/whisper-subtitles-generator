# Whisper - Subtitle generation

A small script that uses [Whisper](https://github.com/openai/whisper) to generate English subtitles for a given video/audio file.

## Install

I recommend using a virtual environment, like so:

```bash
python -m venv venv
./venv/Scripts/activate
```

Then install the dependencies.

```bash
pip install -r requirements.txt
```

## Usage

Pass the video(s) you want to process as arguments. You can override the default model used for text detection with `--model`.

```bash
# usage: tts-whisper.py [-h] [--output OUTPUT] [--model {tiny.en,tiny,base.en,base,small.en,small,medium.en,medium,large}]
#                       [--skip-confirmation]
#                       input [input ...]

./venv/Scripts/python.exe tts-whisper.py my-video1.mp4 my-video2.mp4
```

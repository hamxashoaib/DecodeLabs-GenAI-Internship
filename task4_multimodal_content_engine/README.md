# Task 4 – The Multimodal Content Engine 🎥

## Objective
Build an automated pipeline that takes a video/audio file, transcribes it, identifies the most "viral" segments, and generates social media captions + B-roll descriptions for each segment.

## What's Included

| File | Description |
|------|-------------|
| `pipeline.py` | Master script — runs the full pipeline end to end |
| `transcribe.py` | Whisper-based audio transcription with timestamps |
| `viral_extractor.py` | GPT-powered viral segment identifier |
| `caption_generator.py` | Social media caption + B-roll description generator |
| `sample_output.json` | Example of pipeline output for a 10-minute video |

## Pipeline Flow

```
[Input: Video or Audio File]
         ↓
[transcribe.py] — OpenAI Whisper
  → Full transcript with timestamps
         ↓
[viral_extractor.py] — GPT-4o
  → Identifies 5 most shareable/viral segments
         ↓
[caption_generator.py] — GPT-4o
  → Generates for each segment:
     • Instagram/TikTok caption
     • Twitter/X hook
     • Viral headline
     • B-roll description
         ↓
[Output: sample_output.json + console report]
```

## How to Run

```bash
# Install dependencies
pip install openai-whisper openai ffmpeg-python

# Run the full pipeline
python pipeline.py --input your_video.mp4

# Or transcribe only
python transcribe.py --input your_audio.mp3

# Output is saved to output/
```

## Requirements
- Python 3.10+
- ffmpeg installed on system (`sudo apt install ffmpeg` or `brew install ffmpeg`)
- OpenAI API key in `.env`

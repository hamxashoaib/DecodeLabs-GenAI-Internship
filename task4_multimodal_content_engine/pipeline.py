"""
pipeline.py – Master Multimodal Content Pipeline
Task 4: The Multimodal Content Engine
DecodeLabs Generative AI Internship | Batch 2026

Runs the full pipeline:
  [Video/Audio] → [Transcription] → [Viral Detection] → [Caption Generation] → [Output]

Usage:
  python pipeline.py --input your_video.mp4
  python pipeline.py --input your_audio.mp3 --model medium
  python pipeline.py --demo   (runs with built-in sample data, no API needed for transcription)
"""

import os
import json
import argparse
from pathlib import Path
from datetime import datetime

from transcribe import transcribe_audio, extract_audio_from_video, TranscriptSegment
from viral_extractor import extract_viral_segments, print_viral_segments
from caption_generator import generate_all_captions, print_content_assets


# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key-here")
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------------------------
# SAMPLE DATA FOR DEMO MODE (no audio file needed)
# ---------------------------------------------------------------------------
DEMO_TRANSCRIPT = [
    {"start": 0, "end": 12, "text": "Most people spend 8 hours a day working and still feel like they got nothing done. The problem isn't time — it's attention."},
    {"start": 12, "end": 28, "text": "Researchers at MIT found that the average knowledge worker is only truly focused for about 2.5 hours per day. The rest is shallow work, meetings, and distractions."},
    {"start": 28, "end": 45, "text": "Here is what shocked me: a single uninterrupted 90-minute deep work session produces the same output as 4 hours of fragmented work. I tested this myself for an entire month."},
    {"start": 45, "end": 62, "text": "The second insight is about decision fatigue. Every small decision you make — what to wear, what to eat, what email to answer first — drains the same mental battery as your big decisions."},
    {"start": 62, "end": 80, "text": "Top CEOs batch their decisions. They decide their week's meals, outfits, and small tasks all at once on Sunday. That way, Monday to Friday is reserved for thinking that actually moves the needle."},
    {"start": 80, "end": 98, "text": "The third thing — and this is the one nobody talks about — is strategic rest. Not sleep. Strategic rest means taking a 20-minute break at the 90-minute mark, every time, without guilt."},
    {"start": 98, "end": 118, "text": "Your brain runs in 90-minute ultradian cycles. Fighting those cycles is like trying to sprint a marathon. Working with them means you can sustain peak performance across your entire day."},
    {"start": 118, "end": 135, "text": "I went from producing 3 deliverables a week to 11, just by restructuring my schedule around these three principles. Not by working more hours — but by working smarter within the same hours."},
    {"start": 135, "end": 150, "text": "If you take one thing from this video, let it be this: protect your deep work time like it is the most important meeting of your life. Because it is. Follow for more."},
]


# ---------------------------------------------------------------------------
# MAIN PIPELINE
# ---------------------------------------------------------------------------
def run_pipeline(input_path: str = None, whisper_model: str = "base", demo: bool = False):
    """
    Full multimodal pipeline from audio/video to content assets.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"pipeline_output_{timestamp}.json"

    print("\n" + "🎬 " * 20)
    print("  MULTIMODAL CONTENT ENGINE — DecodeLabs Task 4")
    print("🎬 " * 20)

    # ── STEP 1: Transcription ──────────────────────────────────────────────
    print("\n[Step 1/3] 🎙️  TRANSCRIPTION")
    print("-" * 40)

    if demo:
        print("[Demo Mode] Using built-in sample transcript (no audio file needed).")
        transcript_segments = DEMO_TRANSCRIPT
    else:
        if not input_path:
            print("[ERROR] Provide --input path or use --demo flag.")
            return

        audio_path = input_path
        video_extensions = {".mp4", ".mov", ".avi", ".mkv", ".webm"}
        if Path(input_path).suffix.lower() in video_extensions:
            audio_path = OUTPUT_DIR / "temp_audio.mp3"
            extract_audio_from_video(input_path, str(audio_path))

        segments: list[TranscriptSegment] = transcribe_audio(str(audio_path), model_size=whisper_model)
        transcript_segments = [
            {"start": s.start, "end": s.end, "text": s.text}
            for s in segments
        ]

        # Save transcript
        transcript_path = OUTPUT_DIR / f"transcript_{timestamp}.json"
        with open(transcript_path, "w") as f:
            json.dump(transcript_segments, f, indent=2)
        print(f"[Step 1] Transcript saved → {transcript_path}")

    # ── STEP 2: Viral Segment Detection ───────────────────────────────────
    print("\n[Step 2/3] 🔥 VIRAL SEGMENT DETECTION")
    print("-" * 40)

    viral_segments = extract_viral_segments(transcript_segments, OPENAI_API_KEY)
    print_viral_segments(viral_segments)

    # ── STEP 3: Caption & B-Roll Generation ───────────────────────────────
    print("\n[Step 3/3] 📱 CONTENT ASSET GENERATION")
    print("-" * 40)

    content_assets = generate_all_captions(viral_segments, OPENAI_API_KEY)
    print_content_assets(content_assets)

    # ── FINAL OUTPUT ───────────────────────────────────────────────────────
    final_output = {
        "pipeline_run": timestamp,
        "source": "demo" if demo else input_path,
        "total_viral_segments": len(viral_segments),
        "viral_segments": viral_segments,
        "content_assets": content_assets
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=2, ensure_ascii=False)

    print(f"\n\n✅ Pipeline complete. Full output saved → {output_file}")
    return final_output


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multimodal Content Engine Pipeline")
    parser.add_argument("--input", help="Path to video or audio file")
    parser.add_argument("--model", default="base", choices=["tiny", "base", "small", "medium", "large"],
                        help="Whisper model size")
    parser.add_argument("--demo", action="store_true", help="Run with built-in sample data")
    args = parser.parse_args()

    run_pipeline(
        input_path=args.input,
        whisper_model=args.model,
        demo=args.demo
    )

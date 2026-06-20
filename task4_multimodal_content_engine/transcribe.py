"""
transcribe.py – Whisper Speech-to-Text Module
Task 4: The Multimodal Content Engine
DecodeLabs Generative AI Internship | Batch 2026

Transcribes a video or audio file using OpenAI Whisper
and returns the full transcript with word-level timestamps.
"""

import os
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, asdict


@dataclass
class TranscriptSegment:
    """Represents a timed segment of transcript text."""
    id: int
    start: float   # seconds
    end: float     # seconds
    text: str

    @property
    def duration(self) -> float:
        return round(self.end - self.start, 2)

    @property
    def start_formatted(self) -> str:
        m, s = divmod(int(self.start), 60)
        return f"{m:02d}:{s:02d}"

    @property
    def end_formatted(self) -> str:
        m, s = divmod(int(self.end), 60)
        return f"{m:02d}:{s:02d}"


def extract_audio_from_video(video_path: str, output_path: str = "temp_audio.mp3") -> str:
    """Extract audio track from a video file using ffmpeg."""
    try:
        import ffmpeg
        (
            ffmpeg
            .input(video_path)
            .output(output_path, acodec="mp3", ab="192k")
            .overwrite_output()
            .run(quiet=True)
        )
        print(f"[Transcribe] Audio extracted → {output_path}")
        return output_path
    except ImportError:
        print("[ERROR] ffmpeg-python not installed. Run: pip install ffmpeg-python")
        raise
    except Exception as e:
        print(f"[ERROR] ffmpeg failed: {e}")
        raise


def transcribe_audio(audio_path: str, model_size: str = "base") -> list[TranscriptSegment]:
    """
    Transcribe audio file using OpenAI Whisper.

    Args:
        audio_path: Path to .mp3 / .wav / .m4a file
        model_size: Whisper model size — 'tiny', 'base', 'small', 'medium', 'large'
                    Larger = more accurate but slower.

    Returns:
        List of TranscriptSegment objects with timestamps.
    """
    try:
        import whisper
    except ImportError:
        print("[ERROR] Whisper not installed. Run: pip install openai-whisper")
        raise

    print(f"[Transcribe] Loading Whisper model: {model_size}")
    model = whisper.load_model(model_size)

    print(f"[Transcribe] Transcribing: {audio_path}")
    result = model.transcribe(audio_path, verbose=False)

    segments = [
        TranscriptSegment(
            id=i,
            start=seg["start"],
            end=seg["end"],
            text=seg["text"].strip()
        )
        for i, seg in enumerate(result["segments"])
    ]

    print(f"[Transcribe] Done. {len(segments)} segments, {len(result['text'].split())} words.")
    return segments


def save_transcript(segments: list[TranscriptSegment], output_path: str = "transcript.json") -> None:
    """Save transcript segments to a JSON file."""
    data = {
        "total_segments": len(segments),
        "total_duration_seconds": segments[-1].end if segments else 0,
        "segments": [asdict(s) for s in segments]
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"[Transcribe] Transcript saved → {output_path}")


def print_transcript(segments: list[TranscriptSegment]) -> None:
    """Pretty-print transcript to console."""
    print("\n" + "=" * 60)
    print("  FULL TRANSCRIPT WITH TIMESTAMPS")
    print("=" * 60)
    for seg in segments:
        print(f"[{seg.start_formatted} → {seg.end_formatted}] {seg.text}")


# ---------------------------------------------------------------------------
# CLI ENTRYPOINT
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Whisper transcription module")
    parser.add_argument("--input", required=True, help="Path to video or audio file")
    parser.add_argument("--model", default="base", choices=["tiny", "base", "small", "medium", "large"])
    parser.add_argument("--output", default="transcript.json", help="Output JSON path")
    args = parser.parse_args()

    input_path = args.input
    audio_path = input_path

    # Extract audio if input is a video file
    video_extensions = {".mp4", ".mov", ".avi", ".mkv", ".webm"}
    if Path(input_path).suffix.lower() in video_extensions:
        audio_path = "temp_audio.mp3"
        extract_audio_from_video(input_path, audio_path)

    segments = transcribe_audio(audio_path, model_size=args.model)
    print_transcript(segments)
    save_transcript(segments, args.output)


if __name__ == "__main__":
    main()

"""
viral_extractor.py – GPT-Powered Viral Segment Detector
Task 4: The Multimodal Content Engine
DecodeLabs Generative AI Internship | Batch 2026

Takes a transcript and uses GPT-4o to identify the 5 most
"viral-worthy" segments — moments that would perform well
as short-form Reels, TikToks, or YouTube Shorts.
"""

import os
import json
from openai import OpenAI

# ---------------------------------------------------------------------------
# VIRAL SEGMENT DETECTION PROMPT
# ---------------------------------------------------------------------------
VIRAL_DETECTION_PROMPT = """
You are a viral content strategist and social media expert with 10 years of experience
creating short-form content that gets millions of views.

Given the transcript below, identify the 5 most viral-worthy segments.

A viral segment should have ONE OR MORE of these qualities:
- Surprising or counterintuitive fact
- Strong emotional hook (inspiring, funny, shocking, relatable)
- Quotable one-liner or "mic drop" moment
- Practical tip that gives immediate value
- Storytelling moment with tension and resolution
- Data point or statistic that challenges assumptions

For each segment, return:
1. "segment_id" — index number (1–5)
2. "start_time" — approximate start time in MM:SS format
3. "end_time" — approximate end time in MM:SS format
4. "transcript_excerpt" — the exact text of the segment (verbatim)
5. "viral_score" — score from 1–10 estimating viral potential
6. "viral_reason" — one sentence explaining why this segment is viral-worthy
7. "reel_type" — one of: ["Motivational", "Educational", "Shocking", "Funny", "Inspirational", "How-To"]

Return ONLY a valid JSON array. No preamble, no markdown fences.

TRANSCRIPT:
{transcript}
"""


def format_transcript_for_prompt(segments: list[dict]) -> str:
    """Format transcript segments into a readable string for the prompt."""
    lines = []
    for seg in segments:
        start_m, start_s = divmod(int(seg.get("start", 0)), 60)
        end_m, end_s = divmod(int(seg.get("end", 0)), 60)
        timestamp = f"[{start_m:02d}:{start_s:02d} → {end_m:02d}:{end_s:02d}]"
        lines.append(f"{timestamp} {seg['text']}")
    return "\n".join(lines)


def extract_viral_segments(
    transcript_segments: list[dict],
    api_key: str,
    model: str = "gpt-4o",
    n_segments: int = 5
) -> list[dict]:
    """
    Use GPT-4o to identify viral segments from a transcript.

    Args:
        transcript_segments: List of segment dicts with 'start', 'end', 'text' keys
        api_key: OpenAI API key
        model: GPT model to use
        n_segments: Number of viral segments to extract (default 5)

    Returns:
        List of viral segment dicts
    """
    client = OpenAI(api_key=api_key)

    formatted_transcript = format_transcript_for_prompt(transcript_segments)

    prompt = VIRAL_DETECTION_PROMPT.format(transcript=formatted_transcript)

    print(f"[ViralExtractor] Analyzing transcript with {model}...")
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=2000
    )

    raw_output = response.choices[0].message.content.strip()

    # Clean JSON fences if present
    if raw_output.startswith("```"):
        raw_output = raw_output.split("```")[1]
        if raw_output.startswith("json"):
            raw_output = raw_output[4:]

    try:
        viral_segments = json.loads(raw_output)
        print(f"[ViralExtractor] Identified {len(viral_segments)} viral segments.")
        return viral_segments[:n_segments]
    except json.JSONDecodeError as e:
        print(f"[ERROR] Failed to parse viral segments JSON: {e}")
        print(f"Raw output:\n{raw_output}")
        return []


def print_viral_segments(segments: list[dict]) -> None:
    """Pretty-print viral segments to console."""
    print("\n" + "=" * 60)
    print("  🔥 TOP VIRAL SEGMENTS IDENTIFIED")
    print("=" * 60)
    for seg in segments:
        print(f"\n▶ Segment {seg.get('segment_id', '?')} | Score: {seg.get('viral_score', '?')}/10 | Type: {seg.get('reel_type', '?')}")
        print(f"  ⏱️  {seg.get('start_time', '?')} → {seg.get('end_time', '?')}")
        print(f"  📝 \"{seg.get('transcript_excerpt', '')}\"")
        print(f"  💡 Why viral: {seg.get('viral_reason', '')}")


if __name__ == "__main__":
    # Demo with sample transcript
    sample_transcript = [
        {"start": 0, "end": 15, "text": "Most people think success is about working harder, but the data actually shows something completely different."},
        {"start": 15, "end": 35, "text": "A study of 500 top performers found that they all had one habit in common — they protected their mornings like a boardroom meeting."},
        {"start": 35, "end": 55, "text": "And here is the shocking part: 78% of them said that a single 90-minute deep work block in the morning replaced 4 hours of regular work."},
        {"start": 55, "end": 80, "text": "So I tried it for 30 days. No phone, no email, just the hardest task on my list. The results were honestly embarrassing compared to my old routine."},
        {"start": 80, "end": 110, "text": "The second thing they all did was what I call 'decision batching' — making all their small decisions once a week to preserve mental energy for what actually matters."},
    ]

    api_key = os.getenv("OPENAI_API_KEY", "your-api-key-here")
    segments = extract_viral_segments(sample_transcript, api_key)
    print_viral_segments(segments)

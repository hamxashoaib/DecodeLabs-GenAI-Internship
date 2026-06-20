"""
caption_generator.py – Social Media Caption & B-Roll Generator
Task 4: The Multimodal Content Engine
DecodeLabs Generative AI Internship | Batch 2026

Takes viral segments and generates platform-specific captions,
viral headlines, and AI-suggested B-roll descriptions.
"""

import os
import json
from openai import OpenAI


# ---------------------------------------------------------------------------
# CAPTION GENERATION PROMPT
# ---------------------------------------------------------------------------
CAPTION_PROMPT = """
You are a viral social media content creator specializing in short-form video content.

Given the following video segment transcript, generate platform-optimized content assets.

SEGMENT TEXT:
"{segment_text}"

REEL TYPE: {reel_type}
VIRAL SCORE: {viral_score}/10

Generate the following (return ONLY valid JSON, no markdown):

{{
  "instagram_caption": "Caption for Instagram Reel (2–3 sentences + 5 relevant hashtags. Hook in first line.)",
  "tiktok_caption": "Caption for TikTok (shorter, punchy, 1–2 sentences + 3 trending hashtags)",
  "twitter_hook": "Tweet-length hook (max 280 chars). Must make people stop scrolling.",
  "viral_headline": "YouTube/Reel title that maximizes clicks (under 70 chars, use power words)",
  "broll_descriptions": [
    "B-roll shot 1: Detailed visual description for the video editor (what to show on screen)",
    "B-roll shot 2: Another visual suggestion",
    "B-roll shot 3: Another visual suggestion"
  ],
  "on_screen_text": "Bold text overlay for the first 3 seconds of the Reel (the hook text)",
  "cta": "Call-to-action for the end of the Reel (short, 1 sentence)"
}}
"""


def generate_caption_for_segment(
    segment: dict,
    api_key: str,
    model: str = "gpt-4o"
) -> dict:
    """
    Generate all content assets for a single viral segment.

    Args:
        segment: Viral segment dict from viral_extractor.py
        api_key: OpenAI API key
        model: GPT model to use

    Returns:
        Dict with all generated content assets
    """
    client = OpenAI(api_key=api_key)

    prompt = CAPTION_PROMPT.format(
        segment_text=segment.get("transcript_excerpt", ""),
        reel_type=segment.get("reel_type", "Educational"),
        viral_score=segment.get("viral_score", 7)
    )

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=800
    )

    raw = response.choices[0].message.content.strip()

    # Clean JSON fences
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    try:
        content = json.loads(raw)
        content["segment_id"] = segment.get("segment_id")
        content["start_time"] = segment.get("start_time")
        content["end_time"] = segment.get("end_time")
        content["original_text"] = segment.get("transcript_excerpt")
        return content
    except json.JSONDecodeError:
        return {
            "segment_id": segment.get("segment_id"),
            "error": "Failed to parse response",
            "raw": raw
        }


def generate_all_captions(
    viral_segments: list[dict],
    api_key: str,
    model: str = "gpt-4o"
) -> list[dict]:
    """Generate content assets for all viral segments."""
    print(f"\n[CaptionGenerator] Generating captions for {len(viral_segments)} segments...")
    results = []
    for i, segment in enumerate(viral_segments):
        print(f"  → Segment {i+1}/{len(viral_segments)}...")
        content = generate_caption_for_segment(segment, api_key, model)
        results.append(content)
    return results


def print_content_assets(content_list: list[dict]) -> None:
    """Pretty-print all generated content assets."""
    print("\n" + "=" * 60)
    print("  📱 GENERATED CONTENT ASSETS")
    print("=" * 60)
    for item in content_list:
        seg_id = item.get("segment_id", "?")
        print(f"\n{'─'*50}")
        print(f"🎬 REEL {seg_id} | {item.get('start_time', '?')} → {item.get('end_time', '?')}")
        print(f"{'─'*50}")
        print(f"\n📢 Viral Headline:\n  {item.get('viral_headline', 'N/A')}")
        print(f"\n📌 On-Screen Hook Text:\n  {item.get('on_screen_text', 'N/A')}")
        print(f"\n📸 Instagram:\n  {item.get('instagram_caption', 'N/A')}")
        print(f"\n🎵 TikTok:\n  {item.get('tiktok_caption', 'N/A')}")
        print(f"\n🐦 Twitter/X Hook:\n  {item.get('twitter_hook', 'N/A')}")
        print(f"\n🎥 B-Roll Suggestions:")
        for broll in item.get("broll_descriptions", []):
            print(f"   • {broll}")
        print(f"\n✅ CTA: {item.get('cta', 'N/A')}")


if __name__ == "__main__":
    # Demo
    sample_segments = [
        {
            "segment_id": 1,
            "start_time": "00:35",
            "end_time": "00:55",
            "transcript_excerpt": "78% of top performers said a single 90-minute deep work block replaced 4 hours of regular work.",
            "reel_type": "Educational",
            "viral_score": 9
        }
    ]
    api_key = os.getenv("OPENAI_API_KEY", "your-api-key-here")
    results = generate_all_captions(sample_segments, api_key)
    print_content_assets(results)

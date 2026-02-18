#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "google-genai>=1.0.0",
#     "pillow>=10.0.0",
#     "requests>=2.31.0",
# ]
# ///
"""
Generate images using Google's Nano Banana Pro (Gemini 3 Pro Image) API or OpenRouter.
"""

import argparse
import os
import sys
import base64
import requests
import json
from io import BytesIO
from pathlib import Path

def get_api_key(provided_key: str | None, env_var: str) -> str | None:
    if provided_key:
        return provided_key
    return os.environ.get(env_var)

def main():
    parser = argparse.ArgumentParser(description="Generate images via Gemini 3 Pro Image (Native/OpenRouter)")
    parser.add_argument("--prompt", "-p", required=True, help="Image description/prompt")
    parser.add_argument("--filename", "-f", required=True, help="Output filename")
    parser.add_argument("--input-image", "-i", action="append", dest="input_images", help="Input image path(s)")
    parser.add_argument("--resolution", "-r", choices=["1K", "2K", "4K"], default="1K", help="Output resolution")
    parser.add_argument("--api-key", "-k", help="API key override")
    args = parser.parse_args()

    # Determine Backend
    openrouter_key = get_api_key(args.api_key, "OPENROUTER_API_KEY")
    gemini_key = get_api_key(args.api_key, "GEMINI_API_KEY")

    if openrouter_key and not gemini_key:
        generate_via_openrouter(openrouter_key, args.prompt, args.filename, args.resolution)
    elif gemini_key:
        generate_via_gemini_native(gemini_key, args.prompt, args.filename, args.resolution, args.input_images)
    else:
        print("Error: No API key found (GEMINI_API_KEY or OPENROUTER_API_KEY).", file=sys.stderr)
        sys.exit(1)

def generate_via_openrouter(api_key, prompt, filename, resolution):
    print(f"Generating image via OpenRouter with resolution {resolution}...")
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://openclaw.ai",
        "X-Title": "OpenClaw Alpha"
    }
    
    # Gemini 3 Pro Image handles resolution via content parameters or model strings.
    # OpenRouter uses model google/gemini-3-pro-image-preview
    # It returns modalities including image data.
    payload = {
        "model": "google/gemini-3-pro-image-preview",
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"}
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=90)
        response.raise_for_status()
        data = response.json()
        
        # Check for image data in the response content or tool calls
        # For Gemini-3-pro-image on OR, it usually returns text with a b64 string or a direct block.
        content = data['choices'][0]['message'].get('content', "")
        
        # If content is a URL or JSON containing b64
        if "data:image" in content or "base64" in content.lower():
            # Extract b64
            import re
            b64_match = re.search(r"data:image/[^;]+;base64,([^\"]+)", content)
            if b64_match:
                img_data = base64.b64decode(b64_match.group(1))
                save_bytes_as_png(img_data, filename)
                return

        # Fallback: check if OpenRouter wrapped the image in the 'parts' or structured fields
        # Note: OpenRouter mapping for this specific model sometimes returns a direct URL.
        print(f"Model responded: {content[:100]}...")
        print("Error: Could not find image data in OpenRouter response. The model might have returned text only.", file=sys.stderr)
        sys.exit(1)
        
    except Exception as e:
        print(f"Error via OpenRouter: {e}", file=sys.stderr)
        sys.exit(1)

def save_bytes_as_png(img_data, filename):
    from PIL import Image as PILImage
    img = PILImage.open(BytesIO(img_data))
    img.save(filename, "PNG")
    print(f"Image saved: {Path(filename).resolve()}")
    print(f"MEDIA: {Path(filename).resolve()}")

def generate_via_gemini_native(api_key, prompt, filename, resolution, input_images_paths):
    from google import genai
    from google.genai import types
    from PIL import Image as PILImage
    
    print(f"Generating image via Native Gemini with resolution {resolution}...")
    client = genai.Client(api_key=api_key)
    
    contents = prompt
    if input_images_paths:
        input_images = [PILImage.open(img) for img in input_images_paths]
        contents = [*input_images, prompt]

    try:
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
                image_config=types.ImageConfig(image_size=resolution)
            )
        )
        
        for part in response.parts:
            if part.inline_data:
                img_data = part.inline_data.data
                if isinstance(img_data, str):
                    img_data = base64.b64decode(img_data)
                save_bytes_as_png(img_data, filename)
                return
        print("Error: No image in native response.", file=sys.stderr)
    except Exception as e:
        print(f"Native Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

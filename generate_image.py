#!/usr/bin/env python3
"""
Image Generation Script using OpenRouter API
Usage: python3 generate_image.py "your prompt here" [--output file.png] [--model model-id] [--aspect-ratio 16:9] [--size 4K]
"""

import requests
import json
import base64
import os
import argparse
import sys


def generate_image(
    prompt: str,
    output_file: str = "generated_image.png",
    model: str = "google/gemini-2.5-flash-image",
    aspect_ratio: str = None,
    image_size: str = None,
):
    """Generate an image using OpenRouter API"""
    
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: OPENROUTER_API_KEY environment variable not set")
        sys.exit(1)
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "modalities": ["image", "text"]
    }
    
    # Add image config if specified
    if aspect_ratio or image_size:
        payload["image_config"] = {}
        if aspect_ratio:
            payload["image_config"]["aspect_ratio"] = aspect_ratio
        if image_size:
            payload["image_config"]["image_size"] = image_size
    
    print(f"Generating image with prompt: {prompt}")
    print(f"Model: {model}")
    if aspect_ratio:
        print(f"Aspect ratio: {aspect_ratio}")
    if image_size:
        print(f"Image size: {image_size}")
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        sys.exit(1)
    
    # Check for errors
    if "error" in result:
        print(f"Error from API: {result['error']}")
        sys.exit(1)
    
    # Extract image
    if result.get("choices") and result["choices"][0]["message"].get("images"):
        message = result["choices"][0]["message"]
        image_url = message["images"][0]["image_url"]["url"]
        
        # Remove data URL prefix and decode
        if "base64," in image_url:
            base64_data = image_url.split("base64,", 1)[1]
        else:
            base64_data = image_url
        
        try:
            with open(output_file, "wb") as f:
                f.write(base64.b64decode(base64_data))
            print(f"\n✓ Image saved to: {output_file}")
            
            # Print assistant response if available
            if message.get("content"):
                print(f"\nAssistant: {message['content']}")
        except Exception as e:
            print(f"Error saving image: {e}")
            sys.exit(1)
    else:
        print("Error: No image generated in response")
        print(f"Response: {json.dumps(result, indent=2)}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using OpenRouter API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "a cute banana wearing sunglasses"
  %(prog)s "sunset over mountains" --output sunset.png
  %(prog)s "cityscape" --model google/gemini-3-pro-image-preview --aspect-ratio 16:9 --size 4K
  
Available aspect ratios: 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9
Available sizes: 1K, 2K, 4K

Available models:
  google/gemini-2.5-flash-image (default, fast & cheap)
  google/gemini-3-pro-image-preview (higher quality)
  openai/gpt-5-image-mini
  openai/gpt-5-image
"""
    )
    
    parser.add_argument("prompt", help="Text prompt describing the image to generate")
    parser.add_argument(
        "-o", "--output",
        default="generated_image.png",
        help="Output file path (default: generated_image.png)"
    )
    parser.add_argument(
        "-m", "--model",
        default="google/gemini-2.5-flash-image",
        help="Model to use (default: google/gemini-2.5-flash-image)"
    )
    parser.add_argument(
        "-a", "--aspect-ratio",
        help="Aspect ratio (e.g., 16:9) - Gemini models only"
    )
    parser.add_argument(
        "-s", "--size",
        choices=["1K", "2K", "4K"],
        help="Image size - Gemini models only"
    )
    
    args = parser.parse_args()
    
    generate_image(
        prompt=args.prompt,
        output_file=args.output,
        model=args.model,
        aspect_ratio=args.aspect_ratio,
        image_size=args.size
    )


if __name__ == "__main__":
    main()

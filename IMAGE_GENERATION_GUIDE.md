# Image Generation with OpenRouter

## Overview

OpenRouter provides access to multiple AI image generation models through a unified API. You can generate images using text prompts, with options for different aspect ratios, resolutions, and models.

## Available Models

The following image generation models are currently available:

| Model ID | Cost (per 1M tokens) | Notes |
|----------|---------------------|-------|
| `google/gemini-2.5-flash-image` | $0.30 prompt / $2.50 completion | **Recommended** - Fast, cheap, good quality |
| `google/gemini-3-pro-image-preview` | $2.00 prompt / $12.00 completion | Higher quality, supports more config options |
| `openai/gpt-5-image-mini` | $2.50 prompt / $2.00 completion | OpenAI's smaller image model |
| `openai/gpt-5-image` | $10.00 prompt / $10.00 completion | OpenAI's full image model |

## Quick Start

### Using the CLI Script

A ready-to-use bash script is available:

```bash
# Basic usage
./generate_image.sh "a cute banana wearing sunglasses"

# Specify output file
./generate_image.sh "a sunset over mountains" sunset.png

# Use a different model
./generate_image.sh "abstract art" output.png "google/gemini-3-pro-image-preview"
```

### Using curl directly

```bash
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer ${OPENROUTER_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "google/gemini-2.5-flash-image",
    "messages": [
      {
        "role": "user",
        "content": "Generate an image of a futuristic cityscape"
      }
    ],
    "modalities": ["image", "text"]
  }'
```

### Using Python

```python
import requests
import json
import base64
import os

def generate_image(prompt, output_file="generated.png", model="google/gemini-2.5-flash-image"):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
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
    
    response = requests.post(url, headers=headers, json=payload)
    result = response.json()
    
    if result.get("choices"):
        message = result["choices"][0]["message"]
        if message.get("images"):
            # Extract base64 image data
            image_url = message["images"][0]["image_url"]["url"]
            # Remove data URL prefix
            base64_data = image_url.split(",", 1)[1]
            # Decode and save
            with open(output_file, "wb") as f:
                f.write(base64.b64decode(base64_data))
            print(f"Image saved to: {output_file}")
            print(f"Assistant: {message.get('content', '')}")
        else:
            print("No image generated")
    else:
        print(f"Error: {result}")

# Example usage
generate_image("a cyberpunk banana in neon lights")
```

### Using Node.js/TypeScript

```typescript
import fs from 'fs';

async function generateImage(
  prompt: string, 
  outputFile: string = 'generated.png',
  model: string = 'google/gemini-2.5-flash-image'
) {
  const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.OPENROUTER_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model,
      messages: [
        {
          role: 'user',
          content: prompt,
        },
      ],
      modalities: ['image', 'text'],
    }),
  });

  const result = await response.json();

  if (result.choices && result.choices[0].message.images) {
    const imageUrl = result.choices[0].message.images[0].image_url.url;
    // Remove data URL prefix
    const base64Data = imageUrl.split(',')[1];
    // Decode and save
    fs.writeFileSync(outputFile, Buffer.from(base64Data, 'base64'));
    console.log(`Image saved to: ${outputFile}`);
    console.log(`Assistant: ${result.choices[0].message.content}`);
  } else {
    console.log('No image generated');
  }
}

// Example usage
generateImage('a banana in space');
```

## Advanced Configuration

### Aspect Ratios (Gemini models)

```json
{
  "image_config": {
    "aspect_ratio": "16:9"
  }
}
```

Supported ratios: `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`

### Image Size (Gemini models)

```json
{
  "image_config": {
    "image_size": "4K"
  }
}
```

Options: `1K` (default), `2K`, `4K`

### Combined Example

```bash
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer ${OPENROUTER_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "google/gemini-3-pro-image-preview",
    "messages": [
      {
        "role": "user",
        "content": "Create a cinematic wide shot of a nano banana in a fancy restaurant"
      }
    ],
    "modalities": ["image", "text"],
    "image_config": {
      "aspect_ratio": "16:9",
      "image_size": "4K"
    }
  }'
```

## Response Format

Images are returned as base64-encoded data URLs in the response:

```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "I've generated your image.",
        "images": [
          {
            "type": "image_url",
            "image_url": {
              "url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
            }
          }
        ]
      }
    }
  ]
}
```

## Environment Setup

Ensure the OpenRouter API key is set:

```bash
export OPENROUTER_API_KEY="sk-or-v1-..."
```

The API key is already available in this environment.

## Pricing Considerations

- **Gemini 2.5 Flash Image** is the most cost-effective option for most use cases
- Higher resolution (4K) and premium models cost more
- Some models charge per image, others per token
- Always check current pricing at https://openrouter.ai/models

## Troubleshooting

### No image in response
- Verify the model supports image generation (`output_modalities` includes `"image"`)
- Ensure `modalities: ["image", "text"]` is set (or just `["image"]` for image-only models)
- Check that your prompt clearly requests an image

### Error: "Model not found"
- Use the models page to find available models: https://openrouter.ai/models
- Filter by output modalities to see image-capable models

### Base64 decoding errors
- Ensure you're stripping the `data:image/png;base64,` prefix before decoding
- Check for complete data transmission in your HTTP client

## Additional Resources

- OpenRouter Docs: https://openrouter.ai/docs/guides/overview/multimodal/image-generation
- Models List: https://openrouter.ai/models
- API Reference: https://openrouter.ai/docs/api/reference/overview

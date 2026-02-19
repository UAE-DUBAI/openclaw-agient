# Image Generation Capabilities Report

**Date:** 2026-02-15  
**Status:** ✓ Fully Operational

## Summary

OpenRouter provides full image generation capabilities through multiple AI models accessible via REST API. The system is working and tested with both CLI and programmatic interfaces.

## What's Available

### 1. API Access
- **Endpoint:** `https://openrouter.ai/api/v1/chat/completions`
- **Authentication:** Bearer token (API key already configured in environment)
- **Method:** POST with JSON payload

### 2. Available Models

| Model | Cost (per 1M tokens) | Best For |
|-------|---------------------|----------|
| **google/gemini-2.5-flash-image** | $0.30 / $2.50 | Default choice - fast, cheap, good quality |
| google/gemini-3-pro-image-preview | $2.00 / $12.00 | Higher quality, advanced config options |
| openai/gpt-5-image-mini | $2.50 / $2.00 | OpenAI alternative |
| openai/gpt-5-image | $10.00 / $10.00 | Premium quality |

**Recommendation:** Use `google/gemini-2.5-flash-image` for most purposes.

### 3. Ready-to-Use Tools

#### Bash Script: `generate_image.sh`
```bash
# Simple usage
./generate_image.sh "your prompt here"

# With custom output
./generate_image.sh "a sunset" sunset.png

# With specific model
./generate_image.sh "abstract art" art.png "google/gemini-3-pro-image-preview"
```

**Status:** ✓ Tested and working

#### Python Script: `generate_image.py`
```bash
# Basic usage
python3 generate_image.py "your prompt"

# Full options
python3 generate_image.py "cityscape" \
  --output city.png \
  --model google/gemini-3-pro-image-preview \
  --aspect-ratio 16:9 \
  --size 4K
```

**Features:**
- Command-line arguments
- Aspect ratio control (1:1, 16:9, 21:9, etc.)
- Image size control (1K, 2K, 4K)
- Error handling
- Help documentation

**Status:** ✓ Tested and working

### 4. Advanced Features

#### Aspect Ratios (Gemini models)
- 1:1 → 1024×1024 (default)
- 16:9 → 1344×768 (widescreen)
- 9:16 → 768×1344 (portrait)
- 21:9 → 1536×672 (ultrawide)
- Plus: 2:3, 3:2, 3:4, 4:3, 4:5, 5:4

#### Image Sizes (Gemini models)
- 1K → Standard resolution (default)
- 2K → Higher resolution
- 4K → Highest resolution

#### Response Format
- Images returned as base64-encoded PNG data
- Embedded in JSON response
- Can include text description from model

## Testing Results

✓ **Test 1:** Basic image generation  
✓ **Test 2:** Bash script with custom output  
✓ **Test 3:** Python script with options  

All tests successful. Generated images confirmed as valid PNG files (1024×1024 default resolution).

## Integration Options

### 1. Direct API Calls (curl)
Best for: Quick scripts, testing, simple automation

### 2. Bash Script
Best for: Terminal workflows, cron jobs, simple CLI usage

### 3. Python Script
Best for: Advanced automation, integration with Python tools, batch processing

### 4. Custom Integration
The API is REST-based and can be integrated with any language:
- Node.js/TypeScript (see guide)
- Python (requests library)
- Go, Rust, Java, etc.

## How to Use

### Quick Start (5 seconds)
```bash
./generate_image.sh "a happy banana"
```

### With Options
```bash
python3 generate_image.py "cyberpunk cityscape at night" \
  --output cybercity.png \
  --aspect-ratio 16:9 \
  --size 2K
```

### In Code (Python)
```python
import requests, base64, os

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
        "Content-Type": "application/json"
    },
    json={
        "model": "google/gemini-2.5-flash-image",
        "messages": [{"role": "user", "content": "your prompt"}],
        "modalities": ["image", "text"]
    }
)

image_url = response.json()["choices"][0]["message"]["images"][0]["image_url"]["url"]
image_data = base64.b64decode(image_url.split(",")[1])
with open("output.png", "wb") as f:
    f.write(image_data)
```

## Documentation

- **Full Guide:** `IMAGE_GENERATION_GUIDE.md`
- **API Docs:** https://openrouter.ai/docs/guides/overview/multimodal/image-generation
- **Models List:** https://openrouter.ai/models (filter by "image" output modality)

## Cost Estimates

Using default model (gemini-2.5-flash-image):
- Single image: ~$0.001-0.005 (less than a penny)
- 100 images: ~$0.10-0.50
- 1000 images: ~$1-5

Actual cost depends on prompt complexity and model used.

## About "Nano Banana"

🍌 **Discovery:** "Nano Banana" is actually Google's internal nickname for their Gemini image generation models!

- `google/gemini-2.5-flash-image` → "Google: Gemini 2.5 Flash Image (**Nano Banana**)"
- `google/gemini-3-pro-image-preview` → "Google: **Nano Banana Pro**"

These are the models you're looking for!

## Limitations & Notes

1. **Rate Limits:** Subject to OpenRouter's rate limits (check account)
2. **Model-Specific Features:** Advanced config (aspect ratio, size) only works with Gemini models
3. **Response Time:** Image generation takes 5-15 seconds typically
4. **Output Format:** Always PNG, base64-encoded in response

## Next Steps / Recommendations

1. **For immediate use:** Run `./generate_image.sh "your idea"` 
2. **For integration:** Use the Python script or build on the API examples
3. **For advanced needs:** Check IMAGE_GENERATION_GUIDE.md for all options
4. **For cost optimization:** Stick with gemini-2.5-flash-image unless you need premium quality

## Conclusion

✅ **Image generation is fully operational and easy to use.**

Three working implementations are ready:
1. Bash script for quick CLI usage
2. Python script with full options
3. Complete API documentation for custom integration

All tested and confirmed working with the configured OpenRouter API key.

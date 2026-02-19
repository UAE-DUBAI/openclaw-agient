#!/bin/bash
# Image Generation Script using OpenRouter API
# Usage: ./generate_image.sh "your prompt here" [output_file.png] [model]

set -e

PROMPT="${1:-Generate a simple test image}"
OUTPUT_FILE="${2:-generated_image.png}"
MODEL="${3:-google/gemini-2.5-flash-image}"

if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "Error: OPENROUTER_API_KEY environment variable not set"
    exit 1
fi

echo "Generating image with prompt: $PROMPT"
echo "Model: $MODEL"

# Make API request and extract base64 image
RESPONSE=$(curl -s https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer ${OPENROUTER_API_KEY}" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"${MODEL}\",
    \"messages\": [
      {
        \"role\": \"user\",
        \"content\": \"${PROMPT}\"
      }
    ],
    \"modalities\": [\"image\", \"text\"]
  }")

# Check for errors
if echo "$RESPONSE" | jq -e '.error' > /dev/null 2>&1; then
    echo "Error from API:"
    echo "$RESPONSE" | jq '.error'
    exit 1
fi

# Extract and decode the base64 image
IMAGE_URL=$(echo "$RESPONSE" | jq -r '.choices[0].message.images[0].image_url.url')

if [ -z "$IMAGE_URL" ] || [ "$IMAGE_URL" = "null" ]; then
    echo "Error: No image generated"
    echo "Response:"
    echo "$RESPONSE" | jq '.'
    exit 1
fi

# Remove the data URL prefix and decode
echo "$IMAGE_URL" | sed 's/^data:image\/[^;]*;base64,//' | base64 -d > "$OUTPUT_FILE"

echo "Image saved to: $OUTPUT_FILE"
echo ""
echo "Assistant response:"
echo "$RESPONSE" | jq -r '.choices[0].message.content'

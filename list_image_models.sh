#!/bin/bash
# List all available image generation models from OpenRouter

if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "Error: OPENROUTER_API_KEY environment variable not set"
    exit 1
fi

echo "Available Image Generation Models:"
echo "=================================="
echo ""

curl -s https://openrouter.ai/api/v1/models \
  -H "Authorization: Bearer ${OPENROUTER_API_KEY}" \
  | jq -r '.data[] | 
    select(.architecture.output_modalities != null) | 
    select(.architecture.output_modalities | any(. == "image")) | 
    "Model: \(.id)\n  Name: \(.name)\n  Prompt: $\(.pricing.prompt) per 1M tokens\n  Completion: $\(.pricing.completion) per 1M tokens\n  Context: \(.context_length) tokens\n"'

echo ""
echo "Recommended: google/gemini-2.5-flash-image (fast & cheap)"

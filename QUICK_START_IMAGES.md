# Quick Start: Image Generation

## TL;DR

```bash
# Generate an image in one line:
./generate_image.sh "your idea here"
```

That's it! Output saved to `generated_image.png`

## Common Use Cases

### Basic Image
```bash
./generate_image.sh "a sunset over mountains"
```

### Custom Output File
```bash
./generate_image.sh "a cat in space" cat_space.png
```

### High Quality (16:9, 4K)
```bash
python3 generate_image.py "cinematic landscape" \
  --aspect-ratio 16:9 \
  --size 4K \
  --output landscape.png
```

### Different Model
```bash
./generate_image.sh "abstract art" art.png "google/gemini-3-pro-image-preview"
```

## Files Created

- ✓ `generate_image.sh` - Bash script (simple & fast)
- ✓ `generate_image.py` - Python script (full featured)
- ✓ `IMAGE_GENERATION_GUIDE.md` - Complete documentation
- ✓ `IMAGE_GENERATION_REPORT.md` - Status & capabilities report

## Cost

~$0.001-0.005 per image (less than a penny) using default model.

## Help

```bash
python3 generate_image.py --help
```

## Test Results

✓ Bash script: Working  
✓ Python script: Working  
✓ Test images generated successfully

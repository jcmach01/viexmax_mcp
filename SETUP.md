# ViewMax Studio MCP - Setup Guide

## Overview

This is an MCP (Model Context Protocol) server for ViewMax Studio that enables Claude to:
1. Generate detailed video prompts and narrative scripts based on your ideas
2. Submit videos to ViewMax for generation
3. Check the status of video generation tasks

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file in the same directory as `viewmax_mcp.py`:

```
VIEWMAX_API_KEY=sk-DaUWYNnOPIlu58pZJSbEW1Cf7ZHkZNk1
```

Replace the key with your actual ViewMax API key.

### 3. Run the Server

```bash
python viewmax_mcp.py
```

You should see output indicating the server is running.

## Configuration

### API Key

The MCP requires a valid ViewMax API key. Set it as an environment variable:

```bash
export VIEWMAX_API_KEY="your-api-key-here"
```

### Default Settings

The MCP comes with these defaults (can be modified in code):

- **Video Duration**: 10 seconds
- **Aspect Ratio**: 9:16 (YouTube Shorts format)
- **Video Quality**: Standard
- **Audio**: Enabled (for narrative/voiceover)

To change these, edit the constants at the top of `viewmax_mcp.py`:

```python
DURATION = 10  # in seconds
ASPECT_RATIO = "9:16"
QUALITY = "standard"  # or "high"
GENERATE_AUDIO = True
```

## Available Tools

### 1. Generate Prompt & Script
- **Tool**: `viewmax_generate_prompt_and_script`
- **Input**: Your video idea + optional format
- **Output**: Detailed prompt + narrative script (both ≤2000 chars)
- **Format Options**:
  - `shoppable_video` - Product showcases, unboxing
  - `viral_hook` - Fast-paced, eye-catching openings
  - `trending` - Current trending formats
  - `meme` - Comedic, funny content
  - `pov_roleplay` - Immersive, character-driven
  - `reaction` - Fast emotional responses
  - `storytelling` - Narrative-driven with emotional arc

### 2. Submit Video
- **Tool**: `viewmax_submit_video`
- **Input**: Approved prompt + script
- **Output**: Task ID + estimated credits
- **Auto-selects** the best AI model based on format
- **Shows cost before submitting** (2000 char limit enforced)

### 3. Check Task Status
- **Tool**: `viewmax_check_task_status`
- **Input**: Task ID (from submission)
- **Output**: Status (pending/processing/success/failed) + video URL if ready
- **Non-destructive** - safe to call repeatedly

## Workflow

1. **Ask Claude for a prompt**
   ```
   "Give me a prompt for a cute animals video with a sad story"
   ```
   Claude will ask which format you want (storytelling, viral hook, etc.)

2. **Review the generated prompt and script**
   - Prompt: Instructions for the AI video generator
   - Script: Narrative for voiceover/text-to-speech

3. **Approve and submit**
   ```
   Claude shows: "This will cost 120 credits. Ready to submit?"
   ```
   You confirm and the video generation task is created.

4. **Check status manually**
   - Log into ViewMax dashboard
   - Or ask Claude to check with the task ID

## AI Models Available

The MCP automatically selects the best model for each format:

### Storytelling (Best)
- **Seedance 1.5 Pro** - Audio-visual sync + film-grade camera
- Runway - Cinematic quality
- Veo 3.1 - High quality with frame control

### Viral Hook
- **Grok Imagine** - Fast, cheap (10-90 credits)
- Gemini Omni Flash - Ultra-fast (4-10s)
- Seedance 2.0 Fast - Fast generation

### Meme
- **Grok Imagine** - Comedic potential
- Veo 3.1 Lite - Budget-friendly (15 credits)
- Gemini Omni Flash - Quick generation

### POV & Roleplay
- **Seedance 1.5 Pro** - Film-grade camera + audio sync
- Runway - Cinematic immersion
- Veo 3.1 - High quality

### Shoppable Video
- **Runway** - Cinematic product focus
- Veo 3.1 Fast - Quick, consistent visuals
- Kling 2.6 - All-around quality

### Trending
- **Kling 2.6** - Versatile, good quality
- Seedance 2.0 Fast - Fast generation
- Grok Imagine - Fast and affordable

### Reaction
- **Gemini Omni Flash** - Ultra-fast (4-10s)
- Grok Imagine - Fast and cheap
- Veo 3.1 Fast - Quick generation

## Character Limits

Both the prompt and script have a **2000 character maximum**:

- **Prompt**: Visual descriptions, camera work, mood, style (≤2000 chars)
- **Script**: Narrative, dialogue, voiceover text (≤2000 chars)

The MCP validates these automatically and prevents submission if exceeded.

## Cost Information

Credit costs vary by model and duration. Examples:

- **Grok Imagine**: 10-90 credits
- **Seedance 2.0 Fast**: 80-495 credits
- **Seedance 1.5 Pro**: 7-60 credits
- **Runway**: 12-30 credits
- **Veo 3.1 Lite**: 15 credits
- **Veo 3.1 Fast**: 30-100 credits
- **Veo 3.1**: 225-285 credits

The MCP will show you the exact cost before submission.

## Troubleshooting

### "VIEWMAX_API_KEY environment variable not set"
- Create a `.env` file with your API key
- Or set it in your environment: `export VIEWMAX_API_KEY="your-key"`

### "Invalid API key"
- Verify your API key is correct
- Check that it hasn't expired in your ViewMax dashboard

### "Rate limit exceeded"
- Wait a few minutes before trying again
- Consider spacing out video submissions

### "Request timed out"
- The API took too long to respond
- Try again in a moment

### Character limit exceeded
- Prompt or script is over 2000 characters
- The MCP will tell you the exact count
- Condense your content and try again

## Integration with Cowork

To use this MCP in Cowork mode:

1. Save `viewmax_mcp.py` and `requirements.txt`
2. Set your API key as an environment variable
3. The MCP will be automatically available in Claude conversations

## Advanced Usage

### Changing Default Settings

Edit the constants in `viewmax_mcp.py`:

```python
# Change duration to 15 seconds
DURATION = 15

# Change quality to high
QUALITY = "high"

# Change aspect ratio (1:1 square, 16:9 landscape)
ASPECT_RATIO = "1:1"
```

### Using Specific Models

When submitting, you can request a specific model:

```
"Submit with Runway for cinematic quality"
```

Claude will use that model instead of auto-selecting.

## More Information

- ViewMax Website: https://viewmax.studio/
- API Documentation: https://viewmax.studio/docs/api
- Support: support@viewmax.studio

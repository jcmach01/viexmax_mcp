# ViewMax Studio MCP

A Model Context Protocol (MCP) server that enables Claude to generate AI videos using ViewMax Studio's powerful video generation tools.

## Features

✅ **Generate Video Prompts & Scripts** - Create detailed prompts for AI video generation with correlated narrative scripts, all within 2000 character limits

✅ **Smart Model Selection** - Automatically selects the best AI model (Seedance, Kling, Runway, etc.) based on your video format

✅ **Cost Preview** - See credit costs before submitting, with automatic validation and approval flow

✅ **Task Status Tracking** - Check video generation progress with task IDs

✅ **7 Video Formats** - Optimized guidelines for storytelling, viral hooks, trending, memes, POV/roleplay, reactions, and shoppable videos

✅ **Character Limit Enforcement** - Validates that prompts and scripts don't exceed ViewMax's 2000 character limit

## Quick Start

### 1. Install
```bash
pip install -r requirements.txt
```

### 2. Configure
Copy `.env.example` to `.env` and add your ViewMax API key:
```bash
cp .env.example .env
# Edit .env and add your API key
```

### 3. Run
```bash
python viewmax_mcp.py
```

### 4. Use with Claude
Ask Claude to generate a video:
```
"Give me a prompt for a cute animals video with a sad story"
```

Claude will:
1. Ask which format you want (if not specified)
2. Generate a detailed prompt + narrative script
3. Show you the character counts
4. Ask for approval
5. Submit to ViewMax and show the task ID
6. Let you check status manually

## Workflow Example

```
User: "Create a viral hook about coffee shops"

Claude: Which format would you prefer?
- Viral Hook (fast-paced, eye-catching)
- Trending (universal appeal)
- etc.

User: "Viral Hook"

Claude: Here's your prompt and script:

PROMPT:
[Detailed visual description with camera work, cuts, mood...]

SCRIPT:
[Snappy narration designed for voiceover...]

Prompt: 1,247/2000 characters
Script: 892/2000 characters

Ready to submit? I'll show the credit cost first.

User: "Yes, submit it"

Claude: This will cost 75 credits. Confirm?

User: "Confirm"

Claude: ✅ Video generation started!
Task ID: abc123def456
Model: Grok Imagine

Check status manually in your ViewMax dashboard, or ask me to check with the task ID.
```

## Tools

### 1. Generate Prompt & Script
Creates a detailed video prompt and narrative script based on your idea and format.

**Input:**
- `idea` (required): Your video concept
- `format` (optional): One of 7 formats below

**Output:**
- Detailed prompt (≤2000 chars) - for AI video generator
- Narrative script (≤2000 chars) - for voiceover/text-to-speech
- Character counts for both

**Formats:**
1. **Storytelling** - Narrative with emotional arc
2. **Viral Hook** - Fast-paced, eye-catching opener
3. **Trending** - Current trending format
4. **Meme** - Comedic, funny content
5. **POV & Roleplay** - Immersive, character-driven
6. **Reaction** - Fast emotional response
7. **Shoppable Video** - Product showcase

### 2. Submit Video
Submits approved prompt and script to ViewMax for generation. Shows cost and requires confirmation before submission.

**Input:**
- `prompt` (required): Detailed video prompt (≤2000 chars)
- `script` (required): Narrative script (≤2000 chars)
- `model` (optional): AI model (auto-selected if omitted)
- `format` (optional): Video format (helps with model selection)
- `approved` (required): Set to true to confirm submission

**Output:**
- Task ID for status checking
- Credit cost
- Selected AI model
- Confirmation message

### 3. Check Task Status
Polls the status of a video generation task.

**Input:**
- `task_id` (required): Task ID from submission

**Output:**
- Status: pending, processing, success, failed, or canceled
- Video URL (if ready)
- Error details (if failed)

## AI Models

The MCP automatically selects the best model for each format:

| Format | Best Model | Why |
|--------|-----------|-----|
| Storytelling | Seedance 1.5 Pro | Audio-visual sync + film-grade camera |
| Viral Hook | Grok Imagine | Fast, cheap, eye-catching |
| Trending | Kling 2.6 | Versatile, good quality |
| Meme | Grok Imagine | Comedic potential, fast |
| POV & Roleplay | Seedance 1.5 Pro | Cinematic, immersive |
| Reaction | Gemini Omni Flash | Ultra-fast (4-10s) |
| Shoppable Video | Runway | Cinematic product focus |

**Available Models:**
- Seedance 1.5 Pro (7-60 credits)
- Seedance 2.0 (95-1200 credits)
- Seedance 2.0 Fast (80-495 credits)
- Kling 2.6 (55-220 credits)
- Grok Imagine (10-90 credits)
- Runway (12-30 credits)
- Gemini Omni Flash (45-180 credits)
- Veo 3.1 (225-285 credits)
- Veo 3.1 Fast (30-100 credits)
- Veo 3.1 Lite (15 credits)

## Configuration

### Environment Variables

```bash
VIEWMAX_API_KEY=your-api-key-here  # Required
PORT=8000                            # Optional, for HTTP transport
LOG_LEVEL=info                       # Optional
```

### Default Settings

Edit `viewmax_mcp.py` to change:

```python
DURATION = 10              # Video duration in seconds
ASPECT_RATIO = "9:16"      # YouTube Shorts format
QUALITY = "standard"       # or "high"
GENERATE_AUDIO = True      # Enable audio/voiceover
```

## Character Limits

ViewMax enforces 2000 character maximums:

- **Prompt**: 2000 characters (visual descriptions, camera work, mood, style)
- **Script**: 2000 characters (narrative, dialogue, voiceover text)

The MCP validates these automatically and prevents submission if exceeded.

## Cost Information

Credits are consumed based on:
- **AI Model** - Different models cost different amounts
- **Video Duration** - Longer videos cost more
- **Aspect Ratio** - Some ratios cost more than others

The MCP shows you the exact cost before submission, so you know exactly what you're paying.

## Error Handling

The MCP provides clear error messages for:
- Invalid API key
- Rate limits exceeded
- Character limit exceeded
- Network timeouts
- Invalid input formats
- Missing environment variables

## Troubleshooting

### API Key Issues
```bash
# Set API key as environment variable
export VIEWMAX_API_KEY="your-key-here"

# Or create .env file
echo "VIEWMAX_API_KEY=your-key-here" > .env
```

### Character Limit Exceeded
The MCP will tell you the exact character count. Condense your content:
- Use shorter sentences
- Remove redundant descriptions
- Focus on the most important details

### Video Not Generated
1. Check task ID is correct
2. Wait a few minutes (videos take 1-5 minutes)
3. Check for error messages in task status
4. Verify API key is still valid

### Rate Limiting
If you hit rate limits:
- Wait 5-10 minutes before trying again
- Space out video submissions
- Consider using cheaper models (Grok Imagine, Veo 3.1 Lite)

## Project Structure

```
viewmax_mcp/
├── viewmax_mcp.py        # Main MCP server
├── requirements.txt      # Python dependencies
├── .env.example         # Configuration template
├── SETUP.md            # Detailed setup guide
└── README.md           # This file
```

## Development

### Running Tests
```bash
# Verify server starts
python viewmax_mcp.py --help

# Test API connectivity
python -c "
import asyncio
from viewmax_mcp import _make_api_request
asyncio.run(_make_api_request('test'))
"
```

### Adding Custom Models

Edit the `AIModel` enum in `viewmax_mcp.py`:

```python
class AIModel(str, Enum):
    YOUR_NEW_MODEL = "your-new-model-name"
```

Then add format guidance in `FORMAT_GUIDELINES`.

## Integrating with Cowork

To use this MCP in Anthropic's Cowork mode:

1. Place files in your Cowork plugins directory
2. Set `VIEWMAX_API_KEY` environment variable
3. The MCP will automatically appear in Claude conversations

## API Reference

For complete ViewMax API documentation, visit:
https://viewmax.studio/docs/api

## Support

- **ViewMax Support**: support@viewmax.studio
- **API Documentation**: https://viewmax.studio/docs
- **ViewMax Website**: https://viewmax.studio/

## License

This MCP server is provided as-is for use with ViewMax Studio.

## Changelog

### v1.0.0 (Initial Release)
- Generate video prompts and scripts
- Submit videos to ViewMax
- Check task status
- Smart model selection
- Character limit validation
- Cost preview before submission

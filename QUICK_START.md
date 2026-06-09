# ViewMax MCP - Quick Start Guide

## Setup (5 minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Create .env File
```bash
cp .env.example .env
```

Edit `.env` and add your API key (you already have this):
```
VIEWMAX_API_KEY=sk-DaUWYNnOPIlu58pZJSbEW1Cf7ZHkZNk1
```

### Step 3: Run the Server
```bash
python viewmax_mcp.py
```

✅ Done! The MCP is ready to use.

---

## Using It

### Example 1: Generate a Storytelling Video

```
You:    "Give me a prompt for a storytelling video about a cute animal with a sad story"

Claude: [Generates detailed prompt + narrative script]
        Prompt: 1,456/2000 characters
        Script: 987/2000 characters
        
        Ready to submit? I'll show the cost first.

You:    "Yes, submit it"

Claude: This will cost 60 credits for Seedance 1.5 Pro.
        Confirm submission?

You:    "Confirm"

Claude: ✅ Video task created!
        Task ID: abc123
        Check status in your ViewMax dashboard.
```

### Example 2: Generate a Viral Hook

```
You:    "Make a viral hook about coffee shops"

Claude: Here's your prompt and script for viral hook format:
        [Shows details...]
        
        Ready to submit?

You:    "Yes"

Claude: This will cost 45 credits for Grok Imagine.
        Confirm?

You:    "Go ahead"

Claude: ✅ Task created! ID: def456
```

### Example 3: Check Video Status

```
You:    "Check the status of task abc123"

Claude: Status: processing
        Estimated time: 2-3 minutes remaining
        I'll let you know when it's ready!
```

---

## Available Formats

Tell Claude which format you want (or let it guess):

| Format | Best For | Model |
|--------|----------|-------|
| **Storytelling** | Narrative, emotional | Seedance 1.5 Pro |
| **Viral Hook** | Eye-catching opening | Grok Imagine |
| **Trending** | Current trends | Kling 2.6 |
| **Meme** | Funny, comedic | Grok Imagine |
| **POV & Roleplay** | Immersive stories | Seedance 1.5 Pro |
| **Reaction** | Emotional responses | Gemini Omni Flash |
| **Shoppable Video** | Product showcase | Runway |

---

## Tips

### 💰 Save Credits
- Use **Grok Imagine** (10-90 credits) for quick videos
- Use **Veo 3.1 Lite** (15 credits) for budget videos
- Expensive models (Veo 3.1: 225-285 credits) for premium quality

### ⚡ Faster Generation
- **Gemini Omni Flash** generates in 4-10 seconds
- **Grok Imagine** is very fast
- Larger models take 1-5 minutes

### 📝 Character Limits
- Prompt: Max 2000 characters (visual descriptions)
- Script: Max 2000 characters (voiceover text)
- Keep them concise and impactful

### 🎬 Best Practices
1. **Be specific** in your idea description
2. **Use the script** for voiceover content
3. **Choose format** based on your goal
4. **Approve before submitting** - you'll see the cost
5. **Check status manually** in ViewMax dashboard

---

## Common Requests

### "Make a storytelling video about..."
```
User: "Give me a prompt for a storytelling video about [your idea]"
Claude: [Generates with Seedance 1.5 Pro for audio sync]
```

### "Create a viral hook about..."
```
User: "Create a viral hook prompt for [your idea]"
Claude: [Generates with Grok Imagine for fast, eye-catching content]
```

### "Generate a product video about..."
```
User: "Make a shoppable video prompt for [product name]"
Claude: [Generates with Runway for cinematic product focus]
```

### "I want a funny/meme video about..."
```
User: "Create a meme prompt about [your idea]"
Claude: [Generates with Grok Imagine for comedic timing]
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "API key not found" | Set `VIEWMAX_API_KEY` in `.env` |
| "Character limit exceeded" | Shorten your prompt/script |
| "Rate limit exceeded" | Wait 5-10 minutes and try again |
| "Video failed to generate" | Check ViewMax dashboard for error details |
| "Server won't start" | Run `pip install -r requirements.txt` first |

---

## File Organization

```
Your project folder:
├── viewmax_mcp.py          ← Main MCP server
├── requirements.txt        ← Dependencies
├── .env                    ← Your API key (created from .env.example)
├── SETUP.md               ← Detailed setup guide
├── README.md              ← Full documentation
└── QUICK_START.md         ← This file
```

---

## Video Generation Timeline

1. **Submit** - Immediate (seconds)
2. **Queue** - Usually instant
3. **Processing** - 1-5 minutes (varies by model)
4. **Ready** - Video URL available in ViewMax

Check status anytime via ViewMax dashboard or ask Claude to check with task ID.

---

## Next Steps

1. ✅ Install dependencies
2. ✅ Create `.env` with API key
3. ✅ Run `python viewmax_mcp.py`
4. ✅ Ask Claude to generate your first video!

---

## Need Help?

- **Setup issues**: See `SETUP.md`
- **Full documentation**: See `README.md`
- **ViewMax support**: support@viewmax.studio
- **API docs**: https://viewmax.studio/docs/api

---

Enjoy creating videos! 🎬

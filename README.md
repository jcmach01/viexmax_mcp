# ViewMax Studio MCP Server

An MCP (Model Context Protocol) server that enables Claude and other LLM clients to generate AI video prompts with narrative scripts using the ViewMax Studio API.

## Features

- **7 Video Formats**: Shoppable Video, Viral Hook, Trending, Meme, POV & Roleplay, Reaction, Storytelling
- **11 AI Models**: Seedance, Kling, Grok, Runway, Gemini, Veo with automatic model selection
- **Prompt Generation**: Create engaging video prompts tailored to your format
- **Script Generation**: Generate narrative scripts aligned with your prompt
- **Task Tracking**: Monitor video generation progress with task IDs
- **Character Validation**: Enforce 2000-character limits for prompts and scripts
- **HTTP Deployment**: Built with FastMCP for remote HTTP access

## Quick Start

### 1. Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd viewmax-mcp

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your ViewMax API key
```

### 2. Local Development

```bash
# Make sure you're in the virtual environment with dependencies installed
python app.py
```

The server will start at `http://localhost:8000` and be accessible at `http://localhost:8000/mcp`

### 3. Using in Claude Desktop

1. Create/update your `claude_desktop_config.json`:
   - **macOS/Linux**: `~/.config/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

2. Add the MCP server configuration:

```json
{
  "mcpServers": {
    "viewmax": {
      "command": "python",
      "args": ["<path-to>/app.py"],
      "env": {
        "VIEWMAX_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

3. Restart Claude Desktop and the tools should be available

### 4. Using in Cowork

1. In Cowork settings, go to Connectors
2. Add a new connector with type "MCP"
3. Point it to your running server at `http://localhost:8000` (for local testing)
4. Or use the deployed URL for remote access

## Deployment to Railway

### Prerequisites
- Railway account (free tier available at railway.app)
- GitHub repository with your code
- ViewMax API key set as environment variable

### Steps

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial ViewMax MCP server"
   git push origin main
   ```

2. **Deploy on Railway**
   - Connect your GitHub account to Railway
   - Create new project → Deploy from GitHub
   - Select your repository
   - Railway will auto-detect the `Procfile` and run the server

3. **Set Environment Variables**
   - In Railway dashboard, go to Variables
   - Add `VIEWMAX_API_KEY` with your actual API key
   - Railway automatically provides `PORT` environment variable

4. **Access Your Server**
   - Railway provides a public domain like: `https://viexmaxmcp-production.up.railway.app`
   - MCP endpoint: `https://viexmaxmcp-production.up.railway.app/mcp`

### Adding to Claude via Connector

In Cowork Connectors, use the deployed URL:
```
https://viexmaxmcp-production.up.railway.app
```

## API Tools

### 1. `viewmax_generate_prompt_and_script`
Generates both a video prompt and narrative script based on your topic and format.

**Inputs:**
- `topic`: The subject matter for the video
- `format`: One of 7 video formats (shoppable_video, viral_hook, trending, meme, pov_roleplay, reaction, storytelling)
- `duration`: Video length in seconds (15-120, default: 30)
- `style`: Optional style/mood (e.g., "cinematic", "casual")
- `tone`: Optional voice tone (e.g., "professional", "energetic")

**Outputs:**
- Generated prompt (max 2000 characters)
- Generated script (max 2000 characters)
- Selected model and its cost
- Character counts and ready-to-submit status

### 2. `viewmax_submit_video`
Submits a video generation request to ViewMax API.

**Inputs:**
- `prompt`: Your video prompt text
- `script`: Narrative script for the video
- `format`: Video format type
- `model`: AI model to use (from the 11 available)

**Outputs:**
- Task ID for tracking
- Submission status
- Model used and format

### 3. `viewmax_check_task_status`
Checks the progress of a submitted video generation task.

**Inputs:**
- `task_id`: The ID returned from video submission

**Outputs:**
- Current status (generating, completed, failed, etc.)
- Progress percentage
- Estimated completion time
- Video URL (when ready)

## Available Models

| Model | Cost (credits/min) | Quality | Best For |
|-------|------------------|---------|----------|
| Seedance 1.5 Pro | 8.0 | High | General purpose |
| Seedance 2.0 | 10.0 | Very High | Premium quality |
| Seedance 2.0 Fast | 6.0 | High | Quick turnaround |
| Kling 2.6 | 9.0 | Very High | Complex scenes |
| Grok Imagine | 7.0 | High | Creative content |
| Runway | 8.5 | Very High | Professional videos |
| Gemini Omni Flash | 5.0 | Medium-High | Budget-friendly |
| Veo 3.1 | 12.0 | Excellent | Premium production |
| Veo 3.1 Fast | 9.0 | Very High | Fast premium |
| Veo 3.1 Lite | 4.5 | Medium-High | Quick generation |

## Architecture

- **Framework**: FastMCP - Python framework for building MCP servers
- **Transport**: HTTP with ASGI (Starlette/Uvicorn)
- **API Client**: httpx (async HTTP client)
- **Validation**: Pydantic models for type safety
- **Deployment**: Railway with Procfile automation

## Key Implementation Details

1. **HTTP Transport**: Uses `mcp.http_app()` to expose the server as an ASGI application, accessible via HTTP endpoints
2. **Automatic Model Selection**: Recommends optimal model based on video format
3. **Progress Reporting**: Tools report progress in real-time using MCP context
4. **Error Handling**: Comprehensive error messages for validation and API failures
5. **Async/Await**: Non-blocking operations for API calls and progress updates

## Troubleshooting

### "Connection refused" when running locally
- Ensure the server is running: `python app.py`
- Check that port 8000 is not already in use
- Try accessing `http://localhost:8000/mcp` in your browser

### "API Key invalid" error
- Verify your VIEWMAX_API_KEY in the .env file
- Ensure the key hasn't expired
- Check the .env file is being loaded

### MCP server not appearing in Claude
- Restart Claude Desktop after updating configuration
- Check the MCP server logs for startup errors
- Verify the endpoint URL is accessible

## Development

### Testing Locally

```bash
# Run the server
python app.py

# In another terminal, test with curl
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "resources/list",
    "params": {}
  }'
```

### Building on the Existing Code

To extend this MCP server:

1. Add new tools by using the `@mcp.tool` decorator
2. Define new Pydantic models for tool inputs
3. Use `ctx.report_progress()` for long-running tasks
4. Add API calls to ViewMax endpoints as needed

## License

MIT License - See LICENSE file for details

## Support

For issues or questions:
1. Check the README troubleshooting section
2. Review the FastMCP documentation: https://gofastmcp.com
3. Check ViewMax API documentation for API-specific issues

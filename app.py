"""
ViewMax Studio MCP Server - HTTP ASGI Application
Generates AI video prompts with narrative scripts using FastMCP HTTP transport
"""

import os
import asyncio
from typing import Literal
from pydantic import BaseModel, Field
import httpx
from fastmcp import FastMCP, Context

# Initialize FastMCP server
mcp = FastMCP("ViewMax Studio")

# ViewMax API Configuration
VIEWMAX_API_KEY = os.getenv("VIEWMAX_API_KEY", "sk-DaUWYNnOPIlu58pZJSbEW1Cf7ZHkZNk1")
VIEWMAX_BASE_URL = "https://api.viewmax.ai"

# AI Models with costs (credits per minute)
AI_MODELS = {
    "seedance_1_5_pro": {"name": "Seedance 1.5 Pro", "cost": 8.0, "quality": "high"},
    "seedance_2_0": {"name": "Seedance 2.0", "cost": 10.0, "quality": "very_high"},
    "seedance_2_0_fast": {"name": "Seedance 2.0 Fast", "cost": 6.0, "quality": "high"},
    "kling_2_6": {"name": "Kling 2.6", "cost": 9.0, "quality": "very_high"},
    "grok_imagine": {"name": "Grok Imagine", "cost": 7.0, "quality": "high"},
    "runway": {"name": "Runway", "cost": 8.5, "quality": "very_high"},
    "gemini_omni_flash": {"name": "Gemini Omni Flash", "cost": 5.0, "quality": "medium_high"},
    "veo_3_1": {"name": "Veo 3.1", "cost": 12.0, "quality": "excellent"},
    "veo_3_1_fast": {"name": "Veo 3.1 Fast", "cost": 9.0, "quality": "very_high"},
    "veo_3_1_lite": {"name": "Veo 3.1 Lite", "cost": 4.5, "quality": "medium_high"},
}

# Video Formats with guidelines
VIDEO_FORMATS = {
    "shoppable_video": {
        "name": "Shoppable Video",
        "description": "Interactive product showcase with embedded shopping links",
        "recommended_models": ["seedance_2_0", "veo_3_1"],
        "prompt_style": "product_focused",
        "script_style": "persuasive_cta",
    },
    "viral_hook": {
        "name": "Viral Hook",
        "description": "Short, attention-grabbing opening sequence",
        "recommended_models": ["seedance_2_0_fast", "veo_3_1_fast"],
        "prompt_style": "emotional_impact",
        "script_style": "punchy_short",
    },
    "trending": {
        "name": "Trending",
        "description": "Current trend-based content with high engagement potential",
        "recommended_models": ["seedance_2_0", "kling_2_6"],
        "prompt_style": "trend_aware",
        "script_style": "conversational_trend",
    },
    "meme": {
        "name": "Meme",
        "description": "Humorous content with meme-style elements",
        "recommended_models": ["seedance_1_5_pro", "grok_imagine"],
        "prompt_style": "comedic",
        "script_style": "comedic_caption",
    },
    "pov_roleplay": {
        "name": "POV & Roleplay",
        "description": "First-person perspective or character roleplay scenarios",
        "recommended_models": ["veo_3_1", "seedance_2_0"],
        "prompt_style": "immersive_pov",
        "script_style": "dialogue_driven",
    },
    "reaction": {
        "name": "Reaction",
        "description": "Response or reaction to content or events",
        "recommended_models": ["seedance_2_0_fast", "kling_2_6"],
        "prompt_style": "response_focused",
        "script_style": "spontaneous_reaction",
    },
    "storytelling": {
        "name": "Storytelling",
        "description": "Narrative-driven content with plot and character development",
        "recommended_models": ["veo_3_1", "seedance_2_0"],
        "prompt_style": "narrative_rich",
        "script_style": "story_arc",
    },
}

# Pydantic models for input validation
class PromptInput(BaseModel):
    topic: str = Field(..., description="Main topic or subject for the video")
    format: Literal[
        "shoppable_video",
        "viral_hook",
        "trending",
        "meme",
        "pov_roleplay",
        "reaction",
        "storytelling",
    ] = Field(..., description="Type of video to generate")
    duration: int = Field(
        default=30, description="Video duration in seconds (15-120)", ge=15, le=120
    )
    style: str = Field(default="", description="Optional style or mood")
    tone: str = Field(default="", description="Optional tone or voice style")

class VideoSubmissionInput(BaseModel):
    prompt: str = Field(..., description="The video prompt text")
    script: str = Field(..., description="Narrative script for the video")
    format: str = Field(..., description="Video format type")
    model: str = Field(..., description="AI model to use for generation")

class TaskStatusInput(BaseModel):
    task_id: str = Field(..., description="ID of the task to check")

# Helper functions
def select_model_for_format(format_key: str) -> str:
    """Select best model based on format"""
    if format_key in VIDEO_FORMATS:
        return VIDEO_FORMATS[format_key]["recommended_models"][0]
    return "seedance_2_0"

def validate_character_limit(text: str, limit: int = 2000) -> tuple[bool, str]:
    """Validate text character limit"""
    if len(text) > limit:
        return False, f"Text exceeds {limit} character limit ({len(text)} characters)"
    return True, ""

async def call_viewmax_api(endpoint: str, payload: dict) -> dict:
    """Call ViewMax API with proper error handling"""
    headers = {
        "Authorization": f"Bearer {VIEWMAX_API_KEY}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                f"{VIEWMAX_BASE_URL}/{endpoint}",
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": str(e), "status": "failed"}

# MCP Tools
@mcp.tool
async def viewmax_generate_prompt_and_script(
    input: PromptInput,
    ctx: Context,
) -> dict:
    """
    Generate an AI video prompt and narrative script for ViewMax Studio.
    Automatically selects the best model based on the video format.
    """
    format_key = input.format
    format_info = VIDEO_FORMATS.get(format_key)

    if not format_info:
        return {
            "error": f"Unknown format: {format_key}",
            "available_formats": list(VIDEO_FORMATS.keys()),
        }

    # Select model
    selected_model = select_model_for_format(format_key)
    model_info = AI_MODELS.get(selected_model, {})

    # Build generation payload
    generation_input = {
        "topic": input.topic,
        "format": format_info["name"],
        "prompt_style": format_info["prompt_style"],
        "script_style": format_info["script_style"],
        "duration": input.duration,
        "style": input.style or "default",
        "tone": input.tone or "professional",
    }

    await ctx.report_progress(20, 100, "Generating prompt...")

    # Generate prompt
    prompt_response = await call_viewmax_api("ai/generate", {
        "type": "prompt",
        "input": generation_input,
    })

    if "error" in prompt_response:
        return {
            "error": "Failed to generate prompt",
            "details": prompt_response.get("error"),
        }

    prompt = prompt_response.get("content", "")

    # Validate prompt
    is_valid, error_msg = validate_character_limit(prompt)
    if not is_valid:
        return {"error": f"Generated prompt validation failed: {error_msg}"}

    await ctx.report_progress(50, 100, "Generating script...")

    # Generate script
    script_response = await call_viewmax_api("ai/generate", {
        "type": "script",
        "input": {
            **generation_input,
            "prompt": prompt,
        },
    })

    if "error" in script_response:
        return {
            "error": "Failed to generate script",
            "details": script_response.get("error"),
        }

    script = script_response.get("content", "")

    # Validate script
    is_valid, error_msg = validate_character_limit(script)
    if not is_valid:
        return {"error": f"Generated script validation failed: {error_msg}"}

    await ctx.report_progress(100, 100, "Complete")

    return {
        "success": True,
        "format": format_info["name"],
        "prompt": prompt,
        "script": script,
        "model_selected": model_info.get("name", selected_model),
        "model_cost": model_info.get("cost", 0),
        "prompt_length": len(prompt),
        "script_length": len(script),
        "ready_to_submit": True,
    }

@mcp.tool
async def viewmax_submit_video(
    input: VideoSubmissionInput,
    ctx: Context,
) -> dict:
    """
    Submit a video generation request to ViewMax Studio API.
    Returns a task ID for tracking the video generation progress.
    """
    # Validate inputs
    prompt_valid, prompt_error = validate_character_limit(input.prompt)
    if not prompt_valid:
        return {"error": f"Prompt validation failed: {prompt_error}"}

    script_valid, script_error = validate_character_limit(input.script)
    if not script_valid:
        return {"error": f"Script validation failed: {script_error}"}

    # Verify model exists
    if input.model not in AI_MODELS:
        return {
            "error": f"Unknown model: {input.model}",
            "available_models": list(AI_MODELS.keys()),
        }

    await ctx.report_progress(30, 100, "Submitting to ViewMax API...")

    # Submit to API
    submission_response = await call_viewmax_api("ai/query", {
        "prompt": input.prompt,
        "script": input.script,
        "format": input.format,
        "model": input.model,
        "api_version": "v1",
    })

    if "error" in submission_response:
        return {
            "error": "Failed to submit video",
            "details": submission_response.get("error"),
        }

    task_id = submission_response.get("task_id")

    await ctx.report_progress(100, 100, "Submitted successfully")

    return {
        "success": True,
        "task_id": task_id,
        "status": "submitted",
        "model_used": input.model,
        "format": input.format,
        "message": "Video generation submitted. Use task_id to check status.",
    }

@mcp.tool
async def viewmax_check_task_status(input: TaskStatusInput) -> dict:
    """
    Check the generation status of a submitted video task.
    Returns current progress and status information.
    """
    status_response = await call_viewmax_api("ai/query", {
        "task_id": input.task_id,
        "action": "status",
    })

    if "error" in status_response:
        return {
            "error": "Failed to check task status",
            "task_id": input.task_id,
            "details": status_response.get("error"),
        }

    return {
        "task_id": input.task_id,
        "status": status_response.get("status", "unknown"),
        "progress": status_response.get("progress", 0),
        "estimated_completion": status_response.get("estimated_completion"),
        "video_url": status_response.get("video_url"),
        "error": status_response.get("error"),
    }

# Create ASGI application for HTTP deployment
app = mcp.http_app()

# For local testing with direct HTTP run
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)

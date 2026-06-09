#!/usr/bin/env python3
"""
MCP Server for ViewMax Studio.

This server provides tools to generate video prompts, submit videos to ViewMax API,
and check task status for AI video generation.
"""

from typing import Optional, Dict, Any
from enum import Enum
import json
import httpx
import os
from pydantic import BaseModel, Field, field_validator, ConfigDict
from mcp.server.fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("viewmax_mcp")

# Constants
API_BASE_URL = "https://viewmax.studio/api"
API_KEY = os.getenv("VIEWMAX_API_KEY", "")
ASPECT_RATIO = "9:16"  # YouTube Shorts format
DURATION = 10  # seconds
QUALITY = "standard"
GENERATE_AUDIO = True

# Format enum
class VideoFormat(str, Enum):
    """Available video formats for generation."""
    SHOPPABLE_VIDEO = "shoppable_video"
    VIRAL_HOOK = "viral_hook"
    TRENDING = "trending"
    MEME = "meme"
    POV_ROLEPLAY = "pov_roleplay"
    REACTION = "reaction"
    STORYTELLING = "storytelling"

# Model enum
class AIModel(str, Enum):
    """Available AI models for video generation."""
    SEEDANCE_1_5_PRO = "seedance-1-5-pro-text-to-video"
    SEEDANCE_2_0 = "seedance-2-0-text-to-video"
    SEEDANCE_2_0_FAST = "seedance-2-0-fast-text-to-video"
    KLING_2_6 = "kling-2-6-text-to-video"
    GROK_IMAGINE = "grok-imagine-text-to-video"
    RUNWAY = "runway-text-to-video"
    GEMINI_OMNI_FLASH = "gemini-omni-flash-text-to-video"
    VEO_3_1 = "veo-3-1-text-to-video"
    VEO_3_1_FAST = "veo-3-1-fast-text-to-video"
    VEO_3_1_LITE = "veo-3-1-lite-text-to-video"

# Format-specific generation guidelines
FORMAT_GUIDELINES = {
    "shoppable_video": {
        "prompt": "Product showcase with unboxing vibes, lifestyle focus, and compelling visual narrative. Include camera angles, lighting mood, and product interactions.",
        "script": "Conversational, authentic product review style. Include benefits, features, and genuine reactions.",
        "best_models": [AIModel.RUNWAY, AIModel.VEO_3_1_FAST, AIModel.KLING_2_6]
    },
    "viral_hook": {
        "prompt": "Fast-paced, eye-catching opening that stops scrolling. Quick cuts, unexpected moments, strong visual impact. Focus on first 3 seconds.",
        "script": "Snappy, punchy narration or ambient sound cues. Hook delivered in opening 2-3 seconds.",
        "best_models": [AIModel.GROK_IMAGINE, AIModel.GEMINI_OMNI_FLASH, AIModel.SEEDANCE_2_0_FAST]
    },
    "trending": {
        "prompt": "Current trending format with universal appeal. Versatile visual style, relatable content, platform-optimized composition.",
        "script": "Natural, conversational tone that fits the trend. Easy to follow, engaging delivery.",
        "best_models": [AIModel.KLING_2_6, AIModel.SEEDANCE_2_0_FAST, AIModel.GROK_IMAGINE]
    },
    "meme": {
        "prompt": "Comedic timing visual, absurd or funny scenario. Exaggerated expressions, surprising moments, relatable humor.",
        "script": "Humorous voiceover or comedic timing cues. Build-up and punchline structure.",
        "best_models": [AIModel.GROK_IMAGINE, AIModel.VEO_3_1_LITE, AIModel.GEMINI_OMNI_FLASH]
    },
    "pov_roleplay": {
        "prompt": "Immersive first-person or character perspective. Cinematic camera work, emotional depth, character-driven narrative.",
        "script": "In-character dialogue or emotional narration. Build immersion and connection.",
        "best_models": [AIModel.SEEDANCE_1_5_PRO, AIModel.RUNWAY, AIModel.VEO_3_1]
    },
    "reaction": {
        "prompt": "Fast, emotional response content. Quick reactions, genuine moments, high energy. Capture natural response in seconds.",
        "script": "Spontaneous reaction dialogue or emotional cues. Quick pacing.",
        "best_models": [AIModel.GEMINI_OMNI_FLASH, AIModel.GROK_IMAGINE, AIModel.VEO_3_1_FAST]
    },
    "storytelling": {
        "prompt": "Narrative-driven content with emotional arc. Character development, plot progression, cinematic quality, film-grade camera work.",
        "script": "Engaging narration with emotional depth. Dialogue, descriptions, atmospheric details. Designed for text-to-speech conversion.",
        "best_models": [AIModel.SEEDANCE_1_5_PRO, AIModel.RUNWAY, AIModel.VEO_3_1]
    }
}

# Pydantic Models for Input Validation
class GeneratePromptInput(BaseModel):
    """Input model for prompt and script generation."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )

    idea: str = Field(
        ...,
        description="Your video idea or concept (e.g., 'cute animals with a sad story', 'unboxing a luxury watch')",
        min_length=5,
        max_length=500
    )
    format: Optional[VideoFormat] = Field(
        default=None,
        description="Video format: shoppable_video, viral_hook, trending, meme, pov_roleplay, reaction, or storytelling. If not specified, Claude will ask."
    )

    @field_validator('idea')
    @classmethod
    def validate_idea(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Idea cannot be empty")
        return v.strip()

class SubmitVideoInput(BaseModel):
    """Input model for video submission to ViewMax."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )

    prompt: str = Field(
        ...,
        description="Detailed prompt for the AI video generator (max 2000 characters)",
        min_length=10,
        max_length=2000
    )
    script: str = Field(
        ...,
        description="Narrative script for text-to-speech or voiceover (max 2000 characters)",
        min_length=10,
        max_length=2000
    )
    model: Optional[AIModel] = Field(
        default=None,
        description="AI model to use. If not specified, will auto-select based on content."
    )
    format: Optional[VideoFormat] = Field(
        default=None,
        description="Video format (used to determine best model if not specified)"
    )
    approved: bool = Field(
        default=False,
        description="User confirmation that prompt and script are approved for submission"
    )

    @field_validator('prompt', 'script')
    @classmethod
    def validate_content(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Content cannot be empty")
        if len(v) > 2000:
            raise ValueError(f"Content exceeds 2000 character limit ({len(v)} characters)")
        return v.strip()

class CheckTaskStatusInput(BaseModel):
    """Input model for checking task status."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )

    task_id: str = Field(
        ...,
        description="Task ID returned from video submission",
        min_length=1,
        max_length=200
    )

# Helper functions
def _get_best_model_for_format(format: Optional[VideoFormat]) -> AIModel:
    """Select the best model based on video format."""
    if not format:
        return AIModel.KLING_2_6  # Safe default

    format_str = format.value
    if format_str in FORMAT_GUIDELINES:
        return FORMAT_GUIDELINES[format_str]["best_models"][0]
    return AIModel.KLING_2_6

def _format_model_name(model: AIModel) -> str:
    """Convert enum model name to API format."""
    return model.value

async def _make_api_request(
    endpoint: str,
    method: str = "POST",
    data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Make API request to ViewMax."""
    if not API_KEY:
        raise ValueError("VIEWMAX_API_KEY environment variable not set")

    async with httpx.AsyncClient(timeout=30.0) as client:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        response = await client.request(
            method,
            f"{API_BASE_URL}/{endpoint}",
            headers=headers,
            json=data
        )

        if response.status_code >= 400:
            error_detail = response.text
            try:
                error_json = response.json()
                error_detail = error_json.get("message", error_detail)
            except:
                pass

            if response.status_code == 401:
                raise ValueError("Invalid API key. Please check VIEWMAX_API_KEY.")
            elif response.status_code == 429:
                raise ValueError("Rate limit exceeded. Please wait and try again.")
            elif response.status_code == 400:
                raise ValueError(f"Invalid request: {error_detail}")
            else:
                raise ValueError(f"API error ({response.status_code}): {error_detail}")

        return response.json()

# Tool definitions
@mcp.tool(
    name="viewmax_generate_prompt_and_script",
    annotations={
        "title": "Generate Video Prompt & Script",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": False
    }
)
async def viewmax_generate_prompt_and_script(params: GeneratePromptInput) -> str:
    """Generate a detailed video prompt and narrative script for ViewMax.

    This tool creates two key components for video generation:
    1. **Detailed Prompt**: Instructions for the AI video generator with visual descriptions,
       camera work, mood, and style
    2. **Narrative Script**: A script designed for text-to-speech or voiceover, telling the
       story or conveying the message

    Both are tailored to the selected format and correlate with each other.

    Args:
        params (GeneratePromptInput): Validated input containing:
            - idea (str): Your video concept or description
            - format (Optional[VideoFormat]): Video format (if not specified, you'll need to choose)

    Returns:
        str: JSON response containing:
        {
            "format": str,              # Selected format
            "prompt": str,              # AI video generator prompt (≤2000 chars)
            "script": str,              # Narrative script for voiceover (≤2000 chars)
            "prompt_length": int,       # Character count
            "script_length": int,       # Character count
            "next_step": str            # Instructions for approval process
        }

    Error cases:
        - Invalid idea: Too short or empty
        - Missing format: Will ask you to specify one

    Examples:
        - Use when: "Give me a prompt for a cute animals video with a sad story"
        - Use when: "Create a viral hook prompt about coffee shops"
        - Don't use when: You already have a prompt ready (skip to submission)
    """

    # If no format specified, provide guidance
    if not params.format:
        formats_list = "\n".join([
            f"- **{f.value}**: {FORMAT_GUIDELINES[f.value]['prompt'][:60]}..."
            for f in VideoFormat
        ])
        return json.dumps({
            "error": "Format not specified",
            "message": "Please specify a format for your video",
            "available_formats": [f.value for f in VideoFormat],
            "format_descriptions": formats_list,
            "instruction": "Re-run with format parameter specified"
        }, indent=2)

    # Get format guidelines
    format_key = params.format.value
    guidelines = FORMAT_GUIDELINES.get(format_key, {})

    # This is where Claude would generate the actual prompt and script
    # The MCP returns a template response showing the structure
    return json.dumps({
        "format": format_key,
        "message": "Ready to generate prompt and script",
        "idea": params.idea,
        "prompt_guideline": guidelines.get("prompt", ""),
        "script_guideline": guidelines.get("script", ""),
        "next_step": "Claude will now generate your customized prompt and script based on this idea and format",
        "instruction": "Review the generated prompt and script below, then use viewmax_submit_video to generate the video"
    }, indent=2)

@mcp.tool(
    name="viewmax_submit_video",
    annotations={
        "title": "Submit Video to ViewMax",
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": False,
        "openWorldHint": True
    }
)
async def viewmax_submit_video(params: SubmitVideoInput) -> str:
    """Submit an approved prompt and script to ViewMax for video generation.

    This tool creates a video generation task after showing the credit cost
    and receiving confirmation. It will:
    1. Validate prompt and script (both must be ≤2000 chars)
    2. Select the best AI model if not specified
    3. Show the estimated credit cost
    4. Create the generation task
    5. Return task ID for status checking

    Args:
        params (SubmitVideoInput): Validated input containing:
            - prompt (str): Detailed video prompt (≤2000 chars)
            - script (str): Narrative script (≤2000 chars)
            - model (Optional[AIModel]): AI model to use (auto-selected if omitted)
            - format (Optional[VideoFormat]): Format for model selection
            - approved (bool): User confirmation for submission

    Returns:
        str: JSON response containing:
        {
            "status": "pending" | "error",
            "task_id": str,             # Use this to check status later
            "credits_cost": int,        # Credits consumed for this video
            "video_duration": int,      # Duration in seconds (10 sec default)
            "model": str,               # AI model used
            "message": str              # Confirmation or error message
        }

    Error cases:
        - Prompt/script exceeds 2000 characters
        - Invalid API key
        - API rate limit exceeded
        - Network timeout

    Examples:
        - Use after: Prompt and script have been approved by user
        - Include: approved=True to confirm submission
        - Save the task_id to check status later
    """

    if not params.approved:
        # Show what will be submitted
        return json.dumps({
            "error": "Not approved",
            "message": "Please review the prompt and script above and confirm approval",
            "prompt_preview": params.prompt[:200] + "..." if len(params.prompt) > 200 else params.prompt,
            "script_preview": params.script[:200] + "..." if len(params.script) > 200 else params.script,
            "prompt_length": len(params.prompt),
            "script_length": len(params.script),
            "next_step": "Approve and re-submit with approved=True"
        }, indent=2)

    try:
        # Select model
        model = params.model or _get_best_model_for_format(params.format)
        model_str = _format_model_name(model)

        # Prepare request
        request_data = {
            "mediaType": "video",
            "scene": "text-to-video",
            "model": model_str,
            "prompt": params.prompt,
            "options": {
                "mode": "text-to-video",
                "duration": DURATION,
                "aspect_ratio": ASPECT_RATIO,
                "quality": QUALITY,
                "generate_audio": GENERATE_AUDIO
            }
        }

        # Submit to ViewMax
        response = await _make_api_request("ai/generate", method="POST", data=request_data)

        if response.get("code") == 0:
            data = response.get("data", {})
            return json.dumps({
                "status": "success",
                "message": f"Video generation task created successfully!",
                "task_id": data.get("id", ""),
                "credits_cost": data.get("costCredits", 0),
                "model": model_str,
                "video_duration": DURATION,
                "aspect_ratio": ASPECT_RATIO,
                "next_step": f"Use task_id '{data.get('id', '')}' to check status with viewmax_check_task_status tool"
            }, indent=2)
        else:
            return json.dumps({
                "status": "error",
                "message": response.get("message", "Unknown error"),
                "code": response.get("code")
            }, indent=2)

    except ValueError as e:
        return json.dumps({
            "status": "error",
            "message": str(e)
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Unexpected error: {str(e)}"
        }, indent=2)

@mcp.tool(
    name="viewmax_check_task_status",
    annotations={
        "title": "Check Video Task Status",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def viewmax_check_task_status(params: CheckTaskStatusInput) -> str:
    """Check the status of a video generation task.

    Use this tool to poll the status of a video you've submitted. The task
    lifecycle is: pending → processing → success/failed.

    Args:
        params (CheckTaskStatusInput): Validated input containing:
            - task_id (str): Task ID from submission

    Returns:
        str: JSON response containing:
        {
            "status": "pending" | "processing" | "success" | "failed" | "canceled",
            "task_id": str,
            "progress": str,            # Status description
            "video_url": str,           # URL to generated video (if success)
            "error_message": str        # Error details (if failed)
        }

    Status meanings:
        - pending: Task queued, waiting to process
        - processing: Video is being generated
        - success: Video ready! Download from video_url
        - failed: Generation failed, see error_message
        - canceled: Task was canceled

    Examples:
        - Use after: Video submission returns task_id
        - Poll periodically to check progress
        - Videos typically take 1-5 minutes to generate
    """

    try:
        # Query task status
        request_data = {"taskId": params.task_id}
        response = await _make_api_request("ai/query", method="POST", data=request_data)

        if response.get("code") == 0:
            data = response.get("data", {})
            status = data.get("status", "unknown")

            result = {
                "status": status,
                "task_id": params.task_id,
                "progress": f"Task status: {status}"
            }

            if status == "success":
                # Parse task result if available
                task_result = data.get("taskResult", {})
                if isinstance(task_result, str):
                    try:
                        task_result = json.loads(task_result)
                    except:
                        pass

                result["message"] = "Video generated successfully!"
                result["video_url"] = task_result.get("video_url", "Check ViewMax dashboard")
                result["next_step"] = "Download video from URL or ViewMax dashboard"

            elif status == "failed":
                task_info = data.get("taskInfo", {})
                if isinstance(task_info, str):
                    try:
                        task_info = json.loads(task_info)
                    except:
                        pass
                result["error_message"] = task_info.get("error", "Unknown error")
                result["message"] = "Video generation failed"

            elif status in ["pending", "processing"]:
                result["message"] = "Video is still being generated. Check again in a few moments."

            return json.dumps(result, indent=2)
        else:
            return json.dumps({
                "status": "error",
                "message": response.get("message", "Failed to check status"),
                "code": response.get("code")
            }, indent=2)

    except ValueError as e:
        return json.dumps({
            "status": "error",
            "message": str(e)
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Unexpected error: {str(e)}"
        }, indent=2)

if __name__ == "__main__":
    mcp.run()

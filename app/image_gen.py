from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
import os
import base64

router = APIRouter()

STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")
STABILITY_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"

if not STABILITY_API_KEY:
    raise RuntimeError("STABILITY_API_KEY not set in environment")


class ImageGenRequest(BaseModel):
    prompt: str


class ImageGenResponse(BaseModel):
    image_base64: str
    prompt: str


@router.post("/", response_model=ImageGenResponse)
def generate_image(request: ImageGenRequest):
    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Accept": "application/json"
    }

    files = {
        "prompt": (None, request.prompt),
        "output_format": (None, "png"),
    }

    try:
        response = requests.post(
            STABILITY_URL,
            headers=headers,
            files=files,
            timeout=30
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=502,
                detail=f"Stability API error: {response.text}"
            )

        data = response.json()

        if "image" not in data:
            raise HTTPException(
                status_code=502,
                detail=f"Unexpected response format: {data}"
            )

        return ImageGenResponse(
            image_base64=data["image"],
            prompt=request.prompt
        )

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=str(e))

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests

router = APIRouter()

APERTIUM_URL = "https://www.apertium.org/apy/translate"


class TranslateRequest(BaseModel):
    text: str
    source_lang: str
    target_lang: str


class TranslateResponse(BaseModel):
    translated_text: str
    source_lang: str
    target_lang: str


@router.post("/", response_model=TranslateResponse)
def translate_text(request: TranslateRequest):
    params = {
        "q": request.text,
        "langpair": f"{request.source_lang}|{request.target_lang}"
    }

    try:
        response = requests.get(APERTIUM_URL, params=params, timeout=10)

        if response.status_code != 200:
            raise HTTPException(
                status_code=502,
                detail=f"Apertium API error: {response.text}"
            )

        data = response.json()

        if "responseData" not in data:
            raise HTTPException(
                status_code=502,
                detail=f"Unexpected response format: {data}"
            )

        return TranslateResponse(
            translated_text=data["responseData"]["translatedText"],
            source_lang=request.source_lang,
            target_lang=request.target_lang
        )

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=str(e))

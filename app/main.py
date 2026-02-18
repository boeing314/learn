from fastapi import FastAPI
from dotenv import load_dotenv

# Load environment variables (.env)
load_dotenv()

from app.translation import router as translation_router
from app.image_gen import router as image_gen_router

app = FastAPI(
    title="Collaborative AI Microservice",
    version="1.0.0"
)

# Health check (useful for testing & grading)
@app.get("/")
def health_check():
    return {"status": "running"}

# Translation (Apertium)
app.include_router(
    translation_router,
    prefix="/api/v1/translate",
    tags=["Translation"]
)

# Image Generation
app.include_router(
    image_gen_router,
    prefix="/api/v1/image",
    tags=["Image Generation"]
)

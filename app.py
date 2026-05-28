import os
import base64
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
from dotenv import load_dotenv

from models import AnalyzeRequest, AnalysisResult
from analyzer import PsychGuardAnalyzer
from taxonomy import DEMO_EXAMPLES

load_dotenv()

app = FastAPI(title="PsychGuard API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

analyzer = PsychGuardAnalyzer()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}


@app.get("/")
async def serve_frontend():
    return FileResponse(os.path.join(frontend_dir, "index.html"))


@app.post("/api/analyze", response_model=AnalysisResult)
async def analyze(request: AnalyzeRequest):
    try:
        result = analyzer.analyze(request.message, request.channel, request.language)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка анализа: {str(e)}")


@app.post("/api/extract-text")
async def extract_text(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="Поддерживаются только изображения: JPG, PNG, WEBP")

    image_data = await file.read()
    if len(image_data) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Файл слишком большой. Максимум 10 МБ.")

    b64 = base64.b64encode(image_data).decode("utf-8")
    media_type = file.content_type

    try:
        response = groq_client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{media_type};base64,{b64}"},
                    },
                    {
                        "type": "text",
                        "text": (
                            "Extract all text visible in this image exactly as it appears. "
                            "Return only the extracted text with no additional commentary or formatting. "
                            "If the image contains a chat message, SMS, or email, extract the message content."
                        ),
                    },
                ],
            }],
            max_tokens=1000,
        )
        extracted = response.choices[0].message.content.strip()
        return {"text": extracted}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Не удалось извлечь текст: {str(e)}")


@app.get("/api/examples")
async def get_examples():
    return DEMO_EXAMPLES


@app.get("/api/health")
async def health():
    return {"status": "ok"}

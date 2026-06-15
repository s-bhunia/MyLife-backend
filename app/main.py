# main.py
import os
import httpx
from datetime import datetime
import asyncio
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from .intents import INTENT_REPLIES
from .schemas import IntentRequest, FeedbackRequest
from . import database 
from .gemini_service import get_gemini_intent  # <-- Import the new Gemini handler

load_dotenv()

Token = os.getenv("TELEGRAM_BOT_TOKEN")
ChatId = os.getenv("TELEGRAM_CHAT_ID")

@asynccontextmanager
async def lifespan(app: FastAPI):
    database.init_db()
    yield

app = FastAPI(title="mylife backend", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/intent")
async def match_intent(req: IntentRequest):
    gemini_response = None
    try:
        gemini_response = await asyncio.wait_for(get_gemini_intent(req.text), timeout=5.0)
    except asyncio.TimeoutError:
        print("Gemini intent matching timed out after 5 seconds.")
    
    if gemini_response and "action" in gemini_response and "reply" in gemini_response:
        return gemini_response
        
    print("Falling back to local Python intent matcher...")
    action = database.match_intent_pure_python(req.text)
    
    if action == "UNKNOWN":
        return {
            "action": "UNKNOWN",
            "reply": "I'm not completely sure what you mean, but feel free to explore the space!"
        }
        
    return {
        "action": action,
        "reply": INTENT_REPLIES.get(action, "Navigating...")
    }


@app.post("/api/feedback/text")
async def text_feedback(req: FeedbackRequest):
    """Sends text feedback straight to Telegram."""
    if not Token or not ChatId:
        return {"status": "error", "detail": "Telegram credentials not configured"}
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"📩 *MyLife Feedback*\n👤 {req.name}\n📧 {req.email or 'N/A'}\n📝 {req.message}\n🕐 {timestamp}"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://api.telegram.org/bot{Token}/sendMessage",
                json={"chat_id": ChatId, "text": msg, "parse_mode": "Markdown"},
                timeout=10.0
            )
            response.raise_for_status()
            return {"status": "success", "detail": "Message sent."}
    except httpx.HTTPError as e:
        return {"status": "error", "detail": f"Telegram API error: {str(e)}"}


@app.post("/api/feedback/voice")
async def voice_feedback(
    file: UploadFile = File(...), 
    name: str = Form("Anonymous"),
    email: Optional[str] = Form(None)
):
    """Forwards pre-encoded audio from the client natively to Telegram."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    caption = f"🎙️ Audio from {name} \n({email or 'No email'})\n🕐 {timestamp}"
    
    filename = file.filename or "audio_message.webm"
    mime_type = file.content_type or "audio/webm"
    
    async with httpx.AsyncClient() as client:
        await client.post(
            f"https://api.telegram.org/bot{Token}/sendAudio",
            data={"chat_id": ChatId, "caption": caption},
            files={"audio": (filename, await file.read(), mime_type)}
        )
        
    return {"status": "success", "detail": "Audio sent."}
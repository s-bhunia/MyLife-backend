# main.py
import os
import httpx
from datetime import datetime
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
 

from .intents import INTENT_REPLIES
from .schemas import IntentRequest, FeedbackRequest
from . import database 

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
    """Matches user text to navigation actions or chat conversations using semantic vector search."""
    results = database.collection.query(query_texts=[req.text], n_results=1)
    
    if not results["distances"][0] or results["distances"][0][0] > 1.2:
        return {
            "action": "UNKNOWN", 
            "reply": "I'm not completely sure what you mean. Try asking to see my projects, skills, or bookshelf!"
        }
    
    action = results["metadatas"][0][0]["action"]
    reply_text = INTENT_REPLIES.get(action, "Got it.")
    
    return {"action": action, "reply": reply_text}


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
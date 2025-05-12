import logging
from typing import List

from backend.api.models import get_models

from openai import OpenAI
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.llm.generate import generate as generate_llm
from backend.ngram.generate import generate as generate_ngram

app = FastAPI(debug=True)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ChatRequest(BaseModel):
    model: str
    messages: List[dict]

class ChatResponse(BaseModel):
    reply: str


models_db = [
    {"id": "gpt-4o", "name": "OpenAI 4o", "base_url": "https://api.openai.com/v1/"},
    {"id": "llama3.2:1b", "name": "Lokales LLM (llama3.2:1b)", "base_url": "http://127.0.0.1:4444/v1"},
    {"id": "local-n-gram", "name": "Lokales N-Gram-Modell", "base_url": ""},
]


@app.get("/models", response_model=List[dict])
async def get_models():
    return models_db

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat: ChatRequest):
    if chat.model not in [model["id"] for model in models_db]:
        raise HTTPException(status_code=400, detail="Invalid model selected.")
    
    if chat.model == "gpt-4o":
        reply = generate_llm(chat.messages, base_url="https://api.openai.com/v1/", model=chat.model)
    if chat.model == "llama3.2:1b":
        reply = generate_llm(chat.messages, base_url="http://127.0.0.1:4444/v1", model=chat.model)
    if chat.model == "local-n-gram":
        text = chat.messages[-1]["content"]
        reply = generate_ngram(text)

    return ChatResponse(reply=reply)

def run():
    uvicorn.run(app, host="0.0.0.0", port=8000)
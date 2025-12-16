from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

SYSTEM_PROMPT = """
You are an AI Literacy and Future Skills Assistant.

Respond ONLY with bullet points.

Rules:
- No introductory sentence
- No headings
- No bold text
- No markdown
- No repeated items
- Maximum of 5 bullet points
- Each bullet point must be one sentence
- Focus on job categories, not specific job titles

If you cannot follow these rules, simplify your answer.
"""


def clean_bullets(text: str) -> list[str]:
    # Remove markdown bold and trim
    text = text.replace("**", "").strip()

    # Split on newlines first; if it’s all one line, also split on commas
    parts = []
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        # If the model returned comma-separated items, split them
        if "," in line:
            parts.extend([p.strip() for p in line.split(",")])
        else:
            parts.append(line)

    bullets = []
    for p in parts:
        # Remove leading bullet markers like "*", "-", "•"
        p = p.lstrip("*-• ").strip()

        # Skip intros and junk
        if not p:
            continue
        if p.lower().startswith(("sure", "here are", "these are")):
            continue

        bullets.append(p)

    # Deduplicate, preserve order, cap at 5
    unique = list(dict.fromkeys(bullets))
    return unique[:5]
    
def is_allowed_topic(user_message: str) -> bool:
    disallowed_keywords = [
        "medical", "diagnosis", "treatment",
        "legal", "lawsuit", "contract","prescription",
        "financial advice", "investment", "stock",
        "politics", "election", "vote",
        "violence", "weapon", "hate"
    ]

    message_lower = user_message.lower()

    for keyword in disallowed_keywords:
        if keyword in message_lower:
            return False

    return True

@app.post("/chat")
def chat(request: ChatRequest):
    
    if not is_allowed_topic(request.message):
        return {
            "reply": [
                "This topic is outside the scope of this chatbot.",
                "The assistant is designed to discuss jobs, skills, and education related to AI.",
                "Please rephrase your question within that scope."
            ]
        }

    ollama_payload = {
        "model": "gemma:2b",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": request.message}
        ],
        "stream": False
    }

    response = requests.post(
        "http://localhost:11434/api/chat",
        json=ollama_payload,
        timeout=60
    )

    ollama_response = response.json()
    print("OLLAMA RESPONSE:", ollama_response)

    raw_reply = ""

    if "message" in ollama_response and "content" in ollama_response["message"]:
        raw_reply = ollama_response["message"]["content"]
    elif "response" in ollama_response:
        raw_reply = ollama_response["response"]
    elif "error" in ollama_response:
        return {"reply": [f"Ollama error: {ollama_response['error']}"]}
    else:
        raw_reply = str(ollama_response)

    cleaned_bullets = clean_bullets(raw_reply)

    return {"reply": cleaned_bullets}

@app.get("/")#If a GET request comes in to /, call health_check().
def health_check():
    return {"status": "Server is running"}

@app.get("/ui")
def serve_ui():
    return FileResponse("static/index.html")

#Opening a URL in a browser automatically sends a GET request to the server.” http://127.0.0.1:8000/ for get and http://127.0.0.1:8000/docs for post http://127.0.0.1:8000/ui
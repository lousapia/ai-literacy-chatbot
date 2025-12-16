# AI Literacy Chatbot

This project is a small, end-to-end AI application that demonstrates how
open-source large language models can be used responsibly to explain how AI
is changing jobs, skills, and education.

The application is intentionally scoped and designed for teaching and
applied learning.

---

## Architecture Overview

Browser UI (HTML / JavaScript)  
→ FastAPI Backend  
→ Ollama (Local LLM Runtime)  
→ Open-Source Model (Gemma)

The UI never talks directly to the model.
All validation, guardrails, and prompt control happen in the API layer.

---

## Tech Stack

- Python 3.10+
- FastAPI
- Ollama
- Open-source LLM (Gemma)
- HTML / JavaScript

---

## Prerequisites

- Python installed
- Ollama installed and running
- A local model pulled (e.g. `gemma:2b`)

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-literacy-chatbot.git
cd ai-literacy-chatbot
2. Create and activate a virtual environment
bash
Copy code
python -m venv venv
venv\Scripts\activate
3. Install dependencies
bash
Copy code
pip install fastapi uvicorn requests
4. Pull the model using Ollama
bash
Copy code
ollama pull gemma:2b
5. Run the application
bash
Copy code
uvicorn main:app --reload
6. Open the UI in a browser
arduino
Copy code
http://127.0.0.1:8000/ui
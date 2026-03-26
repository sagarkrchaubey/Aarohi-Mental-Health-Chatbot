# Aarohi - AI Mental Health Support System

Aarohi is a production-oriented mental health support chatbot built with FastAPI, Streamlit, and the Google Gemini API. It is intentionally scoped as an emotionally supportive companion rather than a general-purpose assistant.

## Features

- Evidence-informed emotional support grounded in WHO, NIMH, NHS, and SAMHSA guidance
- Aarohi first tries to understand the user's likely struggle before offering coping options
- Faster backend flow with model discovery caching, shorter context windows, and tuned output length
- Stable Gemini 2.5 model catalog with per-reply model switching in the UI
- Multiple visual themes including Forest, Lake, Waterfall, Volcano, Dragon, and Lotus
- Mandatory crisis override for self-harm related phrases
- Persistent chat history in JSON storage
- Session memory in the frontend
- Modular backend architecture

## Project Structure

```text
backend/
  __init__.py
  config.py
  gemini_service.py
  guidance_library.py
  history_store.py
  main.py
  model_manager.py
  safety.py
  schemas.py
frontend/
  app.py
data/
  chat_history.json
requirements.txt
.env.example
README.md
```

## Setup

```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_API_URL=https://generativelanguage.googleapis.com/v1beta/models
REQUEST_TIMEOUT_SECONDS=18
REQUEST_MAX_RETRIES=1
MODEL_CACHE_TTL_SECONDS=600
HISTORY_WINDOW_SIZE=6
MAX_OUTPUT_TOKENS=260
AAROHI_API_BASE_URL=http://localhost:8000
```

## Run Backend

```bash
uvicorn backend.main:app --reload
```

## Run Frontend

```bash
streamlit run frontend/app.py
```

## API

### `GET /health`

Returns health status.

### `GET /models`

Fetches available Gemini models dynamically from the API and returns approved display metadata for the frontend.

### `POST /chat`

Example request:

```json
{
  "message": "I've been feeling exhausted and anxious lately.",
  "model": "gemini-2.5-flash",
  "session_id": "session-123"
}
```

## Safety

If the message includes any of the following:

- `suicide`
- `kill myself`
- `end my life`

Aarohi bypasses the model call and returns a direct supportive crisis response encouraging immediate human help.

## Model Notes

- Default model: `gemini-2.5-flash`
- Fast UI default: `gemini-2.5-flash-lite`
- Fallback model: `gemini-2.5-flash-lite`
- Recommended stable models in the app: `gemini-2.5-flash-lite`, `gemini-2.5-flash`, `gemini-2.5-pro`
- Legacy `gemini-2.0-*` models may no longer work reliably and are only shown when discovered

## Notes

- History file: `data/chat_history.json`
- Aarohi is intentionally limited to mental health support conversations and redirects unrelated prompts back to emotional context

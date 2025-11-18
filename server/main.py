# main.py (or server.py)

import os

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from phishing_model import predict_email  # uses your saved pipelines

app = FastAPI(title="FastAPI + Scalable Frontend + Phishing API")

# --- Frontend static + SPA shell ---

BASE_DIR = os.path.dirname(__file__)
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")

# Serve static assets (JS/CSS/etc.) under /static
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# --- CORS so Chrome extension can call the API ---

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # you can tighten later if you want
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Models for phishing API ---

class EmailRequest(BaseModel):
    text: str
    # "svm", "logreg", or None (let backend pick default)
    model: str | None = None


# Chrome extension (and web app) can call this
@app.post("/predict-phishing-pipeline")
async def predict_phishing(req: EmailRequest):
    """
    Request body: {"text": "email content", "model": "svm" | "logreg" | null}
    """
    return predict_email(req.text, model=req.model)


# Optional: also expose under /api/... if you want the web app to call it
@app.post("/api/predict-phishing-pipeline")
async def predict_phishing_api(req: EmailRequest):
    return predict_email(req.text, model=req.model)


# --- Sample API routes for your web app ---

@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/user")
def get_user():
    return {"name": "Harshul", "role": "Engineer"}


# --- Serve SPA shell (index.html) ---

@app.get("/")
def serve_index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

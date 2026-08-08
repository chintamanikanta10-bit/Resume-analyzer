"""
main.py

Entry point of the application.
Creates the FastAPI server and registers all routes.
"""

import sys
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from config import ALLOWED_ORIGINS

# Ensure the backend directory is available on the import path when the app
# is started from the project root or via an ASGI server.
BACKEND_DIR = Path(__file__).resolve().parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

# ----------------------------------------------------
# Global Exception Handler
# ----------------------------------------------------

from core.exception_handlers import generic_exception_handler

# ----------------------------------------------------
# Import API Routers
# ----------------------------------------------------

from routes.upload import router as upload_router
from routes.chat import router as chat_router
from routes.resume import router as resume_router
from routes.ats import router as ats_router
from routes.interview import router as interview_router
from routes.career import router as career_router
from routes.auth import router as auth_router

# ----------------------------------------------------
# Create FastAPI Application
# ----------------------------------------------------

app = FastAPI(
    title="AI Career Assistant",
    description="AI-powered Career Assistant with RAG, Resume Analysis, ATS Analysis, Interview Preparation and Career Roadmap",
    version="1.0.0"
)

# ----------------------------------------------------
# Register Global Exception Handler
# ----------------------------------------------------

app.add_exception_handler(
    Exception,
    generic_exception_handler
)

# ----------------------------------------------------
# CORS Configuration
# ----------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Requested-With"],
)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "same-origin")
        response.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        return response


app.add_middleware(SecurityHeadersMiddleware)

# ----------------------------------------------------
# Register Routes
# ----------------------------------------------------

app.include_router(auth_router)
app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(resume_router)
app.include_router(ats_router)
app.include_router(interview_router)
app.include_router(career_router)

# ----------------------------------------------------
# Home Route
# ----------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "AI Career Assistant Backend Running 🚀"
    }


# ----------------------------------------------------
# Health Check
# ----------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "Healthy",
        "server": "Running"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
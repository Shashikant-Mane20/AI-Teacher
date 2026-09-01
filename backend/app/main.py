from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api_auth import router as auth_router
from app.config import settings

app = FastAPI(title=settings.app_name, version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "AI Teacher API"}

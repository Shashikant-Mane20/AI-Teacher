from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import documents, lessons, students, assessments, websocket, interactive, video

app = FastAPI(title="AI Teacher API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents.router, prefix="/api/v1")
app.include_router(lessons.router, prefix="/api/v1")
app.include_router(students.router, prefix="/api/v1")
app.include_router(assessments.router, prefix="/api/v1")
app.include_router(interactive.router, prefix="/api/v1")
app.include_router(video.router, prefix="/api/v1")
app.include_router(websocket.router)


@app.get("/health")
async def health():
    return {"status": "ok"}

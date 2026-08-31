from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.schemas.document import DocumentProcessResponse

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload", response_model=DocumentProcessResponse)
async def upload_document(
    file: UploadFile = File(...),
    title: str = Form(...),
    topic: str | None = Form(default=None),
    language: str = Form(default="en"),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="File is required")

    return {
        "document_id": "doc_001",
        "status": "processed",
        "chunks_count": 120,
        "metadata": {
            "id": "doc_001",
            "title": title,
            "file_name": file.filename,
            "file_type": file.content_type or "unknown",
            "uploaded_by": "student",
            "status": "processed",
        },
    }


@router.get("/{document_id}")
async def get_document(document_id: str):
    return {"document_id": document_id, "status": "processed"}

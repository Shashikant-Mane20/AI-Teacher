from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.schemas.document import DocumentProcessResponse
from app.services.rag_service import RAGService

router = APIRouter(prefix="/documents", tags=["documents"])
rag_service = RAGService()
documents: dict[str, dict] = {}


@router.post("/upload", response_model=DocumentProcessResponse)
async def upload_document(
    file: UploadFile = File(...),
    title: str = Form(...),
    topic: str | None = Form(default=None),
    language: str = Form(default="en"),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="File is required")

    content = await file.read()
    try:
        extracted_text = await rag_service.extract_text(file.filename, content)
        indexed = await rag_service.index_document(extracted_text)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    document_id = f"doc_{len(documents) + 1:03d}"
    document = {
        "document_id": document_id,
        "status": "processed",
        "chunks_count": indexed["chunks_count"],
        "metadata": {
            "id": document_id,
            "title": title,
            "file_name": file.filename,
            "file_type": file.content_type or "unknown",
            "uploaded_by": "student",
            "status": "processed",
        },
    }
    documents[document_id] = {**document, "text": extracted_text, "chunks": indexed["chunks"], "topic": topic, "language": language}
    return document


@router.get("/{document_id}")
async def get_document(document_id: str):
    document = documents.get(document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return {key: value for key, value in document.items() if key not in {"text", "chunks"}}


def get_document_context(document_id: str) -> dict | None:
    return documents.get(document_id)

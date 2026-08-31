from pydantic import BaseModel
from typing import Optional


class DocumentUploadRequest(BaseModel):
    title: str
    topic: Optional[str] = None
    language: str = "en"


class DocumentMetadata(BaseModel):
    id: str
    title: str
    file_name: str
    file_type: str
    uploaded_by: Optional[str]
    status: str = "processed"


class DocumentProcessResponse(BaseModel):
    document_id: str
    status: str
    chunks_count: int
    metadata: DocumentMetadata

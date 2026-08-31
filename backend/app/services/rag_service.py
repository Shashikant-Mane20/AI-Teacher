from typing import List


class RAGService:
    async def index_document(self, text: str):
        chunks = self.chunk_text(text)
        return {"chunks_count": len(chunks)}

    def chunk_text(self, text: str, chunk_size: int = 1000) -> List[str]:
        if not text:
            return []
        return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]

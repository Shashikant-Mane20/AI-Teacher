import json
from typing import Any

import httpx

from app.config import settings


class LLMService:
    async def generate_json(self, system_prompt: str, user_prompt: str) -> dict[str, Any] | None:
        if not settings.enable_llm or not settings.openrouter_api_key:
            return None

        headers = {
            "Authorization": f"Bearer {settings.openrouter_api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": settings.openrouter_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.3,
        }
        try:
            async with httpx.AsyncClient(timeout=45.0) as client:
                response = await client.post(
                    f"{settings.openrouter_base_url.rstrip('/')}/chat/completions",
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
                content = response.json()["choices"][0]["message"]["content"]
                result = json.loads(content)
                return result if isinstance(result, dict) else None
        except (httpx.HTTPError, KeyError, IndexError, TypeError, json.JSONDecodeError):
            return None
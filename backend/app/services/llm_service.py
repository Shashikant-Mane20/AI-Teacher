import asyncio
import json
from typing import Any

import httpx

from app.config import settings


class LLMService:
    async def generate_json(self, system_prompt: str, user_prompt: str) -> dict[str, Any] | None:
        if not settings.enable_llm:
            return None

        providers = {
            "gemini": (settings.gemini_api_key, settings.gemini_model),
            "openai": (settings.openai_api_key, settings.openai_model),
            "grok": (settings.grok_api_key, settings.grok_model),
            "deepseek": (settings.deepseek_api_key, settings.deepseek_model),
        }
        async with httpx.AsyncClient(timeout=45.0) as client:
            for provider in settings.llm_provider_order.split(","):
                provider = provider.strip().lower()
                api_key, model = providers.get(provider, ("", ""))
                if not api_key:
                    continue
                result = await self._request_provider(
                    client, provider, api_key, model, system_prompt, user_prompt
                )
                if result is not None:
                    return result
        return None

    async def _request_provider(
        self,
        client: httpx.AsyncClient,
        provider: str,
        api_key: str,
        model: str,
        system_prompt: str,
        user_prompt: str,
    ) -> dict[str, Any] | None:
        try:
            if provider == "gemini":
                content = await self._request_gemini(api_key, model, system_prompt, user_prompt)
            else:
                base_urls = {
                    "openai": "https://api.openai.com/v1",
                    "grok": "https://api.x.ai/v1",
                    "deepseek": "https://api.deepseek.com",
                }
                response = await client.post(
                    f"{base_urls[provider]}/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}"},
                    json={
                        "model": model,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt},
                        ],
                        "response_format": {"type": "json_object"},
                        "temperature": 0.3,
                    },
                )
                content = response.json()["choices"][0]["message"]["content"]
            response.raise_for_status()
            result = json.loads(content)
            return result if isinstance(result, dict) else None
        except (httpx.HTTPError, KeyError, IndexError, TypeError, json.JSONDecodeError, RuntimeError):
            return None

    async def _request_gemini(
        self, api_key: str, model: str, system_prompt: str, user_prompt: str
    ) -> str:
        try:
            from google import genai
        except ImportError as error:
            raise RuntimeError("Install google-genai to use Gemini") from error

        def create_interaction():
            client = genai.Client(api_key=api_key)
            interaction = client.interactions.create(
                model=model,
                input=f"{system_prompt}\n\n{user_prompt}",
            )
            return interaction.output_text

        return await asyncio.to_thread(create_interaction)

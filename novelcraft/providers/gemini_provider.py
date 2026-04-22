"""Google Gemini Provider (무료 API 지원, 자동 재시도 포함)."""
from __future__ import annotations

import time

from .base import LLMProvider, LLMResponse


class GeminiProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
        try:
            from google import genai
        except ImportError:
            raise ImportError("google-genai 패키지가 필요합니다: pip install google-genai")
        self._client = genai.Client(api_key=api_key)
        self._model = model

    @property
    def name(self) -> str:
        return "gemini"

    @property
    def model_id(self) -> str:
        return self._model

    def generate(
        self,
        system: str,
        user: str,
        *,
        max_tokens: int = 4096,
        cache_system: bool = False,
    ) -> LLMResponse:
        from google.genai import types

        config = types.GenerateContentConfig(
            system_instruction=system,
            max_output_tokens=max_tokens,
            temperature=0.8,
            thinking_config=types.ThinkingConfig(thinking_budget=0),
        )

        max_retries = 3
        for attempt in range(max_retries):
            try:
                resp = self._client.models.generate_content(
                    model=self._model,
                    contents=user,
                    config=config,
                )
                text = resp.text or ""
                usage = resp.usage_metadata
                return LLMResponse(
                    text=text,
                    input_tokens=getattr(usage, "prompt_token_count", 0) if usage else 0,
                    output_tokens=getattr(usage, "candidates_token_count", 0) if usage else 0,
                    model=self._model,
                )
            except Exception as e:
                err = str(e)
                if ("503" in err or "429" in err or "UNAVAILABLE" in err or "RESOURCE_EXHAUSTED" in err) and attempt < max_retries - 1:
                    wait = 30 * (attempt + 1)
                    time.sleep(wait)
                    continue
                raise

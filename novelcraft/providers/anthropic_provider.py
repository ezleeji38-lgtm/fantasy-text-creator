"""Anthropic Claude Provider (프롬프트 캐싱 지원)."""
from __future__ import annotations

from anthropic import Anthropic

from .base import LLMProvider, LLMResponse


class AnthropicProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "claude-opus-4-6"):
        self._client = Anthropic(api_key=api_key)
        self._model = model

    @property
    def name(self) -> str:
        return "anthropic"

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
        if cache_system:
            system_blocks = [
                {"type": "text", "text": "당신은 한국어 판타지 단행본 전문 집필 AI입니다."},
                {"type": "text", "text": system, "cache_control": {"type": "ephemeral"}},
            ]
        else:
            system_blocks = [{"type": "text", "text": system}]

        resp = self._client.messages.create(
            model=self._model,
            max_tokens=max_tokens,
            system=system_blocks,
            messages=[{"role": "user", "content": user}],
        )

        text = "".join(b.text for b in resp.content if b.type == "text")
        return LLMResponse(
            text=text,
            input_tokens=resp.usage.input_tokens,
            output_tokens=resp.usage.output_tokens,
            cache_creation_tokens=getattr(resp.usage, "cache_creation_input_tokens", 0),
            cache_read_tokens=getattr(resp.usage, "cache_read_input_tokens", 0),
            model=self._model,
        )

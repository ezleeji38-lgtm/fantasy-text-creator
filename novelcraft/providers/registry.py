"""Provider 레지스트리. 환경변수 기반 자동 선택."""
from __future__ import annotations

import os

from .base import LLMProvider


def get_provider(
    provider_name: str | None = None,
    model: str | None = None,
) -> LLMProvider:
    """환경변수 또는 인자로 Provider를 생성·반환한다.

    우선순위:
    1. 함수 인자 provider_name
    2. 환경변수 NOVELCRAFT_PROVIDER
    3. 키가 있는 provider 자동 감지 (ANTHROPIC_API_KEY → anthropic, GOOGLE_API_KEY → gemini)
    4. 기본값 anthropic
    """
    name = (provider_name or os.getenv("NOVELCRAFT_PROVIDER", "")).strip().lower()

    if not name:
        if os.getenv("GOOGLE_API_KEY"):
            name = "gemini"
        elif os.getenv("ANTHROPIC_API_KEY"):
            name = "anthropic"
        else:
            name = "anthropic"

    if name == "anthropic":
        from .anthropic_provider import AnthropicProvider
        key = os.getenv("ANTHROPIC_API_KEY")
        if not key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY 환경변수가 없습니다. .env 파일을 확인하세요."
            )
        return AnthropicProvider(
            api_key=key,
            model=model or os.getenv("NOVELCRAFT_MODEL", "claude-opus-4-6"),
        )

    if name == "gemini":
        from .gemini_provider import GeminiProvider
        key = os.getenv("GOOGLE_API_KEY")
        if not key:
            raise RuntimeError(
                "GOOGLE_API_KEY 환경변수가 없습니다.\n"
                "무료 발급: https://aistudio.google.com/apikey"
            )
        return GeminiProvider(
            api_key=key,
            model=model or os.getenv("NOVELCRAFT_MODEL", "gemini-2.5-flash"),
        )

    if name == "ollama":
        from .ollama_provider import OllamaProvider
        return OllamaProvider(
            model=model or os.getenv("NOVELCRAFT_MODEL", "qwen2.5:14b"),
            base_url=os.getenv("OLLAMA_URL", "http://localhost:11434"),
        )

    raise ValueError(
        f"알 수 없는 Provider: '{name}'. 지원: anthropic, gemini, ollama"
    )

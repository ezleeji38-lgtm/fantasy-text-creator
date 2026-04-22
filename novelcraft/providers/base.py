"""Provider 공통 인터페이스."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class LLMResponse:
    text: str
    input_tokens: int
    output_tokens: int
    cache_creation_tokens: int = 0
    cache_read_tokens: int = 0
    model: str = ""

    @property
    def usage_dict(self) -> dict:
        return {
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "cache_creation_input_tokens": self.cache_creation_tokens,
            "cache_read_input_tokens": self.cache_read_tokens,
        }


class LLMProvider(ABC):
    """모든 LLM Provider가 구현해야 하는 인터페이스."""

    @abstractmethod
    def generate(
        self,
        system: str,
        user: str,
        *,
        max_tokens: int = 4096,
        cache_system: bool = False,
    ) -> LLMResponse:
        """시스템 프롬프트 + 유저 메시지로 텍스트를 생성한다.

        Args:
            system: 시스템 프롬프트 (Bible 등)
            user: 유저 메시지 (집필 지시 등)
            max_tokens: 최대 출력 토큰
            cache_system: True이면 system을 프롬프트 캐시에 올린다 (지원 시)
        """

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider 이름 (anthropic, gemini, ollama)."""

    @property
    @abstractmethod
    def model_id(self) -> str:
        """사용 중인 모델 ID."""

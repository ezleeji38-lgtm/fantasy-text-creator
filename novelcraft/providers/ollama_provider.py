"""Ollama 로컬 모델 Provider."""
from __future__ import annotations

import json
import urllib.request

from .base import LLMProvider, LLMResponse

DEFAULT_OLLAMA_URL = "http://localhost:11434"


class OllamaProvider(LLMProvider):
    def __init__(self, model: str = "qwen2.5:14b", base_url: str = DEFAULT_OLLAMA_URL):
        self._model = model
        self._base_url = base_url.rstrip("/")

    @property
    def name(self) -> str:
        return "ollama"

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
        payload = json.dumps({
            "model": self._model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "stream": False,
            "options": {"num_predict": max_tokens, "temperature": 0.8},
        }).encode()

        req = urllib.request.Request(
            f"{self._base_url}/api/chat",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=600) as resp:
            data = json.loads(resp.read())

        text = data.get("message", {}).get("content", "")
        tokens = data.get("eval_count", 0)
        prompt_tokens = data.get("prompt_eval_count", 0)
        return LLMResponse(
            text=text,
            input_tokens=prompt_tokens,
            output_tokens=tokens,
            model=self._model,
        )

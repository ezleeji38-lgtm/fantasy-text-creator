"""프로젝트 설정 로더."""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parent.parent
PROMPTS_DIR = ROOT / "prompts"
PROJECTS_DIR = ROOT / "projects"

DEFAULT_MODEL = os.getenv("NOVELCRAFT_MODEL", "claude-opus-4-6")


@dataclass
class ProjectConfig:
    name: str
    path: Path
    genre: str
    target_length: int
    model: str

    @property
    def bible_dir(self) -> Path:
        return self.path / "bible"

    @property
    def outline_dir(self) -> Path:
        return self.path / "outline"

    @property
    def drafts_dir(self) -> Path:
        return self.path / "drafts"

    @property
    def memory_dir(self) -> Path:
        return self.path / "memory"

    @property
    def chapter_summaries_dir(self) -> Path:
        return self.memory_dir / "chapter_summaries"

    @property
    def behavior_file(self) -> Path:
        return self.path / "behavior.md"


def load_project(name: str) -> ProjectConfig:
    path = PROJECTS_DIR / name
    meta_file = path / "project.json"
    if not meta_file.exists():
        raise FileNotFoundError(
            f"프로젝트 '{name}'을(를) 찾을 수 없습니다. `novelcraft init {name}` 먼저 실행하세요."
        )
    meta = json.loads(meta_file.read_text(encoding="utf-8"))
    return ProjectConfig(
        name=meta["name"],
        path=path,
        genre=meta.get("genre", "판타지"),
        target_length=meta.get("target_length", 100_000),
        model=meta.get("model", DEFAULT_MODEL),
    )


def require_api_key() -> str:
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY 환경변수가 없습니다. .env 파일을 확인하세요."
        )
    return key

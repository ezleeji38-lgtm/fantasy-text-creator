"""Bible + Outline 로더. Claude에게 주입할 단일 컨텍스트 번들 생성."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .config import ProjectConfig


@dataclass
class BibleBundle:
    """Claude 프롬프트에 주입되는 Bible + Outline 컨텍스트."""

    text: str
    token_estimate: int

    def __len__(self) -> int:
        return len(self.text)


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8").strip()


def _section(title: str, body: str) -> str:
    if not body:
        return ""
    return f"\n\n## {title}\n\n{body}"


def load_bible(cfg: ProjectConfig) -> BibleBundle:
    """Bible과 Outline 폴더 전체를 하나의 마크다운 문서로 합친다.

    이 번들은 프롬프트 캐시에 올라가 챕터 집필마다 재사용된다.
    """
    parts: list[str] = [f"# 작품 바이블: {cfg.name}\n\n장르: {cfg.genre}"]

    # 세계관
    parts.append(_section("세계관", _read(cfg.bible_dir / "world.md")))

    # 인물 (여러 파일)
    char_dir = cfg.bible_dir / "characters"
    if char_dir.exists():
        char_texts = []
        for char_file in sorted(char_dir.glob("*.md")):
            body = _read(char_file)
            if body:
                char_texts.append(f"### {char_file.stem}\n\n{body}")
        if char_texts:
            parts.append(_section("등장인물", "\n\n".join(char_texts)))

    # 연표, 용어집, 주제
    parts.append(_section("연표", _read(cfg.bible_dir / "timeline.md")))
    parts.append(_section("용어집", _read(cfg.bible_dir / "glossary.md")))
    parts.append(_section("주제의식", _read(cfg.bible_dir / "themes.md")))

    # 아우트라인
    parts.append(_section("시놉시스", _read(cfg.outline_dir / "synopsis.md")))
    parts.append(_section("3막 구조", _read(cfg.outline_dir / "arcs.md")))
    parts.append(_section("챕터 비트", _read(cfg.outline_dir / "chapters.md")))

    # 작가 문체 가이드
    parts.append(_section("작가 문체 가이드 (behavior)", _read(cfg.behavior_file)))

    text = "".join(p for p in parts if p)
    # 대략 한국어 1토큰 ≈ 1.5자
    token_estimate = int(len(text) / 1.5)
    return BibleBundle(text=text, token_estimate=token_estimate)


def load_chapter_beat(cfg: ProjectConfig, chapter_id: str) -> str:
    """outline/chapters.md에서 특정 챕터의 비트만 추출.

    형식: `## ch01` 헤더로 구분. 헤더가 없으면 전체 outline 반환.
    """
    chapters_md = _read(cfg.outline_dir / "chapters.md")
    if not chapters_md:
        return ""

    marker = f"## {chapter_id}"
    if marker not in chapters_md:
        return chapters_md  # 세분화 전이면 전체 제공

    lines = chapters_md.split("\n")
    collecting = False
    collected: list[str] = []
    for line in lines:
        if line.strip().startswith("## "):
            if collecting:
                break
            if line.strip() == marker:
                collecting = True
                collected.append(line)
                continue
        elif collecting:
            collected.append(line)
    return "\n".join(collected).strip()


def load_previous_summary(cfg: ProjectConfig, chapter_id: str) -> str:
    """직전 챕터의 요약을 불러온다. ch02라면 ch01_summary.md."""
    if not chapter_id.startswith("ch"):
        return ""
    try:
        num = int(chapter_id[2:])
    except ValueError:
        return ""
    if num <= 1:
        return ""
    prev_id = f"ch{num - 1:02d}"
    summary_file = cfg.chapter_summaries_dir / f"{prev_id}_summary.md"
    return _read(summary_file)

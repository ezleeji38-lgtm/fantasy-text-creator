"""챕터 집필 엔진. Claude Opus + 프롬프트 캐싱."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from anthropic import Anthropic

from .bible import BibleBundle, load_bible, load_chapter_beat, load_previous_summary
from .config import PROMPTS_DIR, ProjectConfig, require_api_key

ProgressFn = Callable[[str, str], None]  # (stage, message) 콜백


@dataclass
class WriteResult:
    chapter_id: str
    chapter_text: str
    review: dict
    summary: str
    draft_path: Path
    usage: dict


def _load_prompt(name: str) -> str:
    return (PROMPTS_DIR / name).read_text(encoding="utf-8")


def _fill(template: str, **kwargs: str) -> str:
    out = template
    for key, value in kwargs.items():
        out = out.replace("{" + key + "}", value)
    return out


class ChapterWriter:
    def __init__(self, cfg: ProjectConfig):
        self.cfg = cfg
        self.client = Anthropic(api_key=require_api_key())

    def _build_system(self, bible: BibleBundle) -> list[dict]:
        """시스템 프롬프트. Bible을 캐시 가능한 블록으로 올린다."""
        return [
            {
                "type": "text",
                "text": (
                    "당신은 한국어 판타지 단행본 전문 집필 AI입니다. "
                    "아래 작품 바이블을 절대 기준으로 삼아 작업합니다. "
                    "바이블은 이 세션에서 캐싱되어 반복 참조됩니다."
                ),
            },
            {
                "type": "text",
                "text": bible.text,
                "cache_control": {"type": "ephemeral"},
            },
        ]

    def _call(self, system: list[dict], user_text: str, max_tokens: int) -> tuple[str, dict]:
        resp = self.client.messages.create(
            model=self.cfg.model,
            max_tokens=max_tokens,
            system=system,
            messages=[{"role": "user", "content": user_text}],
        )
        text = "".join(b.text for b in resp.content if b.type == "text")
        usage = {
            "input_tokens": resp.usage.input_tokens,
            "output_tokens": resp.usage.output_tokens,
            "cache_creation_input_tokens": getattr(
                resp.usage, "cache_creation_input_tokens", 0
            ),
            "cache_read_input_tokens": getattr(
                resp.usage, "cache_read_input_tokens", 0
            ),
        }
        return text, usage

    def write_chapter(
        self,
        chapter_id: str,
        progress: ProgressFn | None = None,
    ) -> WriteResult:
        def emit(stage: str, msg: str) -> None:
            if progress is not None:
                try:
                    progress(stage, msg)
                except Exception:
                    pass

        emit("load", "Bible 로드 중…")
        bible = load_bible(self.cfg)
        beat = load_chapter_beat(self.cfg, chapter_id) or "(비트 미지정 — 시놉시스를 참고해 자유 집필)"
        prev = load_previous_summary(self.cfg, chapter_id) or "(첫 챕터이거나 직전 요약 없음)"
        emit("load", f"Bible {len(bible):,}자 로드 완료 (~{bible.token_estimate:,} 토큰)")

        system = self._build_system(bible)

        # 1. 본문 집필
        emit("write", f"Claude {self.cfg.model} 호출 — 본문 집필 시작")
        write_prompt = _fill(
            _load_prompt("write_chapter.md"),
            chapter_id=chapter_id,
            chapter_beat=beat,
            previous_summary=prev,
        )
        chapter_text, usage_write = self._call(system, write_prompt, max_tokens=16000)
        emit("write", f"본문 {len(chapter_text):,}자 생성 완료")

        # 초고 저장
        self.cfg.drafts_dir.mkdir(parents=True, exist_ok=True)
        draft_path = self.cfg.drafts_dir / f"{chapter_id}_draft.md"
        draft_path.write_text(chapter_text, encoding="utf-8")
        emit("save", f"초고 저장: {draft_path.name}")

        # 2. 자가리뷰
        emit("review", "자가리뷰 시작…")
        review_prompt = _fill(
            _load_prompt("self_review.md"),
            chapter_text=chapter_text,
        )
        review_raw, usage_review = self._call(system, review_prompt, max_tokens=2000)
        review = _parse_json(review_raw)

        review_path = self.cfg.drafts_dir / f"{chapter_id}_review.json"
        review_path.write_text(
            json.dumps(review, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        issue_count = len(review.get("issues", []))
        passed = review.get("pass")
        emit("review", f"리뷰 완료 — 이슈 {issue_count}건, 통과={passed}")

        # 3. 요약 생성 (다음 챕터 연속성용)
        emit("summary", "연속성 요약 생성 중…")
        summary_prompt = _fill(
            _load_prompt("summarize_chapter.md"),
            chapter_text=chapter_text,
        )
        summary, usage_sum = self._call(system, summary_prompt, max_tokens=2000)

        self.cfg.chapter_summaries_dir.mkdir(parents=True, exist_ok=True)
        summary_path = self.cfg.chapter_summaries_dir / f"{chapter_id}_summary.md"
        summary_path.write_text(summary, encoding="utf-8")
        emit("summary", f"요약 저장: {summary_path.name}")

        total_usage = _merge_usage([usage_write, usage_review, usage_sum])
        emit(
            "done",
            f"완료 — 입력 {total_usage['input_tokens']:,} · 출력 {total_usage['output_tokens']:,} · "
            f"캐시읽기 {total_usage['cache_read_input_tokens']:,}",
        )

        return WriteResult(
            chapter_id=chapter_id,
            chapter_text=chapter_text,
            review=review,
            summary=summary,
            draft_path=draft_path,
            usage=total_usage,
        )


def _parse_json(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        text = "\n".join(lines[1:-1]) if lines[-1].startswith("```") else "\n".join(lines[1:])
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"parse_error": True, "raw": text}


def _merge_usage(items: list[dict]) -> dict:
    keys = ["input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"]
    return {k: sum(i.get(k, 0) for i in items) for k in keys}

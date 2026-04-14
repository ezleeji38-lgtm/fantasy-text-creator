"""집필 잡(Job) 관리자.

대시보드에서 챕터 집필을 트리거하면 백그라운드 스레드에서 실행하고,
진행 로그를 이벤트 큐에 쌓아 SSE로 스트리밍한다.
"""
from __future__ import annotations

import queue
import threading
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Iterator

from .config import load_project
from .writer import ChapterWriter

_JOB_SENTINEL = "__END__"


@dataclass
class JobEvent:
    ts: float
    stage: str
    message: str

    def to_dict(self) -> dict:
        return {
            "ts": self.ts,
            "iso": datetime.fromtimestamp(self.ts).isoformat(timespec="seconds"),
            "stage": self.stage,
            "message": self.message,
        }


@dataclass
class Job:
    id: str
    project: str
    chapter_id: str
    status: str = "pending"  # pending | running | completed | failed
    created_at: float = field(default_factory=time.time)
    finished_at: float | None = None
    error: str | None = None
    result: dict | None = None  # WriteResult 요약 (본문 제외)
    _events: list[JobEvent] = field(default_factory=list)
    _queue: queue.Queue = field(default_factory=queue.Queue)
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def emit(self, stage: str, message: str) -> None:
        ev = JobEvent(ts=time.time(), stage=stage, message=message)
        with self._lock:
            self._events.append(ev)
        self._queue.put(ev)

    def close(self) -> None:
        self._queue.put(_JOB_SENTINEL)

    def snapshot(self) -> dict:
        with self._lock:
            events = [e.to_dict() for e in self._events]
        return {
            "id": self.id,
            "project": self.project,
            "chapter_id": self.chapter_id,
            "status": self.status,
            "created_at": self.created_at,
            "finished_at": self.finished_at,
            "error": self.error,
            "result": self.result,
            "events": events,
        }

    def stream(self) -> Iterator[JobEvent | None]:
        """이미 쌓인 이벤트 먼저 yield, 이후 실시간으로 대기하며 yield.

        None이 yield되면 heartbeat(keepalive). 종료 시 StopIteration.
        """
        # 1. 기존 이벤트 먼저
        with self._lock:
            backlog = list(self._events)
        backlog_count = len(backlog)
        for ev in backlog:
            yield ev

        # 2. 종료 상태면 큐를 조용히 비우고 종료 (backlog 중복 방지)
        if self.status in ("completed", "failed"):
            try:
                while True:
                    self._queue.get_nowait()
            except queue.Empty:
                pass
            return

        # 3. 실시간 대기 — 이미 backlog로 내보낸 만큼 큐를 건너뛴다
        skipped = 0
        while True:
            try:
                item = self._queue.get(timeout=15.0)
            except queue.Empty:
                yield None  # keepalive
                if self.status in ("completed", "failed"):
                    return
                continue
            if item == _JOB_SENTINEL:
                return
            if skipped < backlog_count:
                skipped += 1
                continue
            yield item


class JobManager:
    def __init__(self) -> None:
        self._jobs: dict[str, Job] = {}
        self._lock = threading.Lock()

    def start_write(self, project_name: str, chapter_id: str) -> Job:
        job = Job(
            id=uuid.uuid4().hex[:12],
            project=project_name,
            chapter_id=chapter_id,
        )
        with self._lock:
            self._jobs[job.id] = job

        thread = threading.Thread(
            target=self._run_write, args=(job,), daemon=True
        )
        thread.start()
        return job

    def _run_write(self, job: Job) -> None:
        job.status = "running"
        job.emit("start", f"{job.project}/{job.chapter_id} 집필 시작")
        try:
            cfg = load_project(job.project)
            writer = ChapterWriter(cfg)
            result = writer.write_chapter(job.chapter_id, progress=job.emit)
            job.result = {
                "chapter_id": result.chapter_id,
                "length_chars": len(result.chapter_text),
                "draft_path": str(result.draft_path),
                "review_pass": result.review.get("pass"),
                "review_issues": len(result.review.get("issues", [])),
                "usage": result.usage,
            }
            job.status = "completed"
            job.emit("done", "집필 완료")
        except Exception as e:
            job.status = "failed"
            job.error = f"{type(e).__name__}: {e}"
            job.emit("error", job.error)
        finally:
            job.finished_at = time.time()
            job.close()

    def get(self, job_id: str) -> Job | None:
        with self._lock:
            return self._jobs.get(job_id)

    def list_recent(self, limit: int = 20) -> list[dict]:
        with self._lock:
            jobs = sorted(self._jobs.values(), key=lambda j: j.created_at, reverse=True)
        return [j.snapshot() for j in jobs[:limit]]


# 전역 싱글턴 (FastAPI 앱에서 공유)
manager = JobManager()

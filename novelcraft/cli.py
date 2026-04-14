"""novelcraft CLI."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .config import DEFAULT_MODEL, PROJECTS_DIR, load_project
from .bible import load_bible
from .writer import ChapterWriter

console = Console()
TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"


@click.group()
def cli():
    """이지연 판타지 소설 자동 집필 시스템."""


@cli.command()
@click.argument("name")
@click.option("--genre", default="정통 판타지", help="작품 장르")
@click.option("--target-length", default=100_000, type=int, help="목표 분량(글자)")
@click.option("--model", default=DEFAULT_MODEL, help="사용할 Claude 모델")
def init(name: str, genre: str, target_length: int, model: str):
    """새 작품 프로젝트를 생성한다."""
    project_dir = PROJECTS_DIR / name
    if project_dir.exists():
        console.print(f"[red]이미 존재하는 프로젝트: {name}[/red]")
        raise click.Abort()

    # 디렉토리 생성
    for sub in ["bible/characters", "outline", "drafts", "revisions", "final",
                "memory/chapter_summaries", "export"]:
        (project_dir / sub).mkdir(parents=True, exist_ok=True)

    # 템플릿 복사
    shutil.copy(TEMPLATES_DIR / "behavior.md", project_dir / "behavior.md")
    for f in (TEMPLATES_DIR / "bible").glob("*.md"):
        shutil.copy(f, project_dir / "bible" / f.name)
    shutil.copy(
        TEMPLATES_DIR / "bible" / "characters" / "주인공.md",
        project_dir / "bible" / "characters" / "주인공.md",
    )
    for f in (TEMPLATES_DIR / "outline").glob("*.md"):
        shutil.copy(f, project_dir / "outline" / f.name)

    # project.json
    meta = {
        "name": name,
        "genre": genre,
        "target_length": target_length,
        "model": model,
    }
    (project_dir / "project.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    console.print(Panel.fit(
        f"[green]✓[/green] 프로젝트 생성 완료: [bold]{name}[/bold]\n\n"
        f"장르: {genre}\n"
        f"목표 분량: {target_length:,}자\n"
        f"모델: {model}\n\n"
        f"경로: {project_dir}\n\n"
        f"[yellow]다음 단계:[/yellow]\n"
        f"1. bible/ 폴더의 파일을 작성하세요 (세계관·인물·연표·용어집·주제)\n"
        f"2. outline/ 폴더의 시놉시스·아크·챕터비트를 작성하세요\n"
        f"3. [bold]novelcraft write ch01 --project {name}[/bold] 로 첫 챕터 집필",
        title="초기화 성공",
    ))


@cli.command()
@click.argument("chapter_id")
@click.option("--project", "-p", required=True, help="작품명")
def write(chapter_id: str, project: str):
    """지정 챕터를 집필한다. (예: novelcraft write ch01 -p 작품명)"""
    cfg = load_project(project)
    bible = load_bible(cfg)

    console.print(Panel.fit(
        f"프로젝트: [bold]{cfg.name}[/bold]\n"
        f"챕터: [bold]{chapter_id}[/bold]\n"
        f"모델: {cfg.model}\n"
        f"Bible 크기: {len(bible):,}자 (~{bible.token_estimate:,} 토큰)",
        title="집필 시작",
    ))

    if len(bible) < 500:
        console.print("[yellow]⚠ Bible이 거의 비어있습니다. 먼저 bible/ 파일을 작성하세요.[/yellow]")
        raise click.Abort()

    writer = ChapterWriter(cfg)
    with console.status("[cyan]Claude가 집필 중...[/cyan]"):
        result = writer.write_chapter(chapter_id)

    # 결과 리포트
    length = len(result.chapter_text)
    table = Table(title="집필 결과")
    table.add_column("항목")
    table.add_column("값")
    table.add_row("챕터 ID", result.chapter_id)
    table.add_row("본문 길이", f"{length:,}자")
    table.add_row("초고 경로", str(result.draft_path))
    table.add_row("자가리뷰 통과", "✓" if result.review.get("pass") else "✗")
    table.add_row("이슈 개수", str(len(result.review.get("issues", []))))
    u = result.usage
    table.add_row("입력 토큰", f"{u['input_tokens']:,}")
    table.add_row("캐시 생성", f"{u['cache_creation_input_tokens']:,}")
    table.add_row("캐시 읽기", f"{u['cache_read_input_tokens']:,}")
    table.add_row("출력 토큰", f"{u['output_tokens']:,}")
    console.print(table)

    # 이슈 출력
    issues = result.review.get("issues", [])
    if issues:
        console.print("\n[yellow]자가리뷰 이슈:[/yellow]")
        for i, issue in enumerate(issues, 1):
            sev = issue.get("severity", "?")
            cat = issue.get("category", "?")
            desc = issue.get("description", "")
            console.print(f"  {i}. [{sev}] {cat}: {desc}")

    comment = result.review.get("overall_comment")
    if comment:
        console.print(f"\n[cyan]총평:[/cyan] {comment}")


@cli.command()
@click.option("--host", default="127.0.0.1", help="바인딩 호스트")
@click.option("--port", default=8765, type=int, help="포트")
@click.option("--no-open", is_flag=True, help="브라우저 자동 열기 비활성화")
def dashboard(host: str, port: int, no_open: bool):
    """집필 작업 현황 대시보드를 연다."""
    import threading
    import time
    import webbrowser

    from .dashboard import run

    url = f"http://{host}:{port}"
    console.print(Panel.fit(
        f"[bold]novelcraft atelier[/bold]\n\n"
        f"주소  [cyan]{url}[/cyan]\n"
        f"종료  Ctrl+C",
        title="대시보드",
    ))

    if not no_open:
        def _open():
            time.sleep(1.0)
            webbrowser.open(url)
        threading.Thread(target=_open, daemon=True).start()

    run(host=host, port=port)


@cli.command("bible-check")
@click.option("--project", "-p", required=True, help="작품명")
def bible_check(project: str):
    """Bible 로드 상태를 점검한다."""
    cfg = load_project(project)
    bible = load_bible(cfg)
    console.print(f"Bible 크기: [bold]{len(bible):,}자[/bold] (~{bible.token_estimate:,} 토큰)")

    # 필수 파일 체크
    checks = {
        "bible/world.md": cfg.bible_dir / "world.md",
        "bible/characters/": cfg.bible_dir / "characters",
        "bible/timeline.md": cfg.bible_dir / "timeline.md",
        "bible/glossary.md": cfg.bible_dir / "glossary.md",
        "bible/themes.md": cfg.bible_dir / "themes.md",
        "outline/synopsis.md": cfg.outline_dir / "synopsis.md",
        "outline/arcs.md": cfg.outline_dir / "arcs.md",
        "outline/chapters.md": cfg.outline_dir / "chapters.md",
        "behavior.md": cfg.behavior_file,
    }
    table = Table(title="Bible 점검")
    table.add_column("파일")
    table.add_column("상태")
    table.add_column("크기")
    for label, path in checks.items():
        if not path.exists():
            table.add_row(label, "[red]없음[/red]", "-")
        elif path.is_dir():
            count = len(list(path.glob("*.md")))
            table.add_row(label, f"[green]{count}개[/green]", "-")
        else:
            size = len(path.read_text(encoding="utf-8"))
            tag = "[green]✓[/green]" if size > 200 else "[yellow]빈약[/yellow]"
            table.add_row(label, tag, f"{size:,}자")
    console.print(table)


if __name__ == "__main__":
    cli()

# 작업 진행 로그 (PROGRESS)

> 언제든 이 파일을 열면 현재까지 어디까지 왔고, 다음에 뭘 해야 하는지 알 수 있도록 유지한다.

---

## 📍 작업 상태 스냅샷

| 항목 | 값 |
|---|---|
| 마지막 작업일 | 2026-04-15 |
| 현재 버전 | **v0.2 완료 · GitHub push 완료** |
| 다음 단계 | **v0.3 Phase 0 착수 직전** (무료 실행 경로 결정 대기) |
| 저장소 | https://github.com/ezleeji38-lgtm/fantasy-text-creator |
| 최신 커밋 | `0bf3e90 novelcraft v0.2: atelier — 한국어 판타지 단행본 집필 시스템` |

---

## 🏁 지금까지의 여정

### Session 1 (2026-04-14)

**A. 기획 단계**
1. 출간용 한국어 판타지 소설 자동 집필 시스템 설계 결정
2. 작가 주도 철학: 이지연이 Bible(세계관·인물) 직접 작성, AI는 챕터 집필만
3. GitHub 조사: authorclaw + storycraftr + AI_NovelGenerator 조합으로 설계
4. `SYSTEM_DESIGN.md` 작성 완료

**B. v0.1 MVP 구현**
- `novelcraft/` Python 패키지 (CLI + Bible 로더 + Claude 호출)
- 명령어: `init`, `write`, `bible-check`
- 한국어 프롬프트 3종 (집필·자가리뷰·요약)
- Bible/Outline/behavior 한국 판타지 템플릿
- Claude Opus 4.6 (1M context) + 프롬프트 캐싱
- 초기 smoke test: CLI 구조 검증 통과 (실제 API 호출은 미실시)

**C. 시스템 성찰 및 v0.2 기획**
- 치명적 약점 15개 정리 (씬 단위 미지원, 자가리뷰 편향, 일관성 검증 부재 등)
- 대시보드 추가 기획: FastAPI + 쓰기 트리거 + SSE 로그

**D. v0.2 Atelier 구현**
- `novelcraft/dashboard.py` — FastAPI 서버, 9개 신규 엔드포인트
- `novelcraft/jobs.py` — 백그라운드 JobManager + 이벤트 큐
- `novelcraft/writer.py` — 단계별 progress 콜백 추가
- `novelcraft/templates/dashboard.html` — 챕터 드로어 + Bible 모달 + SSE 로그 패널
- 에디토리얼 다크 테마 (Bebas Neue / Fraunces / Noto Serif KR) 유지
- Smoke test 완료: 엔드포인트 9종, 경로 traversal 방어, SSE 중복 버그 발견·수정

**E. GitHub 통합**
- 홈 디렉토리 .git 문제 발견 → `fantasy novel/`에 독립 .git 초기화
- git user 설정 (이지연 / ezleeji38@gmail.com, repo-local)
- 원격 전환: choijinyi/fantasy-text-creator → ezleeji38-lgtm/fantasy-text-creator
- 원격에 19개 `.skill` 파일(Phase 1~6 판타지 집필 스킬) 발견 — 이지연님 저장소에 이미 존재
- README.md 충돌 수동 해결 (novelcraft Part 1 + 스킬 Part 2 통합)
- rebase로 선형 히스토리 유지
- 인증 난관 해결:
  1. osxkeychain helper 대기 문제 발견
  2. `brew install gh` (Homebrew 경유)
  3. 디바이스 플로우 인증 (코드 `14EE-AE0C`)
  4. `gh auth setup-git`으로 credential helper 연결
  5. `git push -u origin main` 성공
- 최종 원격 상태: 45 파일 (스킬 19 + novelcraft 26), 4 커밋

---

## 📦 현재 저장소 구성 (45 파일)

```
fantasy-text-creator/
├── README.md                    # Part 1 novelcraft + Part 2 스킬 통합 가이드
├── SYSTEM_DESIGN.md              # 초기 아키텍처 설계서
├── PROGRESS.md                   # ← 이 파일
├── pyproject.toml                # anthropic, click, rich, dotenv, fastapi, uvicorn
├── .env.example
├── .gitignore
│
├── novelcraft/                   # 코어 패키지
│   ├── cli.py                   # init / write / bible-check / dashboard
│   ├── config.py
│   ├── bible.py                 # Bible+Outline 번들링
│   ├── writer.py                # Claude 호출 + 프롬프트 캐싱 + progress 콜백
│   ├── jobs.py                  # JobManager (백그라운드 스레드 + SSE)
│   ├── dashboard.py             # FastAPI 앱 + 9개 API 엔드포인트
│   └── templates/
│       ├── dashboard.html       # 665줄+ 에디토리얼 다크 UI
│       ├── behavior.md          # 작가 문체 가이드 템플릿
│       ├── bible/world.md · timeline.md · glossary.md · themes.md
│       ├── bible/characters/주인공.md
│       └── outline/synopsis.md · arcs.md · chapters.md
│
├── prompts/                      # 한국어 프롬프트 3종
│   ├── write_chapter.md
│   ├── self_review.md
│   └── summarize_chapter.md
│
└── *.skill (19개)                # Claude Code 판타지 스킬 (ZIP 형식)
    # Phase 1: fantasy-worldbuilder, species-culture-designer, magic-system-architect
    # Phase 2: character-arc-engineer, relationship-web-mapper
    # Phase 3: plot-architecture-engine, conflict-tension-designer, foreshadow-twist-weaver
    # Phase 4: prose-style-engine, dialogue-voice-engine, action-battle-choreographer, scene-chapter-composer
    # Phase 5: consistency-auditor, pacing-rhythm-optimizer, beta-reader-simulator, revision-rewrite-engine
    # Phase 6: series-expansion-planner, fantasy-novel-assembler
    # (추가: writing-workflow)
```

---

## 🎯 v0.3 계획 (확정)

### Phase 0 — Prerequisites
- **0.1** API smoke test (실제 호출 1회) ⏸ **비용 문제로 보류**
- **0.2** 19개 스킬 ZIP 추출 → `extracted_skills/{name}/SKILL.md`
- **0.3** SKILLS_MAP.md 작성 (각 스킬 → novelcraft 기능 매핑)

### Phase 1 — Quality Core
- **1.1** 씬 단위 생성기 (`scene-chapter-composer` 이식)
- **1.2** 문체 엔진 (`prose-style-engine` 이식 + 이지연 실제 문장 샘플)
- **1.3** 대사 엔진 (`dialogue-voice-engine` 이식)

### Phase 2 — Review & Consistency
- **2.1** 베타리더 시뮬레이션 (Sonnet 4.6, `beta-reader-simulator` 이식)
- **2.2** 일관성 감사 (`consistency-auditor` 이식, `novelcraft consistency` CLI)
- **2.3** 교차 검증 파이프라인 (생성→자가리뷰→베타리더→일관성감사)

### Phase 3 — Revision Loop
- **3.1~3.4** 3단계 교정 (structural/scene/line) + `revision-rewrite-engine` 이식 + CLI/대시보드

### Phase 4 — Long-form Sustainability
- **4.1** 누적 상태 문서 (`memory/running_state.md`)
- **4.2** 복선 추적 DB (`memory/foreshadowing.json`, `foreshadow-twist-weaver` 이식)
- **4.3** 캐릭터 아크 추적 (`memory/character_arcs.json`, `character-arc-engineer` 이식)

### Phase 5 — Dashboard Polish
- **5.1** 비용 달러 환산 누적
- **5.2** Draft vs Final diff 뷰
- **5.3** 스킬 카탈로그 페이지 (`/skills`)
- **5.4** 라이브 리뷰 렌더

### 이지연님의 결정 (확정)
| # | 질문 | 답변 |
|---|---|---|
| 1 | API smoke test 진행 | **무료일 때만** |
| 2 | 스킬 이식 범위 | **(a) 최대 이식** |
| 3 | Phase 실행 순서 | **추천대로 (0→1→2→3→4→5)** |
| 4 | 검증 주기 | **테스트 챕터마다** |

---

## ⚠️ 해결 대기 중인 충돌: 비용 vs 검증

결정 1(무료)과 결정 4(매 Phase마다 테스트)가 서로 모순.
Anthropic API는 유료(Opus 4.6 기준 챕터 1개당 약 $0.50~$2).

### 검토한 무료 경로 4가지

| 옵션 | 비용 | 한국어 품질 | 자동화 | 추천 |
|---|---|---|---|---|
| **1. 채팅에서 Claude가 직접 집필** | $0 (구독 내) | ⭐⭐⭐⭐⭐ | ❌ 수동 | 즉시 품질 테스트용 |
| **2. Gemini 2.5 Flash 무료 API** | $0 (일 1500req) | ⭐⭐⭐⭐ | ✅ 완전 자동화 | 개발 내내 기본 |
| **3. 로컬 Ollama (qwen2.5/llama3.3)** | $0 영구 | ⭐⭐⭐ | ✅ 자동화 | 장기·보안 중시 |
| **4. OpenRouter 무료 모델** | $0 (한도) | ⭐⭐⭐ | ✅ 자동화 | 옵션 2 대체 |

### 제 추천 전략 (하이브리드 γ)

```
오늘 (5분)   옵션 1 — 채팅에서 Claude가 ch01 품질 테스트
이번 주      옵션 2 — Gemini Provider 구현 + 통합
v0.3 개발    Gemini로 모든 반복 테스트
최종 출간    Claude Opus 1회 재생성 ($40~80)
```

Phase 0.4 (신규) — **Provider 추상화 레이어**: `writer.py` 리팩터링해서 Anthropic/Gemini/Ollama 전환 가능하게.

---

## ⏸ 재개 시 가장 먼저 할 일

### Step 1 — 이지연님의 결정 확인
**α / β / γ / δ 중 하나:**
- **α** 옵션 1만 (오늘 채팅에서 품질 테스트)
- **β** 옵션 2만 (Gemini 무료 API 자동화)
- **γ** 하이브리드 (옵션 1 + 옵션 2) ⭐ 제 추천
- **δ** 옵션 3 로컬 Ollama (Mac RAM 사양 먼저 확인 필요)

### Step 2 — 결정에 따라 즉시 착수
- **α 선택**: 이지연님이 최소 Bible 5분 작성 → 내가 채팅 안에서 ch01 집필 → `projects/테스트작품/drafts/ch01_draft.md`에 저장 → 품질 평가
- **β 선택**: https://aistudio.google.com/apikey 에서 무료 키 발급 → .env에 저장 → novelcraft에 Gemini provider 추가 (Phase 0.4)
- **γ 선택**: α를 먼저 빠르게 수행해서 품질 감 잡고, 병행으로 β 구현
- **δ 선택**: `brew install ollama && ollama pull qwen2.5:14b`

### Step 3 — Phase 0.2 + 0.3 실행 (결정과 무관, 언제든 무료)
19개 `.skill` 추출 + SKILLS_MAP.md 작성. 옵션 무엇을 고르든 이 작업은 필요.

---

## 📋 현재 태스크 큐 (11개 pending)

| ID | 작업 | 상태 |
|---|---|---|
| 15 | Phase 0.2 — 19개 .skill ZIP 추출 | pending |
| 16 | Phase 0.3 — SKILLS_MAP.md 작성 | pending |
| 17 | Phase 1.1 — scene 단위 생성기 | pending |
| 18 | Phase 1.2 — 문체 엔진 통합 | pending |
| 19 | Phase 1.3 — 대사 엔진 통합 | pending |
| 20 | Phase 2.1 — 베타리더 시뮬레이션 (Sonnet) | pending |
| 21 | Phase 2.2 — 일관성 감사 | pending |
| 22 | Phase 2.3 — 교차 검증 파이프라인 | pending |
| 23 | Phase 3 — 3단계 교정 루프 | pending |
| 24 | Phase 4 — 장편 지속성 | pending |
| 25 | Phase 5 — 대시보드 polish | pending |

Provider 추상화(신규 Phase 0.4)는 이지연님 결정 후 추가 예정.

---

## 💡 알려진 한계 & 기술 부채

- **실제 Anthropic API 호출 미검증** — 모델 ID `claude-opus-4-6`, 1M 컨텍스트, 프롬프트 캐싱이 전부 이론상 동작. Phase 0.1 또는 옵션 1로 1회 검증 필요.
- **대시보드 Diff 뷰 없음** — 현재 Draft/Final 두 탭으로 분리. Phase 5.2에서 해결 예정.
- **Bible 모달에서 새 인물 파일 생성 불가** — 기존 파일 수정만. 작은 UX 누락.
- **잡 히스토리 휘발성** — 서버 재시작 시 사라짐. DB 또는 JSONL 영속화 필요.
- **스킬 라이선스 미확인** — 이식 시 프롬프트를 완전히 재작성할 예정 (복사 금지).
- **장편 누적 상태 관리 없음** — Phase 4.1에서 해결 예정.

---

## 🔑 인증·환경 메모

- gh CLI 2.89.0 설치됨 (`/opt/homebrew/bin/gh`)
- gh 인증 완료 (`ezleeji38-lgtm` 계정, `gist, read:org, repo` 스코프)
- git credential helper: gh 자동 연결 완료
- git user (repo-local): 이지연 / ezleeji38@gmail.com
- Python 3.14.3 + `.venv/` 가상환경 + `pip install -e .` 편집 모드
- `.env` 아직 없음 — ANTHROPIC_API_KEY 미설정

---

## 📞 재개 시 첫 질문

이 파일을 읽고 가장 먼저 이지연님에게 할 질문:

> **"지난 번에 v0.3 시작 전에 무료 실행 경로 결정하다가 멈췄습니다.  
> α(채팅 수동), β(Gemini 자동), γ(하이브리드 추천), δ(Ollama 로컬) 중 어느 걸로 갈까요?  
> 결정해주시면 바로 Phase 0.2(스킬 추출)부터 착수합니다."**

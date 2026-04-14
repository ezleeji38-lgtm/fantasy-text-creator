# fantasy-text-creator

**한국어 판타지 소설 단행본 제작 통합 저장소.**
두 축으로 구성됩니다:

1. **`novelcraft/`** — 이지연 판타지 소설 자동 집필 시스템 (Python 파이프라인 + FastAPI 대시보드)
2. **`*.skill` 파일들** — Claude Code용 판타지 집필 스킬 모음 (Phase 1~6)

---

## Part 1 · novelcraft 집필 파이프라인

작가가 세계관·캐릭터 Bible을 설계하고 Claude Opus가 챕터를 집필한다.
CLI + 로컬 웹 대시보드(atelier) 지원.

### 설치
```bash
cd "/Users/ijiyeon/커서/fantasy novel"
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
# .env 파일을 열어 ANTHROPIC_API_KEY 입력
```

### 워크플로우

**1. 프로젝트 생성**
```bash
novelcraft init "작품명" --genre "정통 판타지" --target-length 100000
```

**2. Bible 작성 (작가 수동)**
생성된 `projects/작품명/` 폴더에서 다음 파일을 직접 채운다:
- `bible/world.md` — 세계관
- `bible/characters/*.md` — 인물 프로필 (말투·성격·관계)
- `bible/timeline.md` — 연표
- `bible/glossary.md` — 용어집
- `bible/themes.md` — 주제의식
- `outline/synopsis.md` — 시놉시스
- `outline/arcs.md` — 3막 구조
- `outline/chapters.md` — 챕터 비트 (`## ch01` 헤더로 구분)
- `behavior.md` — 이지연 문체 가이드

**3. Bible 점검**
```bash
novelcraft bible-check -p 작품명
```

**4. 챕터 집필 (CLI)**
```bash
novelcraft write ch01 -p 작품명
```
- Bible 전체가 Claude Opus 프롬프트 캐시에 업로드됨 (5분 TTL)
- 본문 집필 → 자가리뷰 → 연속성 요약 생성
- 저장 위치:
  - 초고: `drafts/ch01_draft.md`
  - 리뷰: `drafts/ch01_review.json`
  - 요약: `memory/chapter_summaries/ch01_summary.md`

**5. 대시보드 atelier (권장)**
```bash
novelcraft dashboard
```
브라우저에서 `http://127.0.0.1:8765` 접속:
- 챕터 셀 클릭 → 우측 드로어 → **집필 시작** 버튼 + 실시간 로그 스트리밍
- 리뷰 이슈 카드로 표시 → **최종 승인**으로 `final/`에 승격
- Bible 인라인 편집 모달

### 비용
- Bible 프롬프트 캐싱 적용 시 10만자 단행본 1권 ≈ $40~80
- 연속 챕터 집필 시 Bible이 캐시에 유지되어 비용 최적화

### 진행 현황
- [x] v0.1 MVP — `init` / `write` / `bible-check`
- [x] v0.2 Atelier — FastAPI 대시보드, 백그라운드 잡, SSE 로그, Bible 인라인 편집, 최종 승인
- [ ] v0.3 — 씬 단위 집필, Sonnet 교차 리뷰, 일관성 검증, 3단계 교정

자세한 설계는 `SYSTEM_DESIGN.md` 참고.

---

## Part 2 · Claude Code 판타지 스킬 모음

저장소에 포함된 `.skill` 파일들은 Claude Code용 판타지 집필 스킬입니다.
판타지 소설 창작의 각 단계를 지원하도록 Phase 1~6으로 구성되어 있습니다.

### 설치 방법

각 `.skill` 파일을 다운로드한 후, Claude 프로젝트 설정(Settings)에서 **Skills** 또는 **Custom Skills** 메뉴로 들어가 `.skill` 파일을 업로드합니다.
파일을 하나씩 업로드해도 되고, 모두 다운로드 후 순서대로 설치해도 됩니다.
설치 순서는 아래 Phase 순서를 권장합니다.

### Phase 구성

| Phase | 스킬 | 역할 |
|---|---|---|
| **1 · 세계 기반** | `fantasy-worldbuilder` · `species-culture-designer` · `magic-system-architect` | 세계관·종족·마법체계 설계 |
| **2 · 인물 망** | `character-arc-engineer` · `relationship-web-mapper` | 캐릭터 아크·관계망 |
| **3 · 플롯 구조** | `plot-architecture-engine` · `conflict-tension-designer` · `foreshadow-twist-weaver` | 3막 구조·갈등·복선 |
| **4 · 씬 집필** | `prose-style-engine` · `dialogue-voice-engine` · `action-battle-choreographer` · `scene-chapter-composer` | 문체·대사·전투·씬 조립 |
| **5 · 검수** | `consistency-auditor` · `pacing-rhythm-optimizer` · `beta-reader-simulator` · `revision-rewrite-engine` | 일관성·페이싱·베타리더·교정 |
| **6 · 확장** | `series-expansion-planner` · `fantasy-novel-assembler` | 시리즈 확장·최종 조립 |

### novelcraft와 함께 쓰기

두 도구는 상호보완적입니다:

- **스킬** — Claude Code 대화 중에 불러 쓰는 **설계·브레인스토밍** 도구. 세계관을 처음부터 잡거나 막힌 플롯을 풀 때 사용.
- **novelcraft** — 설계가 끝난 뒤 **본격 집필·교정·출간 파이프라인**. Bible을 고정하고 챕터를 반복 생성.

권장 워크플로우:
1. **Phase 1~3 스킬**로 세계관·인물·플롯 초안을 Claude Code에서 설계
2. 결과물을 `projects/작품명/bible/` 와 `outline/` 에 정리해 저장
3. **`novelcraft write`** 로 챕터 집필
4. **Phase 5 스킬**로 검수(consistency-auditor 등), 필요 시 수정사항을 Bible에 반영
5. 다음 챕터 반복

---

## 라이선스·출처

- `novelcraft/` · `prompts/` · `SYSTEM_DESIGN.md` — 이지연 창작
- `*.skill` 파일 — 원 저장소에서 가져옴(Fantasy Text Creator 스킬 컬렉션)

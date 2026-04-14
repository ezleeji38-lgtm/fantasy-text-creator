# 이지연 판타지 소설 자동 집필 시스템 설계서

> **목표:** 작가(이지연)가 세계관·캐릭터·플롯을 직접 설계하고, AI가 챕터 본문을 집필하여 **한국어 판타지 단행본 출간**까지 완주하는 로컬 파이프라인.

---

## 1. 설계 철학

### 핵심 원칙
1. **작가 주도(Author-first)** — AI는 집필 보조자이지 작가가 아니다. Bible(세계관·인물) 파일은 작가만 수정한다.
2. **Bible 고정, 챕터 생성** — 한 번 확정된 설정은 모든 챕터 집필 시 컨텍스트로 주입되어 일관성을 보장한다.
3. **출간 품질 우선** — 웹연재가 아닌 단행본 기준. 자가리뷰 + 3단계 교정(구조→씬→문장)을 거친다.
4. **한국어 판타지 네이티브** — 영어 도구 번역이 아니라, 처음부터 한국어 출간 시장(교보/예스24/리디)을 목표로 톤·어휘·호흡을 설계한다.

### 두 도구의 장점 결합
| 요소 | 출처 | 채택 이유 |
|---|---|---|
| **CLI 기반 단순 워크플로우** | storycraftr | 작가가 챕터 단위로 통제 가능, 학습곡선 낮음 |
| **Bible 시스템 (캐릭터/세계관 분리)** | authorclaw | 장편 일관성의 핵심 |
| **6단계 파이프라인 (Planning→Production→Revision)** | authorclaw | 출간 품질 확보 |
| **Smart Excerpt (앞 4K + 뒤 1K 워드 주입)** | authorclaw | 컨텍스트 비용 최적화 |
| **behavior.txt (작가 스타일 가이드)** | storycraftr | 이지연 전용 문체 고정 |
| **3단계 교정 (Structural/Scene/Line)** | authorclaw | 단행본 품질 |

### 의도적으로 버리는 것
- ❌ AI가 세계관·캐릭터 자동 생성 — 작가가 직접 설계
- ❌ 마케팅/출간 자동화 (blurb, ad copy) — MVP 단계에서는 집필에만 집중
- ❌ 멀티 페르소나 시스템 — 이지연 단일 필명
- ❌ Telegram/Discord 브리지 — 로컬 CLI만
- ❌ 복잡한 스킬 라우팅 — 고정 파이프라인

---

## 2. 기술 스택

| 레이어 | 선택 | 이유 |
|---|---|---|
| 언어 | **Python 3.11+** | storycraftr 호환, 이지연 기존 프로젝트와 일관 |
| LLM | **Claude Opus 4.6 (1M context)** | 한국어 창작 품질 최상, 1M 컨텍스트로 장편 Bible 전체 주입 가능 |
| SDK | **anthropic Python SDK** | 프롬프트 캐싱 지원 (Bible 캐싱으로 비용 70%+ 절감) |
| 저장 | **Markdown + JSON** | 작가가 직접 편집, Git 버전 관리 |
| CLI | **click** | storycraftr와 동일 패턴 |
| 실행 | **로컬 터미널** | 외부 서버/계정 불필요 |

### 비용 추산 (10만자 단행본 1권 기준)
- 프롬프트 캐싱 적용: **약 $40~80**
- 캐싱 미적용: 약 $200~300
- 👉 Bible을 캐시에 올리는 것이 핵심

---

## 3. 폴더 구조

```
fantasy novel/
├── SYSTEM_DESIGN.md           # 본 문서
├── README.md                  # 사용법
├── pyproject.toml             # 의존성
├── .env                       # ANTHROPIC_API_KEY
│
├── novelcraft/                # 코어 패키지
│   ├── __init__.py
│   ├── cli.py                 # click 엔트리포인트
│   ├── config.py              # 프로젝트 설정 로더
│   ├── bible.py               # Bible 로딩/주입
│   ├── writer.py              # 챕터 집필 (Claude 호출)
│   ├── reviewer.py            # 자가리뷰 + 3단계 교정
│   ├── consistency.py         # 설정 충돌 검증
│   ├── cache.py               # Anthropic 프롬프트 캐싱
│   └── export.py              # DOCX/EPUB 출력
│
├── prompts/                   # 프롬프트 템플릿 (한국어)
│   ├── write_chapter.md       # 챕터 집필 지시
│   ├── self_review.md         # 자가리뷰
│   ├── revise_structural.md   # 1차: 구조 교정
│   ├── revise_scene.md        # 2차: 씬 교정
│   ├── revise_line.md         # 3차: 문장 교정
│   └── consistency_check.md   # 설정 충돌 검사
│
└── projects/                  # 작품별 폴더
    └── {작품명}/
        ├── project.json       # 작품 메타 (장르, 목표 분량, 권수)
        ├── behavior.md        # 이지연 문체 가이드
        │
        ├── bible/             # ⭐ 작가가 직접 작성/편집
        │   ├── world.md       # 세계관 (지리/역사/마법체계/정치)
        │   ├── characters/    # 인물별 파일
        │   │   ├── 주인공.md
        │   │   ├── 히로인.md
        │   │   └── ...
        │   ├── timeline.md    # 연표
        │   ├── glossary.md    # 고유명사·용어집
        │   └── themes.md      # 주제의식·톤
        │
        ├── outline/           # 플롯 아우트라인
        │   ├── synopsis.md    # 전체 시놉시스
        │   ├── arcs.md        # 3막 구조
        │   └── chapters.md    # 챕터별 비트 (제목+요약)
        │
        ├── drafts/            # AI가 생성한 초고
        │   ├── ch01_draft.md
        │   ├── ch02_draft.md
        │   └── ...
        │
        ├── revisions/         # 교정본 (3단계별)
        │   ├── ch01_r1_structural.md
        │   ├── ch01_r2_scene.md
        │   └── ch01_r3_line.md
        │
        ├── final/             # 최종본 (작가 확정)
        │   └── ch01.md
        │
        ├── memory/            # AI 컨텍스트용 요약
        │   ├── bible_summary.md      # Bible 압축본
        │   └── chapter_summaries/    # 회차별 요약 (다음 챕터 집필시 주입)
        │       └── ch01_summary.md
        │
        └── export/            # 출간 파일
            ├── manuscript.docx
            └── manuscript.epub
```

---

## 4. 워크플로우

### Phase 0: 프로젝트 초기화 (1회)
```bash
novelcraft init "작품명"
```
- `projects/{작품명}/` 생성
- `bible/`, `outline/` 템플릿 파일 생성 (빈 양식)
- `behavior.md`에 이지연 기본 문체 가이드 복사

### Phase 1: 작가 설계 (수동, AI 개입 없음) ⭐
**이지연이 직접 작성하는 파일:**
1. `bible/world.md` — 세계관, 마법체계, 지리, 역사, 정치
2. `bible/characters/*.md` — 인물별 프로필 (목표·갈등·말투·외형·관계)
3. `bible/timeline.md` — 주요 사건 연표
4. `bible/glossary.md` — 고유명사
5. `bible/themes.md` — 주제·톤
6. `outline/synopsis.md` — 전체 시놉시스
7. `outline/arcs.md` — 3막 구조
8. `outline/chapters.md` — 챕터별 비트 (제목 + 3~5줄 요약)

> 💡 이 단계가 가장 중요. AI는 여기 적힌 것만 따른다.

### Phase 2: Bible 검증
```bash
novelcraft bible check
```
- Bible 내부 모순 검사 (예: 캐릭터 나이 vs 연표 충돌)
- 누락 필드 경고 (예: 주인공 "말투" 항목 비어있음)
- ✅/⚠️/❌ 리포트 출력

### Phase 3: 챕터 집필
```bash
novelcraft write ch01
novelcraft write ch02 --prev-summary  # 직전 챕터 요약 자동 주입
```
**내부 동작:**
1. `bible/` 전체를 **프롬프트 캐시**에 로드 (Claude 1M 컨텍스트 활용)
2. `outline/chapters.md`에서 해당 챕터 비트 추출
3. 직전 챕터 요약 주입 (`memory/chapter_summaries/`)
4. `behavior.md`의 이지연 문체 가이드 주입
5. Claude Opus가 한국어 본문 집필 (목표: 5,000~8,000자)
6. 즉시 **자가리뷰** (캐릭터 일관성·연속성 스팟체크)
7. `drafts/ch01_draft.md`에 저장
8. `memory/chapter_summaries/ch01_summary.md` 자동 생성

### Phase 4: 교정 (3단계)
```bash
novelcraft revise ch01 --pass structural  # 1차: 플롯홀, 페이싱, 씬 순서
novelcraft revise ch01 --pass scene       # 2차: 캐릭터 일관성, 대사, 긴장감
novelcraft revise ch01 --pass line        # 3차: 문장, 어휘, 호흡
```
각 패스는 `revisions/` 폴더에 버전별로 저장 → **작가가 수동으로 `final/ch01.md` 확정**

### Phase 5: 일관성 검증 (주기적)
```bash
novelcraft consistency --chapters 1-10
```
- 여러 챕터를 동시에 로드해 Bible과 충돌 검사
- 복선 회수 추적 (arcs.md와 대조)
- 캐릭터 말투 드리프트 감지

### Phase 6: 출간 파일 생성
```bash
novelcraft export --format docx
novelcraft export --format epub
```
- `final/` 폴더의 확정 챕터를 조립
- 표지·목차·판권·작가소개 자동 삽입
- 교보/예스24/리디 업로드용 파일 생성

---

## 5. 핵심 기술 요소

### 5.1 Bible 프롬프트 캐싱 (비용 최적화의 핵심)
```python
# novelcraft/cache.py 개요
messages = [{
    "role": "user",
    "content": [
        {
            "type": "text",
            "text": bible_full_text,
            "cache_control": {"type": "ephemeral"}  # ⭐ Bible 캐싱
        },
        {
            "type": "text",
            "text": f"다음 챕터를 집필하라:\n{chapter_beat}"
        }
    ]
}]
```
- Bible은 한 번 업로드되면 **5분 TTL** 내에 재사용 시 90% 비용 절감
- 연속으로 여러 챕터 생성 시 Bible이 캐시에 유지됨
- 10만자 Bible도 1M 컨텍스트에 여유있게 수용

### 5.2 Smart Excerpt (authorclaw 차용)
Bible이 너무 커지면(20만자 이상) 전체 주입 대신 압축:
- **앞 4,000 단어**: 세계관 개요, 핵심 설정, 주인공 기본 정보
- **뒤 1,000 단어**: 현재 진행 상태, 최근 변경사항
- 중간은 **벡터 검색**으로 해당 챕터와 관련된 부분만 추출

### 5.3 이지연 전용 문체 가이드 (`behavior.md`)
```markdown
# 이지연 판타지 문체 가이드

## 톤
- 서정적이면서 무게감 있는 문장
- 기독교 세계관 은유 허용 (직접 설교 금지)
- ...

## 호흡
- 평균 문장 길이: 20~35자
- 대사 비중: 30~40%
- ...

## 금지어
- "~것 같다" (추측 남발 금지)
- 지나친 감탄사
- ...
```
모든 챕터 집필·교정 시 이 파일이 시스템 프롬프트에 주입됨.

### 5.4 일관성 검증 로직 (AI_NovelGenerator 차용)
```
[챕터1-10 본문] + [Bible] 
  → Claude: "다음 항목의 충돌/누락을 JSON으로 보고하라"
     - 캐릭터 외형/나이/관계 변동
     - 마법체계 규칙 위반
     - 시간선 모순
     - 미회수 복선
```

---

## 6. 구현 로드맵

### Milestone 1: MVP (1~2주)
- [ ] `novelcraft init` — 프로젝트 스캐폴딩
- [ ] `novelcraft write` — 단일 챕터 집필 (Bible 주입 + 프롬프트 캐싱)
- [ ] 한국어 프롬프트 템플릿 3종 (집필/자가리뷰/요약)
- [ ] 기본 Bible 템플릿 제공
- **검증:** 이지연님이 세계관 1개·인물 3명만 만들고 1화 집필 → 품질 평가

### Milestone 2: 교정 루프 (1주)
- [ ] `novelcraft revise --pass structural/scene/line`
- [ ] 3단계 교정 프롬프트 작성
- [ ] 버전 관리 (revisions 폴더)

### Milestone 3: 일관성 검증 (1주)
- [ ] `novelcraft bible check`
- [ ] `novelcraft consistency --chapters`
- [ ] JSON 리포트 포맷

### Milestone 4: 출간 파이프라인 (1주)
- [ ] `novelcraft export --format docx/epub`
- [ ] 단행본 조판 (표지·목차·판권)

### Milestone 5: 최적화
- [ ] Smart Excerpt (Bible 20만자 초과 시)
- [ ] 벡터 검색 기반 컨텍스트 추출
- [ ] 챕터 간 복선 회수 추적

---

## 7. 다음 액션

**즉시 시작 가능한 2가지 옵션:**

### Option A — 바로 구현 착수
Milestone 1 MVP를 지금 만들기 시작. Python 프로젝트 스캐폴딩 + `novelcraft init` + `novelcraft write` 최소 구현.

### Option B — 설계 보완 먼저
다음을 먼저 확정:
1. 출간하려는 작품의 **장르 서브타입** (정통 판타지 / 로맨스 판타지 / 현대 판타지 / 이세계물…)
2. **목표 분량**: 한 권 10만자? 12만자? 총 몇 권?
3. **기독교 세계관 요소** 포함 여부 (M.Div 전도사 배경 활용)
4. `behavior.md`에 들어갈 이지연 문체 샘플 (기존 설교 원고에서 추출 가능)

이지연님 선택에 따라 다음 단계로 진행합니다.

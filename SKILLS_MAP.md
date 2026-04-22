# SKILLS_MAP — 19개 스킬 → novelcraft 기능 매핑표

> Phase 0.3 산출물. 각 스킬의 핵심 기법을 novelcraft 프롬프트/코드에 이식할 때 참조.

## 매핑 총괄표

| # | 스킬 | Phase | 핵심 기법 | novelcraft 이식 대상 | 우선순위 |
|---|---|---|---|---|---|
| 1 | **scene-chapter-composer** | 4 | Scene-Sequel 패턴 (목표-갈등-재난 / 반응-딜레마-결정), 챕터 엔딩 훅, POV 전환 | **Phase 1.1** — scene.py 씬 분해·조립 | ⭐ HIGH |
| 2 | **prose-style-engine** | 4 | 문체 프로파일, Show Don't Tell, 5감 묘사, Info-dump 해소, 문장 리듬 | **Phase 1.2** — behavior.md 강화 + write_chapter.md | ⭐ HIGH |
| 3 | **dialogue-voice-engine** | 4 | 캐릭터별 음성 프로파일, 서브텍스트, 대화 태그/비트 | **Phase 1.3** — 인물 카드 말투 검증 프롬프트 | ⭐ HIGH |
| 4 | **beta-reader-simulator** | 5 | 6개 독자 페르소나(매니아·캐주얼·비평가·10대·편집자·글로벌), 몰입도 진단, 읽기중단지점 | **Phase 2.1** — reviewer.py Sonnet 교차리뷰 | ⭐ HIGH |
| 5 | **consistency-auditor** | 5 | 6영역 감사 (마법규칙·캐릭터행동·시간선·지리·고유명사·세계관규칙), 오류분류·우선순위 | **Phase 2.2** — consistency.py + CLI | ⭐ HIGH |
| 6 | **revision-rewrite-engine** | 5 | 연쇄영향 추적, 수정 우선순위 결정, 단계적 수정 계획, 파급효과 관리 | **Phase 3** — 3단계 교정 프롬프트 | ⭐ HIGH |
| 7 | **foreshadow-twist-weaver** | 3 | 복선 강도 조절(명시적/암시적/잠재적), 적색 청어, "놀랍지만 불가피한" 반전 설계 | **Phase 4.2** — foreshadowing.json 추적 | MEDIUM |
| 8 | **character-arc-engineer** | 2 | 거짓 믿음-진실 구조 (K.M. Weiland), 유령/상처 (Truby), 긍정/플랫/부정 아크 | **Phase 4.3** — character_arcs.json | MEDIUM |
| 9 | **conflict-tension-designer** | 3 | 4층위 갈등 (내적·대인·사회·우주적), 에스컬레이션, 딜레마 설계, 스테이크 관리 | **Phase 1.1** — 씬별 갈등 레이어 주입 | MEDIUM |
| 10 | **pacing-rhythm-optimizer** | 5 | 긴장-이완 곡선, 정보 밀도 분포, 감정 곡선, 장르별 페이싱 가이드 | **Phase 2.2/3** — 챕터 간 페이싱 진단 | MEDIUM |
| 11 | **plot-architecture-engine** | 3 | 3막/영웅여정/7점/Save the Cat 비트시트, 다중POV 직조, 매크로플롯 | 이미 arcs.md로 구현. 참조용 | LOW |
| 12 | **action-battle-choreographer** | 4 | 전투의 서사적 기능, 전투 안무, 마법 전투, 전투 문체 리듬 | **Phase 1.1** — 전투 씬 전용 프롬프트 | LOW |
| 13 | **relationship-web-mapper** | 2 | 동적 관계 변화 추적, 관계-플롯 연동, 관계 변화 그래프 | **Phase 4.3** — 관계 변화 추적 | LOW |
| 14 | **fantasy-worldbuilder** | 1 | 지리→문화→갈등→역사 인과사슬, 8개 요소 통합 | Bible 설계 시 참조. 이미 world.md 작성됨 | LOW |
| 15 | **magic-system-architect** | 1 | Sanderson 3법칙, 하드/소프트 매직, 대가 설계 | Bible 설계 시 참조. 성화 체계 이미 작성됨 | LOW |
| 16 | **species-culture-designer** | 1 | 생물학→사회→가치관→갈등 인과사슬, 종족 재해석 | 현재 작품에 비인간 종족 없음. 미사용 | SKIP |
| 17 | **fantasy-novel-assembler** | 6 | 원고 조판, 프롤로그/에필로그, 부록, 쿼리레터, 시놉시스 | **Phase 5** — export.py DOCX/EPUB | LOW |
| 18 | **series-expansion-planner** | 6 | 시리즈 비전, 권별 아크, 장기 복선, 1권의 독립성 | 현재 1권 완결 구조. 미사용 | SKIP |
| 19 | **writing-workflow** | — | 단편 콘텐츠용 5단계 프로세스 | 소설이 아닌 단편 콘텐츠용. 미사용 | SKIP |

## Phase별 이식 그룹

### Phase 1 (Quality Core) → 스킬 3개
- `scene-chapter-composer` → **씬 분해·조립 로직** (Scene-Sequel 패턴)
- `prose-style-engine` → **문체 프로파일 + 5감 레이어링** (behavior.md/프롬프트 강화)
- `dialogue-voice-engine` → **캐릭터 음성 프로파일 + 서브텍스트** (인물별 말투 가드)

### Phase 2 (Review) → 스킬 2개
- `beta-reader-simulator` → **6개 독자 페르소나 리뷰** (Sonnet 교차 모델)
- `consistency-auditor` → **6영역 일관성 감사** (마법·캐릭터·시간·지리·고유명사·세계관)

### Phase 3 (Revision) → 스킬 1개
- `revision-rewrite-engine` → **연쇄영향 추적 + 3패스 교정 프롬프트**

### Phase 4 (Long-form) → 스킬 2개
- `foreshadow-twist-weaver` → **복선 추적 DB** (강도 분류, 회수 체크)
- `character-arc-engineer` → **캐릭터 아크 추적** (거짓 믿음-진실 진행률)

## 핵심 기법 발췌 (프롬프트 이식 시 직접 참고)

### scene-chapter-composer — Scene-Sequel 패턴
```
Scene(장면): 목표(Goal) → 갈등(Conflict) → 재난(Disaster)
Sequel(반응): 반응(Reaction) → 딜레마(Dilemma) → 결정(Decision)
```
- 모든 씬은 이 중 하나의 패턴을 따른다
- Scene은 행동과 긴장, Sequel은 감정과 성찰
- 이 교대의 리듬이 페이지 터너를 만든다

### prose-style-engine — 문체 5원칙
1. 문체는 세계관의 일부 (현대어 금지)
2. Show Don't Tell (감각→행동→내면 순서)
3. 5감 레이어링 (시각만 쓰면 평면적)
4. Info-dump는 갈등 속에 숨긴다 (설명 장면 금지)
5. 문장 리듬 = 감정 리듬 (짧은 문장=긴장, 긴 문장=성찰)

### beta-reader-simulator — 6개 페르소나
1. 장르 매니아: 마법 체계 논리, 세계관 일관성
2. 캐주얼 리더: 몰입도, 이해 가능성
3. 전문 비평가: 산문 품질, 주제 깊이
4. 10대 독자: 페이싱, 감정 공감
5. 출판 편집자: 시장성, 구조 완성도
6. 글로벌 독자: 문화 번역 가능성

### consistency-auditor — 6영역 감사
1. 마법 규칙 모순 (성화 대가가 ch05에서 달라진 건 아닌지)
2. 캐릭터 행동 비일관성 (말투 드리프트, 성격 위반)
3. 시간선 오류 (낮인데 별이 보인다)
4. 지리적 모순 (3일 걸린다던 거리를 하루 만에)
5. 고유명사 오류 (세레스 vs 세레르스 오타)
6. 세계관 규칙 위반 (혈통만 성화 쓰는데 일반인이 쓰는 장면)

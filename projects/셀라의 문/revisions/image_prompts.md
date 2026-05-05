# 「셀라의 문」 이미지 생성 prompts (14장)

> Gemini API가 무료 티어에서 막혀서 자동 생성 불가. 이 파일의 prompt들을
> ChatGPT Plus / Bing Image Creator / Midjourney / Leonardo.ai 등에 그대로
> 복사 붙여넣어 사용하세요.

## 추천 도구별 사용법

### A. ChatGPT Plus (DALL-E 3) — 가장 추천
1. ChatGPT.com 접속, GPT-4 or GPT-4o 선택
2. 아래 프롬프트 하나씩 채팅에 붙여넣기
3. 생성된 이미지 다운로드 → `projects/셀라의 문/images/` 폴더에 저장
4. 파일명은 아래 §3 표 기준으로

### B. Bing Image Creator (무료)
1. bing.com/create 접속, MS 계정 로그인
2. 같은 프롬프트 영문으로 입력 (한글도 작동하지만 영문 권장)
3. 4장씩 생성됨 — 마음에 드는 1장 다운로드

### C. Midjourney (Discord)
1. /imagine 뒤에 prompt + ` --ar 2:3 --v 6 --style raw` 추가
2. 표지는 2:3, 본문 챕터는 16:9 추천

---

## 공통 스타일 가이드 (모든 prompt에 적용)

```
Painterly digital art in the style of literary fantasy book illustrations.
Atmospheric, quiet, contemplative mood.
Color palette: deep midnight blue with silver moonlight accents and warm gold focal points.
Inspired by Naomi Novik 'Spinning Silver' and Katherine Arden 'Bear and the Nightingale' book covers.
NOT anime, NOT manga, NOT cartoon style.
Painterly brushwork, cinematic composition.
```

ChatGPT/DALL-E에서는 이 스타일 가이드를 첫 메시지에 한 번 알려주고, 그
다음부터는 "위 스타일 유지하면서 다음 장면:" 으로 시작하면 효율적.

---

## §3. 14장 prompts

### 0️⃣ 표지 (00_cover.png) — 비율 2:3
**파일명**: `00_cover.png`
**용도**: 책 표지

```
Book cover composition, 2:3 portrait aspect ratio.
A young woman silhouette stands at the center of five ancient standing stones
arranged in a circle on a windswept Cornish hillside at night. A large full moon
is overhead, casting silver-gold light. She holds her right wrist up — a delicate
crescent moon birthmark glows softly silver-gold on the inner wrist. The figure
is in dark silhouette (no facial features). Below: hint of distant sea cliff and
grey waves. Above her: hint of an arched threshold of light forming between two
of the stones. Generous negative space at top for title. Highly minimalist,
dignified, with one bright focal point (the wrist mark). Cool tones with warm
gold accent.

[+ 위 공통 스타일 가이드]
```

---

### 1️⃣ 프롤로그 (01_ch00_prologue.png) — 비율 16:9
**파일명**: `01_ch00_prologue.png`
**챕터**: 프롤로그 — 700년 전 첫 전사가 콘월로 돌아감

```
Wide cinematic landscape aspect, 16:9. 700 years ago.
A silver-leafed forest at night. A solitary warrior figure stands before a
vertical threshold of golden light suspended in midair between silver-barked
trees. The warrior holds up a wrist with a glowing crescent moon birthmark.
Through the threshold of light, a glimpse of grey ocean cliffs and distant
cottage lights — another world. Silver leaves drift slowly. Behind the warrior,
a robed mage watches in stillness. Solemn farewell scene. Mostly dark with
the threshold of light as the brightest element.

[+ 공통 스타일]
```

---

### 2️⃣ ch01 서클 (02_ch01_circle.png)
**파일명**: `02_ch01_circle.png`
**챕터**: 콘월 보름달 밤 환형석 도착

```
Wide cinematic shot, 16:9.
Five ancient standing stones arranged in a circle on a Cornish hillside at night.
A full moon hangs above. Two teenage girl silhouettes approach the circle through
tall grass — one in a blue hoodie, one in a red jacket. Distant view of a small
coastal village with warm yellow window lights, and grey ocean cliffs behind.
The flat altar stone in the center of the circle glows faintly with collected
moonlight. Anticipatory mood, the moment before a threshold opens.

[+ 공통 스타일]
```

---

### 3️⃣ ch02 은빛 숲 (03_ch02_silverforest.png)
**파일명**: `03_ch02_silverforest.png`
**챕터**: 은빛 숲에서 마수 + 레온 첫 등장

```
Cinematic, 16:9.
A magical silver-leafed forest at dawn. Trees with luminescent silver leaves
glow softly. Tiny silver light-particles drift through the air like slow
fireflies. Two girls in modern Earth clothes (one blue hoodie, one red jacket)
stand nervously in the middle distance. Behind them, in the shadow, the silhouette
of a wolf-like beast with too many teeth and yellow glowing eyes. To the side,
a young silver-haired warrior in silver armor with a navy cape draws a glowing
white sword of pure light. The light from the sword illuminates the scene.
Mystical, tense, painterly.

[+ 공통 스타일]
```

---

### 4️⃣ ch03 빛의 도시 (04_ch03_luminas.png)
**파일명**: `04_ch03_luminas.png`
**챕터**: 호수 위 도시 루미나스 도착

```
Wide architectural establishing shot, 16:9.
A breathtaking medieval city of white stone built on a vast still lake, shrouded
in morning mist. The city's tall slender spires reach skyward, each topped with
a glowing orb of light. Below, the same city is mirrored perfectly in the lake's
surface — a city facing both up and down. Translucent bridges of soft light
connect the buildings. Warm dawn light breaks through the mist. The whole scene
has an otherworldly serenity.

[+ 공통 스타일]
```

---

### 5️⃣ ch04 고대 형태 (05_ch04_ancient_form.png)
**파일명**: `05_ch04_ancient_form.png`
**챕터**: 셀라의 능력 첫 의식적 발현

```
Cinematic shot, 16:9.
A circular stone training ground, walls in cool morning light. A young
Korean-British woman stands in the center with her eyes closed, palms open.
Soft warm gold light flows from her wrists into her body — the light is being
absorbed inward, not emitted outward. Her dark hair is lit faintly with a
golden edge. In the foreground, a young silver-haired warrior watches her
with quiet wonder. Geometric magical patterns are etched into the stone floor,
faintly glowing. Above on a balcony in shadow, a robed figure with a staff
observes — barely visible. Composition emphasizes the girl's transformation.

[+ 공통 스타일]
```

---

### 6️⃣ ch05 손님과 도구 (06_ch05_library.png)
**파일명**: `06_ch05_library.png`
**챕터**: 도서관에서 양피지 발견 + 발자국

```
Cinematic interior, 16:9.
Inside a vast circular library tower. Spiral bookshelves rising many stories
high, illuminated by floating glowing orbs of soft light instead of candles.
A skylight far above sends a single shaft of dawn light down through the dust.
A young Korean-British woman kneels at a lower shelf, holding an ancient
parchment that glows faintly in her hands — the parchment shows the design of
five standing stones. Her wrist with a crescent birthmark is faintly visible.
In the deep shadow behind a bookshelf row, the suggestion of a watching figure.
Mysterious, scholarly, atmospheric.

[+ 공통 스타일]
```

---

### 7️⃣ ch06 에밀리의 귀 (07_ch06_market.png)
**파일명**: `07_ch06_market.png`
**챕터**: 호수 위 시장에서 에밀리 + 검은 외투 미행자 암시

```
Cinematic, 16:9.
A medieval marketplace built on wooden floats over a clear lake. Vendors with
stalls of fish, fruit, and woven goods. Soft warm sunlight, lake reflections.
A young teenage girl with short blond hair in a red modern jacket laughs and
gestures to a market vendor — vivid, alive, warm. The red jacket pops against
the cool lake colors. In the background, far down a market alley, the
suggestion of a figure in a dark cloak pausing to watch — barely visible, easy
to miss. The scene reads as warmth and life, with a quiet undercurrent of
being watched.

[+ 공통 스타일]
```

---

### 8️⃣ ch07 폭주 (08_ch07_explosion.png)
**파일명**: `08_ch07_explosion.png`
**챕터**: 셀라 능력 폭주 + 레온 부상

```
Cinematic, 16:9.
The same circular training ground, but now in chaos. The dark-haired young
woman is at the center of a violent expansion of golden light — uncontrolled,
like a small sun rupturing outward. The geometric patterns in the stone floor
crack and shatter, fragments flying. Stone walls fracture. To one side, a
young silver-haired warrior raises a shield of white light against the gold
blast — the shield is breaking. His face shows pain, not fear. Dust, debris,
light. Tragic, not triumphant. Composition emphasizes power that has betrayed
its wielder.

[+ 공통 스타일]
```

---

### 9️⃣ ch08 새장 (09_ch08_cage.png)
**파일명**: `09_ch08_cage.png`
**챕터**: 셀라의 어두운 밤

```
Cinematic interior, 16:9.
Night. A bedroom in a medieval palace, cool moonlight through tall narrow
windows. A young Korean-British woman sits on the floor with her back against
a closed wooden door, knees drawn up, arms around her knees. Her hair falls
forward. She is alone and crying softly — only one tear visible. Beside her,
untouched bread and fruit on a plate. Through the window, the moon disappearing
behind clouds. The room is beautiful but feels like a cage. Composition
emphasizes solitude and small scale of the figure within ornate surroundings.

[+ 공통 스타일]
```

---

### 🔟 ch09 겁쟁이의 선택 (10_ch09_dawn_choice.png)
**파일명**: `10_ch09_dawn_choice.png`
**챕터**: 새벽 대야 위 셀라의 결심

```
Intimate close-shot, 4:5 or 1:1.
Pre-dawn. A washbasin of clear water on a stone shelf. A young woman's face is
reflected in the still water — her face is wet, eyes swollen from crying, but
her expression is now resolved, no longer trembling. Her dark hair is damp.
Behind the basin, the cold blue light of dawn comes through an arched window.
On a stool beside her, neatly folded: a blue modern hoodie, sneakers with
worn soles, ready to be worn. Quiet, decisive moment. The composition focuses
on the reflection — the act of seeing oneself.

[+ 공통 스타일]
```

---

### 1️⃣1️⃣ ch10 달빛 작전 (11_ch10_infiltration.png)
**파일명**: `11_ch10_infiltration.png`
**챕터**: 별관 잠입

```
Cinematic, 16:9, dramatic lighting.
A narrow underground stone corridor lit only by faintly glowing veins of light
embedded in the wall like luminous capillaries. Three figures move silently
along the wall: a tall warrior in light armor, a young woman in modern hoodie,
and an older knight. Their shadows are long. Ahead, an iron door. The young
woman's wrist glows faintly silver, responding to something behind the door.
Tension, infiltration, unknown ahead. Cinematic composition with strong
directional lighting.

[+ 공통 스타일]
```

---

### 1️⃣2️⃣ ch11 겁쟁이의 빛 (12_ch11_gold_light.png)
**파일명**: `12_ch11_gold_light.png`
**챕터**: 셀라의 금빛 능력 완전 발현 (클라이맥스)

```
Cinematic, 16:9.
An underground stone corridor. A young Korean-British woman in a blue hoodie
stands in the center, holding hands with another teenage girl (short blond
hair, red jacket) behind her. Both are afraid but the dark-haired girl is
luminous — golden light flows outward from her body in a calm river (not an
explosion this time), traveling along the floor and walls in waves. The light
gently dissolves attacking white-light spells in midair around them. Her eyes
have a thin gold ring at the edges. To her side, a silver-haired warrior with
a glowing white sword. In the background, a defeated robed mage on his knees,
his staff fallen. Triumphant but quiet — protection, not destruction.

[+ 공통 스타일]
```

---

### 1️⃣3️⃣ ch12 문 앞에서 (13_ch12_two_worlds.png)
**파일명**: `13_ch12_two_worlds.png`
**챕터**: 콘월 절벽 새벽 + 두 세계 빛의 길

```
Wide cinematic shot, 16:9.
Pre-dawn at a Cornish coastal cliff. Two teenage girls (one blue hoodie with
dark hair, one red jacket with blond hair) sit at the cliff's edge, facing
the sea. The sea is purple and gold with sunrise just beginning on the horizon.
A path of golden light lies on the water from horizon to shore — the same
shape as a moon-path on a lake but lit by sunrise instead. The dark-haired
girl's right wrist visible: a small crescent birthmark still glows faintly
silver-gold even though they have returned. Behind them, the five standing
stones in the distance. Quiet, reflective, homecoming with knowledge that
they will return.

[+ 공통 스타일]
```

---

## §4. 사용 후 워크플로우

### 다운로드한 이미지 저장 위치
```
/Users/ijiyeon/커서/fantasy novel/projects/셀라의 문/images/
```

폴더 안에 위 §3의 파일명 그대로 저장:
- 00_cover.png
- 01_ch00_prologue.png
- 02_ch01_circle.png
- ... (총 14장)

### docx에 이미지 삽입하려면
저장 후 알려 주시면 `scripts/export_docx.py` 를 수정해서 각 챕터 시작에
이미지를 자동 삽입하도록 처리해 드리겠습니다.
(python-docx의 `doc.add_picture()` 사용)

### 시안이 마음에 안 들 때
- 같은 prompt 다시 생성 (랜덤성으로 다른 결과)
- "Make it more atmospheric / less anime-style / more like Spinning Silver cover"
  같은 추가 지시
- 아예 다른 컴포지션 옵션 (cover_concept.md §4 참조)

### 한국어 prompt를 원하면
한국어로 번역해서 입력해도 ChatGPT/Bing은 잘 처리합니다. 다만 영문이
일반적으로 결과가 더 정확.

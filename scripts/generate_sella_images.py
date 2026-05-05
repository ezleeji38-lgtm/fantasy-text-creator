"""「셀라의 문」 표지 + 챕터 이미지 14장 생성.

Gemini 2.0 Flash native image generation.
- 표지(cover) 1장
- 프롤로그(ch00) 1장
- 본문 12챕터(ch01~ch12) 각 1장

style guideline (전 이미지 공통):
- literary fantasy book illustration, painterly digital art
- atmospheric, quiet, contemplative, dignified
- color palette: deep midnight blue + silver moonlight + gold accents
- avoid: anime, manga, cartoon, generic stock fantasy
- inspired by: Naomi Novik 'Spinning Silver' / Katherine Arden covers
"""
import os
import sys
import time
import re
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

from google import genai
from google.genai import types

API_KEY = os.environ["GOOGLE_API_KEY"]
client = genai.Client(api_key=API_KEY)
MODEL = "gemini-2.5-flash-image"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = PROJECT_ROOT / "projects" / "셀라의 문" / "images"

# 모든 prompt 에 prepend 되는 공통 스타일 가이드
STYLE_GUIDE = (
    "Painterly digital art in the style of literary fantasy book illustrations. "
    "Atmospheric, quiet, contemplative mood. Color palette: deep midnight blue "
    "with silver moonlight accents and warm gold focal points. "
    "Inspired by Naomi Novik 'Spinning Silver' and Katherine Arden 'Bear and the "
    "Nightingale' book covers. NOT anime, NOT manga, NOT cartoon style. "
    "Painterly brushwork, cinematic composition. "
)

SCENES = [
    # ── 표지 ──
    {
        "file": "00_cover.png",
        "prompt": (
            STYLE_GUIDE +
            "Book cover composition, 2:3 portrait aspect ratio. "
            "A young woman silhouette stands at the center of five ancient standing "
            "stones arranged in a circle on a windswept Cornish hillside at night. "
            "A large full moon is overhead, casting silver-gold light. She holds "
            "her right wrist up — a delicate crescent moon birthmark glows softly "
            "silver-gold on the inner wrist. The figure is in dark silhouette "
            "(no facial features). Below: hint of distant sea cliff and grey waves. "
            "Above her: hint of an arched threshold of light forming between two "
            "of the stones. Generous negative space at top for title. "
            "Highly minimalist, dignified, with one bright focal point (the wrist mark). "
            "Cool tones with warm gold accent."
        ),
    },

    # ── 프롤로그 ──
    {
        "file": "01_ch00_prologue.png",
        "prompt": (
            STYLE_GUIDE +
            "Wide cinematic landscape aspect. 700 years ago. A silver-leafed forest "
            "at night. A solitary warrior figure stands before a vertical threshold "
            "of golden light suspended in midair between silver-barked trees. "
            "The warrior holds up a wrist with a glowing crescent moon birthmark. "
            "Through the threshold of light, a glimpse of grey ocean cliffs and "
            "distant cottage lights — another world. Silver leaves drift slowly. "
            "Behind the warrior, a robed mage watches in stillness. Solemn farewell scene. "
            "Mostly dark with the threshold of light as the brightest element."
        ),
    },

    # ── ch01 서클 ──
    {
        "file": "02_ch01_circle.png",
        "prompt": (
            STYLE_GUIDE +
            "Five ancient standing stones arranged in a circle on a Cornish "
            "hillside at night. A full moon hangs above. Two teenage girl silhouettes "
            "approach the circle through tall grass — one in a blue hoodie, one in a "
            "red jacket. Distant view of a small coastal village with warm yellow "
            "window lights, and grey ocean cliffs behind. The flat altar stone in the "
            "center of the circle glows faintly with collected moonlight. "
            "Anticipatory mood, the moment before a threshold opens. Wide cinematic shot."
        ),
    },

    # ── ch02 은빛 숲 ──
    {
        "file": "03_ch02_silverforest.png",
        "prompt": (
            STYLE_GUIDE +
            "A magical silver-leafed forest at dawn. Trees with luminescent silver "
            "leaves glow softly. Tiny silver light-particles drift through the air "
            "like slow fireflies. Two girls in modern Earth clothes (one blue hoodie, "
            "one red jacket) stand nervously in the middle distance. Behind them, in "
            "the shadow, the silhouette of a wolf-like beast with too many teeth and "
            "yellow glowing eyes. To the side, a young silver-haired warrior in silver "
            "armor with a navy cape draws a glowing white sword of pure light. "
            "The light from the sword illuminates the scene. Mystical, tense, painterly."
        ),
    },

    # ── ch03 빛의 도시 ──
    {
        "file": "04_ch03_luminas.png",
        "prompt": (
            STYLE_GUIDE +
            "A breathtaking medieval city of white stone built on a vast still lake, "
            "shrouded in morning mist. The city's tall slender spires reach skyward, "
            "each topped with a glowing orb of light. Below, the same city is mirrored "
            "perfectly in the lake's surface — a city facing both up and down. "
            "Translucent bridges of soft light connect the buildings. Warm dawn light "
            "breaks through the mist. The whole scene has an otherworldly serenity. "
            "Wide architectural establishing shot."
        ),
    },

    # ── ch04 고대 형태 ──
    {
        "file": "05_ch04_ancient_form.png",
        "prompt": (
            STYLE_GUIDE +
            "A circular stone training ground, walls in cool morning light. A young "
            "Korean-British woman stands in the center with her eyes closed, palms "
            "open. Soft warm gold light flows from her wrists into her body — the "
            "light is being absorbed inward, not emitted outward. Her dark hair is "
            "lit faintly with a golden edge. In the foreground, a young silver-haired "
            "warrior watches her with quiet wonder. Geometric magical patterns are "
            "etched into the stone floor, faintly glowing. Above on a balcony in "
            "shadow, a robed figure with a staff observes — barely visible. "
            "Composition emphasizes the girl's transformation."
        ),
    },

    # ── ch05 손님과 도구 ──
    {
        "file": "06_ch05_library.png",
        "prompt": (
            STYLE_GUIDE +
            "Inside a vast circular library tower. Spiral bookshelves rising "
            "many stories high, illuminated by floating glowing orbs of soft light "
            "instead of candles. A skylight far above sends a single shaft of dawn "
            "light down through the dust. A young Korean-British woman kneels at a "
            "lower shelf, holding an ancient parchment that glows faintly in her "
            "hands — the parchment shows the design of five standing stones. "
            "Her wrist with a crescent birthmark is faintly visible. In the deep "
            "shadow behind a bookshelf row, the suggestion of a watching figure. "
            "Mysterious, scholarly, atmospheric."
        ),
    },

    # ── ch06 에밀리의 귀 ──
    {
        "file": "07_ch06_market.png",
        "prompt": (
            STYLE_GUIDE +
            "A medieval marketplace built on wooden floats over a clear lake. "
            "Vendors with stalls of fish, fruit, and woven goods. Soft warm sunlight, "
            "lake reflections. A young teenage girl with short blond hair in a red "
            "modern jacket laughs and gestures to a market vendor — vivid, alive, "
            "warm. The red jacket pops against the cool lake colors. "
            "In the background, far down a market alley, the suggestion of a figure "
            "in a dark cloak pausing to watch — barely visible, easy to miss. "
            "The scene reads as warmth and life, with a quiet undercurrent of being watched."
        ),
    },

    # ── ch07 폭주 ──
    {
        "file": "08_ch07_explosion.png",
        "prompt": (
            STYLE_GUIDE +
            "The same circular training ground, but now in chaos. The dark-haired "
            "young woman is at the center of a violent expansion of golden light — "
            "uncontrolled, like a small sun rupturing outward. The geometric patterns "
            "in the stone floor crack and shatter, fragments flying. Stone walls "
            "fracture. To one side, a young silver-haired warrior raises a shield of "
            "white light against the gold blast — the shield is breaking. His face "
            "shows pain, not fear. Dust, debris, light. Tragic, not triumphant. "
            "Composition emphasizes power that has betrayed its wielder."
        ),
    },

    # ── ch08 새장 ──
    {
        "file": "09_ch08_cage.png",
        "prompt": (
            STYLE_GUIDE +
            "Night. A bedroom in a medieval palace, cool moonlight through tall "
            "narrow windows. A young Korean-British woman sits on the floor with "
            "her back against a closed wooden door, knees drawn up, arms around her "
            "knees. Her hair falls forward. She is alone and crying softly — only "
            "one tear visible. Beside her, untouched bread and fruit on a plate. "
            "Through the window, the moon disappearing behind clouds. The room is "
            "beautiful but feels like a cage. Composition emphasizes solitude and "
            "small scale of the figure within ornate surroundings."
        ),
    },

    # ── ch09 겁쟁이의 선택 ──
    {
        "file": "10_ch09_dawn_choice.png",
        "prompt": (
            STYLE_GUIDE +
            "Pre-dawn. A washbasin of clear water on a stone shelf. A young woman's "
            "face is reflected in the still water — her face is wet, eyes swollen "
            "from crying, but her expression is now resolved, no longer trembling. "
            "Her dark hair is damp. Behind the basin, the cold blue light of dawn "
            "comes through an arched window. On a stool beside her, neatly folded: "
            "a blue modern hoodie, sneakers with worn soles, ready to be worn. "
            "Quiet, decisive moment. The composition focuses on the reflection — "
            "the act of seeing oneself."
        ),
    },

    # ── ch10 달빛 작전 ──
    {
        "file": "11_ch10_infiltration.png",
        "prompt": (
            STYLE_GUIDE +
            "A narrow underground stone corridor lit only by faintly glowing veins "
            "of light embedded in the wall like luminous capillaries. Three figures "
            "move silently along the wall: a tall warrior in light armor, a "
            "young woman in modern hoodie, and an older knight. Their shadows are "
            "long. Ahead, an iron door. The young woman's wrist glows faintly silver, "
            "responding to something behind the door. Tension, infiltration, unknown "
            "ahead. Cinematic composition with strong directional lighting."
        ),
    },

    # ── ch11 겁쟁이의 빛 ──
    {
        "file": "12_ch11_gold_light.png",
        "prompt": (
            STYLE_GUIDE +
            "An underground stone corridor. A young Korean-British woman in a blue "
            "hoodie stands in the center, holding hands with another teenage girl "
            "(short blond hair, red jacket) behind her. Both are afraid but the dark-haired "
            "girl is luminous — golden light flows outward from her body in a calm river "
            "(not an explosion this time), traveling along the floor and walls in waves. "
            "The light gently dissolves attacking white-light spells in midair around "
            "them. Her eyes have a thin gold ring at the edges. To her side, a "
            "silver-haired warrior with a glowing white sword. In the background, "
            "a defeated robed mage on his knees, his staff fallen. Triumphant but "
            "quiet — protection, not destruction."
        ),
    },

    # ── ch12 문 앞에서 ──
    {
        "file": "13_ch12_two_worlds.png",
        "prompt": (
            STYLE_GUIDE +
            "Pre-dawn at a Cornish coastal cliff. Two teenage girls (one blue hoodie "
            "with dark hair, one red jacket with blond hair) sit at the cliff's edge, "
            "facing the sea. The sea is purple and gold with sunrise just beginning "
            "on the horizon. A path of golden light lies on the water from horizon to "
            "shore — the same shape as a moon-path on a lake but lit by sunrise instead. "
            "The dark-haired girl's right wrist visible: a small crescent birthmark "
            "still glows faintly silver-gold even though they have returned. "
            "Behind them, the five standing stones in the distance. Quiet, reflective, "
            "homecoming with knowledge that they will return. Wide cinematic shot."
        ),
    },
]


def generate_one(scene, max_retries=3):
    """단일 이미지 생성. 429 시 retry-delay 만큼 대기 후 재시도."""
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=scene["prompt"],
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE", "TEXT"],
                ),
            )
            for part in response.candidates[0].content.parts:
                if part.inline_data and part.inline_data.mime_type.startswith("image/"):
                    return part.inline_data.data, None
            text = response.text if hasattr(response, "text") else ""
            return None, f"no image in response. text: {text[:120]}"
        except Exception as e:
            msg = str(e)
            if "RESOURCE_EXHAUSTED" in msg or "429" in msg:
                m = re.search(r"retry in ([\d.]+)s", msg)
                wait = float(m.group(1)) + 1 if m else 30
                print(f"  ⏳ rate limit — {wait:.0f}s 대기 (시도 {attempt + 1}/{max_retries})")
                time.sleep(wait)
                continue
            return None, msg
    return None, "max retries exceeded"


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    total = len(SCENES)
    print(f"이미지 {total}장 생성 시작 → {OUT_DIR}")
    print(f"모델: {MODEL}")

    success = 0
    for i, scene in enumerate(SCENES, 1):
        out_path = OUT_DIR / scene["file"]
        if out_path.exists() and "--force" not in sys.argv:
            print(f"\n[{i}/{total}] {scene['file']} (이미 존재 — 건너뜀)")
            success += 1
            continue

        print(f"\n[{i}/{total}] {scene['file']}")
        print(f"  prompt: {scene['prompt'][:80]}...")

        img_bytes, err = generate_one(scene)
        if img_bytes:
            out_path.write_bytes(img_bytes)
            size_kb = len(img_bytes) / 1024
            print(f"  ✓ saved → {out_path.name} ({size_kb:.0f} KB)")
            success += 1
        else:
            print(f"  ✗ {err}")

        # 다음 요청까지 인터벌 (free tier 분당 한도 회피)
        if i < total:
            time.sleep(6)

    print(f"\n완료: {success}/{total} 성공")
    print(f"저장 경로: {OUT_DIR}")


if __name__ == "__main__":
    main()

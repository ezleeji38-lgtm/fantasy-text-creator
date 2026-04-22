"""판타지 소설 '테스트작품' 핵심 장면 이미지 생성.

Gemini 2.5 Flash native image generation.
"""
import os
import base64
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

from google import genai
from google.genai import types

API_KEY = os.environ["GOOGLE_API_KEY"]
client = genai.Client(api_key=API_KEY)
MODEL = "gemini-2.0-flash-exp"
OUT_DIR = Path("projects/테스트작품/images")

SCENES = [
    {
        "file": "01_kael_portrait.png",
        "prompt": (
            "Generate an image: Dark fantasy character portrait painting. "
            "A 23-year-old male warrior-priest. Short black hair, piercing grey eyes "
            "with a faint silver luminescence. Lean muscular build, broad shoulders. "
            "Wears a worn dark leather coat with a torn-off religious insignia patch "
            "on the chest. A burn scar on his right hand. Expression: stoic and haunted. "
            "Moody low-key lighting, painterly style like a classic fantasy book cover. "
            "Medieval dark fantasy atmosphere. Portrait format."
        ),
    },
    {
        "file": "02_sacred_flame_healing.png",
        "prompt": (
            "Generate an image: A lone warrior kneeling by an old stone well at dusk "
            "in a quiet medieval village. He holds his right hand over a wound on his "
            "left forearm. A delicate silver-white ethereal luminous glow emanates softly "
            "from his palm, healing the wound. The glow is calm and moonlike, not fiery. "
            "Autumn evening, wisps of cooking smoke from distant cottages. "
            "Painterly dark fantasy illustration, cinematic composition."
        ),
    },
    {
        "file": "03_ashwood_forest.png",
        "prompt": (
            "Generate an image: A vast eerie dark forest landscape. Blackened conifer trees "
            "grow from ash-grey soil — remnants of an ancient great fire 200 years ago. "
            "Twisted dark trunks, sparse canopy with shafts of pale light. Faint mist. "
            "An ominous feeling of something ancient and forbidden lurking. A narrow path "
            "disappears into the darkness. Epic landscape, dark fantasy art style, "
            "muted desaturated palette with subtle cool blue tones."
        ),
    },
    {
        "file": "04_dorins_sword.png",
        "prompt": (
            "Generate an image: A half-corroded medieval longsword lying on ash-grey soil "
            "among dark tree roots in a gloomy forest. The blade is partially dissolved "
            "and blackened. On the cross-guard, a faint sun symbol engraving — mark of "
            "a holy order. Dead black pine needles scattered. Dim forest light filtering "
            "through canopy. Close-up still life, dark fantasy painterly style, somber mood."
        ),
    },
    {
        "file": "05_black_flame_dorin.png",
        "prompt": (
            "Generate an image: A tall gaunt man standing alone in a petrified dark forest. "
            "From both hands, black and dark purple magical flames swirl upward — corrupted "
            "sacred fire. His eyes glow faintly violet. On the forest floor, ancient runic "
            "seal patterns glow, forming a containment circle. Tragic sacrificial atmosphere. "
            "Epic dark fantasy illustration, dramatic chiaroscuro lighting."
        ),
    },
    {
        "file": "06_climax_light_vs_dark.png",
        "prompt": (
            "Generate an image: An epic clash of light versus darkness in a dark fantasy forest. "
            "A young warrior unleashes a massive burst of brilliant silver-white sacred flame "
            "from both hands, pushing back a wall of swirling ancient shadow and darkness. "
            "The silver light illuminates the entire forest, trees become silhouettes. "
            "Wide cinematic composition, dramatic contrast between radiant silver and "
            "consuming darkness. Dark fantasy epic art, painterly brushstrokes."
        ),
    },
]


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    total = len(SCENES)

    for i, scene in enumerate(SCENES, 1):
        out_path = OUT_DIR / scene["file"]
        print(f"\n[{i}/{total}] {scene['file']}")
        print(f"  prompt: {scene['prompt'][:80]}...")

        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=scene["prompt"],
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE", "TEXT"],
                ),
            )

            saved = False
            for part in response.candidates[0].content.parts:
                if part.inline_data and part.inline_data.mime_type.startswith("image/"):
                    img_bytes = part.inline_data.data
                    out_path.write_bytes(img_bytes)
                    size_kb = len(img_bytes) / 1024
                    print(f"  ✓ saved → {out_path} ({size_kb:.0f} KB)")
                    saved = True
                    break

            if not saved:
                text = response.text if hasattr(response, "text") else ""
                print(f"  ✗ no image in response. text: {text[:120]}")

        except Exception as e:
            print(f"  ✗ error: {e}")

    print(f"\n완료! 이미지 저장 경로: {OUT_DIR.resolve()}")


if __name__ == "__main__":
    main()

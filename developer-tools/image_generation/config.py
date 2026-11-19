from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[2]
GAME = ROOT / "game"
OUTPUT = Path(__file__).resolve().parents[1] / "image_generation_list.md"
REQUESTS_OUTPUT = Path(__file__).resolve().parents[1] / "image_requests.json"
RULES_PATH = Path(__file__).resolve().parents[1] / "story_image_rules.json"
RULES = json.loads(RULES_PATH.read_text(encoding="utf-8"))
LABEL = re.compile(r"^\s*label\s+([\w]+)\s*:")
SCENE = re.compile(r"^\s*scene\s+((?:bg|cg)_[\w]+)")
TEXT = re.compile(r"""^\s*(["'])(.*)\1\s*:?\s*$""")
IMAGE_DEF = re.compile(r"^\s*image\s+((?:bg|cg)_[\w]+)\s*=.*?[\"'](images/[^\"']+)[\"']")
VISUAL_CUE = re.compile(
    r"\b(arriv\w*|approach\w*|ask\w*|began|check\w*|close\w*|cry\w*|drop\w*|enter\w*|"
    r"find\w*|found|frown\w*|gasp\w*|give\w*|gave|greet\w*|hand\w*|hold\w*|home again|hug\w*|laugh\w*|"
    r"leave\w*|look\w*|open\w*|offer\w*|pick\w*|point\w*|reach\w*|read\w*|run\w*|ran|"
    r"sit\w*|sat|smil\w*|stand\w*|stood|stare\w*|study\w*|sun set|take\w*|took|tomorrow|turn\w*|walk\w*|wave\w*|"
    r"wear\w*|write\w*|complete\w*|over|new day|finished|anxious|angry|embarrassed|excited|"
    r"exhausted|first shift|hopeful|lonely|meet\w*|nervous|relieved|sad|shift over|"
    r"surprised|tired|worried|woke|wrote|felt|thought|crowded|rain|sunlight)\b", re.I)

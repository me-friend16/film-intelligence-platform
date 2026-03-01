import re
from collections import defaultdict
from typing import Dict, List, Any


SCENE_HEADING_RE = re.compile(
    r"^\s*(INT\.|EXT\.|INT\/EXT\.|I\/E\.)\s+(.+)$",
    re.IGNORECASE
)

CHARACTER_RE = re.compile(r"^[A-Z][A-Z0-9 \-'.]{1,40}$")


def _clean_line(line: str) -> str:
    return re.sub(r"\s+", " ", line.strip())


def parse_script(text: str) -> Dict[str, Any]:
    """
    Lightweight screenplay parser (TXT / Fountain-like).
    Extracts:
    - scenes: scene_number, heading, location, time_of_day, raw_lines
    - characters: name, dialogue_count, scene_appearances, scene_presence_map
    """
    lines = text.splitlines()

    scenes: List[Dict[str, Any]] = []
    current_scene = None

    # Tracking
    char_dialogue_count = defaultdict(int)
    char_scene_presence = defaultdict(set)

    scene_index = 0
    pending_character = None

    def start_new_scene(heading_line: str):
        nonlocal current_scene, scene_index
        scene_index += 1

        heading_line = _clean_line(heading_line)
        # Very rough split: "INT. HOUSE - DAY" -> location "HOUSE", time "DAY"
        # We'll improve later.
        location = heading_line
        time_of_day = None
        if " - " in heading_line:
            parts = heading_line.split(" - ", 1)
            location = parts[0]
            time_of_day = parts[1].strip()

        current_scene = {
            "scene_number": scene_index,
            "heading": heading_line,
            "location": location,
            "time_of_day": time_of_day,
            "raw_lines": [],
            "characters": set(),
        }
        scenes.append(current_scene)

    for raw in lines:
        line = _clean_line(raw)

        if not line:
            continue

        # Scene Heading
        if SCENE_HEADING_RE.match(line):
            start_new_scene(line)
            pending_character = None
            continue

        # If no scene has started yet, create a pseudo scene 1
        if current_scene is None:
            start_new_scene("INT. UNKNOWN - DAY")

        # Character Line (ALL CAPS) - simplistic heuristic
        if CHARACTER_RE.match(line) and len(line.split()) <= 4:
            pending_character = line
            current_scene["characters"].add(pending_character)
            char_scene_presence[pending_character].add(current_scene["scene_number"])
            current_scene["raw_lines"].append({"type": "character", "text": line})
            continue

        # Dialogue line (if previous line was character)
        if pending_character:
            # Heuristic: dialogue continues until blank or next heading/character
            char_dialogue_count[pending_character] += 1
            current_scene["raw_lines"].append({"type": "dialogue", "character": pending_character, "text": line})
            continue

        # Action / description
        current_scene["raw_lines"].append({"type": "action", "text": line})

    # Build characters list
    characters = []
    for name, scenes_set in char_scene_presence.items():
        characters.append({
            "name": name,
            "dialogue_count": char_dialogue_count[name],
            "scene_appearances": len(scenes_set),
            "scene_presence_map": sorted(list(scenes_set)),
            "first_appearance_scene": min(scenes_set) if scenes_set else None,
            "last_appearance_scene": max(scenes_set) if scenes_set else None,
        })

    # Convert scene character sets to lists
    for s in scenes:
        s["characters"] = sorted(list(s["characters"]))
        # Optional: summary stub (later improved)
        s["content"] = " ".join([x["text"] for x in s["raw_lines"][:20]])[:500]

    return {
        "scenes": scenes,
        "characters": sorted(characters, key=lambda c: (-c["dialogue_count"], -c["scene_appearances"], c["name"])),
        "meta": {
            "lines": len(lines),
            "scene_count": len(scenes),
            "character_count": len(characters),
        }
    }
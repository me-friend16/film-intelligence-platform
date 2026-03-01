from typing import Dict, Any
from collections import Counter


def analyze_structure(parsed: Dict[str, Any]) -> Dict[str, Any]:
    """
    Uses parsed scenes/characters to compute structure metrics:
    - scene_count
    - character_count
    - top_characters
    - locations_count
    - dialogue_density
    - pacing (slow/medium/fast)
    - night_scene_ratio
    """
    scenes = parsed.get("scenes", [])
    characters = parsed.get("characters", [])

    scene_count = len(scenes)
    character_count = len(characters)

    # Locations (very rough)
    locations = []
    night_scenes = 0
    for s in scenes:
        loc = (s.get("location") or "").strip()
        if loc:
            locations.append(loc.lower())
        tod = (s.get("time_of_day") or "").strip().lower()
        if any(x in tod for x in ["night", "evening", "midnight"]):
            night_scenes += 1

    location_counter = Counter(locations)
    locations_count = len(location_counter)

    # Dialogue density = dialogue lines / total non-empty lines in scenes (rough)
    dialogue_lines = 0
    action_lines = 0
    for s in scenes:
        for item in s.get("raw_lines", []):
            t = item.get("type")
            if t == "dialogue":
                dialogue_lines += 1
            elif t == "action":
                action_lines += 1

    total_story_lines = dialogue_lines + action_lines
    dialogue_density = (dialogue_lines / total_story_lines) if total_story_lines > 0 else 0.0

    # Pacing heuristic:
    # - Fast: lots of scenes + action-heavy
    # - Slow: fewer scenes + dialogue-heavy
    action_ratio = (action_lines / total_story_lines) if total_story_lines > 0 else 0.0

    pacing = "medium"
    if scene_count >= 60 or (scene_count >= 40 and action_ratio >= 0.55):
        pacing = "fast"
    elif scene_count <= 25 or (dialogue_density >= 0.70 and action_ratio <= 0.30):
        pacing = "slow"

    # Top characters (by dialogue count)
    top_chars = sorted(
        [{"name": c["name"], "dialogue_count": c.get("dialogue_count", 0), "scene_appearances": c.get("scene_appearances", 0)}
         for c in characters],
        key=lambda x: (-x["dialogue_count"], -x["scene_appearances"], x["name"])
    )[:8]

    night_scene_ratio = (night_scenes / scene_count) if scene_count > 0 else 0.0

    return {
        "scene_count": scene_count,
        "character_count": character_count,
        "locations_count": locations_count,
        "top_locations": [{"location": k, "count": v} for k, v in location_counter.most_common(10)],
        "dialogue_lines": dialogue_lines,
        "action_lines": action_lines,
        "dialogue_density": round(dialogue_density, 4),
        "action_ratio": round(action_ratio, 4),
        "pacing": pacing,
        "night_scene_ratio": round(night_scene_ratio, 4),
        "top_characters": top_chars,
    }
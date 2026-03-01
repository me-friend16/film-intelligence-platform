from typing import Dict, Any, List


def _estimate_location_cost(locations_count: int) -> float:
    if locations_count <= 3:
        return 0.1
    elif locations_count <= 8:
        return 0.25
    elif locations_count <= 15:
        return 0.4
    return 0.6


def _estimate_cast_cost(character_count: int) -> float:
    if character_count <= 4:
        return 0.1
    elif character_count <= 10:
        return 0.25
    elif character_count <= 20:
        return 0.4
    return 0.6


def estimate_budget(parsed_data: Dict[str, Any], genre_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Hybrid budget estimation:
    - Based on scene count
    - Location diversity
    - Cast size
    - Genre (spectacle vs contained)
    """

    scenes = parsed_data.get("scenes", [])
    characters = parsed_data.get("characters", [])
    meta = parsed_data.get("meta", {})

    scene_count = meta.get("scene_count", len(scenes))
    character_count = meta.get("character_count", len(characters))

    # Unique locations
    locations = set()
    night_scenes = 0
    for s in scenes:
        loc = s.get("location")
        if loc:
            locations.add(loc.lower())
        tod = (s.get("time_of_day") or "").lower()
        if "night" in tod:
            night_scenes += 1

    locations_count = len(locations)

    # Base score
    score = 0.2

    # Scene complexity
    if scene_count > 60:
        score += 0.3
    elif scene_count > 40:
        score += 0.2
    elif scene_count > 25:
        score += 0.1

    # Location impact
    score += _estimate_location_cost(locations_count)

    # Cast impact
    score += _estimate_cast_cost(character_count)

    # Genre multiplier
    genre = (genre_data or {}).get("primary", "drama")

    if genre in ["action", "fantasy", "sci-fi"]:
        score += 0.35
    elif genre in ["thriller", "crime"]:
        score += 0.2
    elif genre in ["drama", "romance", "comedy"]:
        score += 0.1

    # Night shoot cost
    if scene_count > 0:
        night_ratio = night_scenes / scene_count
        if night_ratio > 0.4:
            score += 0.15

    # Normalize score
    score = min(score, 1.0)

    # Determine tier
    if score < 0.35:
        tier = "Low"
        estimated_range = [100000, 800000]
    elif score < 0.65:
        tier = "Medium"
        estimated_range = [800000, 4000000]
    else:
        tier = "High"
        estimated_range = [4000000, 25000000]

    # Cost drivers
    drivers: List[str] = []

    if scene_count > 50:
        drivers.append("High scene count")
    if locations_count > 10:
        drivers.append("Multiple unique locations")
    if character_count > 15:
        drivers.append("Large ensemble cast")
    if genre in ["action", "fantasy", "sci-fi"]:
        drivers.append("Spectacle / VFX-heavy genre")
    if night_scenes > (scene_count * 0.4):
        drivers.append("High percentage of night shoots")

    # Suggestions to reduce cost
    suggestions: List[str] = []

    if locations_count > 8:
        suggestions.append("Combine scenes into fewer locations to reduce logistics cost")
    if character_count > 15:
        suggestions.append("Reduce minor characters or merge roles")
    if night_scenes > (scene_count * 0.4):
        suggestions.append("Convert some night scenes to day shoots if possible")
    if genre in ["action", "fantasy", "sci-fi"]:
        suggestions.append("Minimize VFX-heavy sequences or reduce large-scale action")

    return {
        "tier": tier,
        "estimated_range_usd": estimated_range,
        "budget_complexity_score": round(score, 4),
        "locations_count": locations_count,
        "character_count": character_count,
        "scene_count": scene_count,
        "major_cost_drivers": drivers[:8],
        "cost_reduction_suggestions": suggestions[:8],
        "method": "hybrid_budget_rules_v1"
    }
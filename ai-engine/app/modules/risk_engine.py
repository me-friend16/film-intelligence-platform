from typing import Dict, Any, List


def analyze_risk(parsed_data: Dict[str, Any], structural_metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
    scenes = parsed_data.get("scenes", [])
    characters = parsed_data.get("characters", [])
    meta = parsed_data.get("meta", {})

    scene_count = structural_metrics.get("scene_count", meta.get("scene_count", len(scenes)))
    locations_count = structural_metrics.get("locations_count", 0)
    character_count = structural_metrics.get("character_count", meta.get("character_count", len(characters)))
    night_ratio = structural_metrics.get("night_scene_ratio", 0.0)
    pacing = structural_metrics.get("pacing", "medium")

    flags: List[Dict[str, Any]] = []

    def add_flag(flag_type: str, severity: str, reason: str, suggestion: str):
        flags.append({
            "type": flag_type,
            "severity": severity,  # Low / Medium / High
            "reason": reason,
            "suggestion": suggestion
        })

    # 1) Too many locations
    if locations_count > 15:
        add_flag(
            "High Location Count",
            "High",
            f"Detected {locations_count} unique locations. Logistics and scheduling will be difficult.",
            "Merge locations where possible and rewrite scenes to reuse sets."
        )
    elif locations_count > 8:
        add_flag(
            "Moderate Location Count",
            "Medium",
            f"Detected {locations_count} unique locations. This may increase cost and time.",
            "Group scenes into fewer primary locations and reduce travel requirements."
        )

    # 2) Too many scenes
    if scene_count > 70:
        add_flag(
            "Very High Scene Count",
            "High",
            f"Detected {scene_count} scenes. Production schedule and post will expand significantly.",
            "Combine scenes, remove redundant beats, and simplify transitions."
        )
    elif scene_count > 50:
        add_flag(
            "High Scene Count",
            "Medium",
            f"Detected {scene_count} scenes. Could lead to longer shoot schedule.",
            "Consider compressing multiple small scenes into fewer key scenes."
        )

    # 3) Too many night scenes
    if night_ratio >= 0.45:
        add_flag(
            "High Night Shoot Ratio",
            "High",
            f"Night scenes ratio is {round(night_ratio*100,1)}%. Night shoots are expensive and tiring.",
            "Convert some night scenes into day scenes or reduce night sequences."
        )
    elif night_ratio >= 0.30:
        add_flag(
            "Moderate Night Shoot Ratio",
            "Medium",
            f"Night scenes ratio is {round(night_ratio*100,1)}%.",
            "Plan night shoots in blocks and reduce night-only setups."
        )

    # 4) Overcrowded cast
    if character_count > 25:
        add_flag(
            "Large Ensemble Cast",
            "High",
            f"Detected {character_count} characters. Managing dates, contracts, and continuity becomes hard.",
            "Merge minor characters and reduce speaking roles."
        )
    elif character_count > 15:
        add_flag(
            "Moderate Ensemble Cast",
            "Medium",
            f"Detected {character_count} characters. Casting and scheduling complexity may rise.",
            "Merge supporting roles or reduce number of speaking parts."
        )

    # 5) Weak protagonist dominance (dialogue dominance heuristic)
    if characters:
        total_dialogue = sum([c.get("dialogue_count", 0) for c in characters]) or 1
        top = sorted(characters, key=lambda c: c.get("dialogue_count", 0), reverse=True)[0]
        dominance = (top.get("dialogue_count", 0) / total_dialogue)

        if dominance < 0.22:
            add_flag(
                "Weak Protagonist Focus",
                "Medium",
                f"Top character '{top.get('name')}' dominates only {round(dominance*100,1)}% of dialogue.",
                "Increase protagonist-driven scenes or clarify who the main character is."
            )

    # 6) Pacing risk
    if pacing == "slow" and scene_count > 35:
        add_flag(
            "Slow Pacing Risk",
            "Medium",
            "Dialogue-heavy structure with many scenes can feel slow to general audiences.",
            "Tighten dialogue, shorten scenes, and increase stakes earlier."
        )
    if pacing == "fast" and scene_count < 25:
        add_flag(
            "Fast Pacing Risk",
            "Low",
            "Very fast pacing with few scenes may reduce emotional depth.",
            "Add emotional beats or calmer scenes between high-intensity sequences."
        )

    # If no flags, return a positive signal
    if not flags:
        add_flag(
            "No Major Production Risks Detected",
            "Low",
            "Script structure appears manageable for production.",
            "Proceed to detailed scheduling and breakdown for finer cost control."
        )

    return flags
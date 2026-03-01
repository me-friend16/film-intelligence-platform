from typing import Dict, Any


def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def predict_audience(text: str, genre_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Hybrid Audience Predictor (rules + explainable signals)
    Inputs:
    - text: full script text
    - genre_data: output from genre_predictor

    Outputs:
    - primary_age_group
    - gender_skew
    - platform_fit (OTT / Theatrical / Either)
    - festival_potential (Low/Medium/High)
    - segments (list)
    """
    primary_genre = (genre_data or {}).get("primary", "drama")
    secondary = set((genre_data or {}).get("secondary", []))

    t = (text or "").lower()

    # Signals (simple)
    has_action = any(k in t for k in ["fight", "chase", "gun", "explosion", "attack"])
    has_romance = any(k in t for k in ["love", "kiss", "relationship", "wedding", "breakup"])
    has_horror = any(k in t for k in ["ghost", "demon", "curse", "possession", "haunted"])
    has_court = any(k in t for k in ["court", "trial", "judge", "lawyer", "evidence"])
    has_family = any(k in t for k in ["mother", "father", "family", "son", "daughter"])
    has_comedy = any(k in t for k in ["laugh", "joke", "funny", "hilarious", "prank"])
    has_social = any(k in t for k in ["poverty", "caste", "prostitution", "corruption", "activist", "rights"])

    # Age group logic
    age_group = "18-35"
    if primary_genre in ["horror", "action", "thriller"]:
        age_group = "18-35"
    elif primary_genre in ["drama", "crime"]:
        age_group = "18-45"
    elif primary_genre in ["comedy", "romance"]:
        age_group = "15-35"
    elif primary_genre in ["fantasy", "sci-fi"]:
        age_group = "15-40"

    if has_family and primary_genre == "drama":
        age_group = "18-55"

    # Gender skew heuristic (very rough — can be improved later)
    gender_skew = "Balanced"
    if has_action and not has_romance:
        gender_skew = "Male-leaning"
    if has_romance and not has_action:
        gender_skew = "Female-leaning"
    if has_court or has_social:
        gender_skew = "Balanced"

    # Platform fit: OTT vs theatrical
    platform_fit = "Either"
    # OTT: heavy drama, crime, thriller, limited action, dialogue-heavy
    # Theatrical: action, spectacle, high intensity
    if primary_genre in ["action", "fantasy", "sci-fi"]:
        platform_fit = "Theatrical"
    elif primary_genre in ["drama", "crime", "thriller"]:
        platform_fit = "OTT"
    elif primary_genre in ["romance", "comedy"]:
        platform_fit = "Either"

    # Festival potential
    festival_potential = "Low"
    festival_score = 0.0
    if has_social:
        festival_score += 0.5
    if primary_genre == "drama" or "drama" in secondary:
        festival_score += 0.25
    if has_family:
        festival_score += 0.15
    if has_comedy and not has_social:
        festival_score -= 0.15
    if has_action:
        festival_score -= 0.10

    festival_score = _clamp(festival_score, 0.0, 1.0)
    if festival_score >= 0.65:
        festival_potential = "High"
    elif festival_score >= 0.35:
        festival_potential = "Medium"

    # Audience segments
    segments = []
    if primary_genre in ["thriller", "crime"]:
        segments.append("Mystery/Crime lovers")
    if primary_genre == "action":
        segments.append("Action & adrenaline seekers")
    if primary_genre == "romance":
        segments.append("Romance-driven viewers")
    if primary_genre == "comedy":
        segments.append("Light entertainment viewers")
    if has_social:
        segments.append("Social-issue / message film audience")
    if festival_potential in ["Medium", "High"]:
        segments.append("Festival / critic audience")

    if not segments:
        segments = ["General audience"]

    # Confidence (rough)
    conf = 0.55
    if primary_genre in ["action", "thriller", "horror"]:
        conf += 0.10
    if has_social or has_court:
        conf += 0.05
    conf = _clamp(conf, 0.35, 0.85)

    return {
        "primary_age_group": age_group,
        "gender_skew": gender_skew,
        "platform_fit": platform_fit,
        "festival_potential": festival_potential,
        "segments": segments[:8],
        "confidence": round(conf, 4),
        "method": "hybrid_rules_v1",
        "signals": {
            "has_action": has_action,
            "has_romance": has_romance,
            "has_horror": has_horror,
            "has_courtroom": has_court,
            "has_family": has_family,
            "has_social_issues": has_social,
        }
    }
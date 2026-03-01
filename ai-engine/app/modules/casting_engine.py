from typing import Dict, Any, List


# ✅ Starter actor pools (editable). Later replace with DB/API.
ACTOR_POOLS = {
    "nepal": {
        "low": ["Dayahang Rai", "Bipin Karki", "Swastima Khadka", "Miruna Magar"],
        "medium": ["Nikhil Upreti", "Priyanka Karki", "Keki Adhikari", "Anmol KC"],
        "high": ["Rajesh Hamal", "Rekha Thapa", "Kristi Shrestha", "Aaryan Sigdel"],
    },
    "india": {
        "low": ["Rajkummar Rao", "Pankaj Tripathi", "Triptii Dimri", "Radhika Apte"],
        "medium": ["Ayushmann Khurrana", "Nawazuddin Siddiqui", "Taapsee Pannu", "Vicky Kaushal"],
        "high": ["Shah Rukh Khan", "Aamir Khan", "Deepika Padukone", "Alia Bhatt"],
    },
    "usa": {
        "low": ["Florence Pugh", "Paul Mescal", "Anya Taylor-Joy", "Barry Keoghan"],
        "medium": ["Ryan Gosling", "Zendaya", "Jake Gyllenhaal", "Scarlett Johansson"],
        "high": ["Leonardo DiCaprio", "Tom Cruise", "Meryl Streep", "Denzel Washington"],
    },
}


def _tier_key(budget_tier: str) -> str:
    b = (budget_tier or "").strip().lower()
    if b == "low":
        return "low"
    if b == "high":
        return "high"
    return "medium"


def suggest_casting(parsed_data: Dict[str, Any],
                    genre_data: Dict[str, Any],
                    budget_data: Dict[str, Any],
                    country: str = "nepal") -> List[Dict[str, Any]]:
    """
    Suggest actors based on:
    - country pool
    - budget tier
    - lead character importance (dialogue dominance)
    - genre
    """

    country_key = (country or "nepal").strip().lower()
    if country_key not in ACTOR_POOLS:
        country_key = "nepal"

    budget_tier = budget_data.get("tier", "Medium")
    tier = _tier_key(budget_tier)

    pool = ACTOR_POOLS[country_key][tier]

    characters = parsed_data.get("characters", [])
    primary_genre = (genre_data or {}).get("primary", "drama")

    # Determine top 2 leads by dialogue count
    sorted_chars = sorted(characters, key=lambda c: c.get("dialogue_count", 0), reverse=True)
    leads = sorted_chars[:2] if sorted_chars else []

    suggestions: List[Dict[str, Any]] = []

    # Archetype logic (simple)
    archetype = "Lead"
    if primary_genre in ["action", "thriller", "crime"]:
        archetype = "Strong Lead"
    elif primary_genre in ["romance"]:
        archetype = "Romantic Lead"
    elif primary_genre in ["comedy"]:
        archetype = "Comic Lead"
    elif primary_genre in ["horror"]:
        archetype = "Horror Lead"

    # Build suggestions
    for idx, actor_name in enumerate(pool[:6]):
        fit = 0.6

        # Higher fit for larger budgets (assume star power possible)
        if tier == "high":
            fit += 0.15
        elif tier == "low":
            fit -= 0.05

        # Genre factor
        if primary_genre in ["action", "thriller", "crime"] and tier in ["medium", "high"]:
            fit += 0.05

        # Lead availability factor: if script has very dominant main character
        if leads:
            lead_dialogue = leads[0].get("dialogue_count", 0)
            total_dialogue = sum([c.get("dialogue_count", 0) for c in characters]) or 1
            dominance = lead_dialogue / total_dialogue
            if dominance > 0.45:
                fit += 0.05  # strong lead-driven script

        fit = max(0.35, min(0.92, fit))

        suggestions.append({
            "name": actor_name,
            "country": country_key,
            "budget_tier": tier,
            "recommended_for": archetype,
            "fit_score": round(fit, 4),
            "notes": f"Suggested from {country_key.upper()} {tier.upper()} pool for {primary_genre.upper()} tone"
        })

    # Also return lead role names for UI
    lead_roles = [{"name": c.get("name"), "dialogue_count": c.get("dialogue_count", 0)} for c in leads]

    return [
        {
            "type": "casting_suggestions",
            "country": country_key,
            "budget_tier": tier,
            "genre": primary_genre,
            "lead_roles_detected": lead_roles,
            "suggestions": suggestions
        }
    ]
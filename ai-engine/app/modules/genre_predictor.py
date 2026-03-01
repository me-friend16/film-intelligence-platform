import re
from typing import Dict, Any, List, Tuple


# Keyword banks (hybrid starter - fast & explainable)
GENRE_KEYWORDS = {
    "action": [
        "fight", "chase", "explosion", "gun", "shoot", "attack", "car crash", "knife",
        "blood", "hostage", "battle", "punch", "kick", "bomb"
    ],
    "thriller": [
        "mystery", "suspect", "killer", "investigate", "evidence", "secret", "threat",
        "escape", "stalk", "surveillance", "kidnap", "blackmail"
    ],
    "horror": [
        "ghost", "haunted", "demon", "curse", "scream", "monster", "evil spirit",
        "possession", "grave", "dark ritual"
    ],
    "romance": [
        "love", "kiss", "date", "relationship", "heart", "wedding", "breakup", "crush",
        "romantic"
    ],
    "comedy": [
        "funny", "joke", "laugh", "comic", "hilarious", "prank", "ridiculous", "awkward"
    ],
    "drama": [
        "family", "mother", "father", "tears", "struggle", "life", "dream", "conflict",
        "sacrifice", "regret", "betrayal"
    ],
    "crime": [
        "police", "cop", "gang", "mafia", "drug", "robbery", "murder", "court", "trial",
        "detective"
    ],
    "sci-fi": [
        "alien", "spaceship", "space", "future", "time travel", "robot", "ai", "android",
        "planet"
    ],
    "fantasy": [
        "magic", "kingdom", "sword", "prophecy", "wizard", "dragon", "myth", "curse"
    ],
}


def _normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text


def _score_genres(text: str) -> List[Tuple[str, float, List[str]]]:
    """
    Returns list of (genre, score, matched_keywords)
    score is normalized 0..1 based on keyword hits
    """
    t = _normalize(text)
    results = []

    for genre, kws in GENRE_KEYWORDS.items():
        hits = []
        score = 0
        for kw in kws:
            if kw in t:
                hits.append(kw)
                score += 1

        # Normalize (cap at 1.0)
        norm = min(1.0, score / max(6, len(kws) * 0.25))  # easier to hit a strong score
        if score > 0:
            results.append((genre, norm, hits))

    results.sort(key=lambda x: x[1], reverse=True)
    return results


def predict_genre(text: str) -> Dict[str, Any]:
    """
    Hybrid Genre Predictor:
    - Stage 1 (now): keyword-scoring (fast)
    - Stage 2 (later): ML model hook (TF-IDF classifier)
    """
    scored = _score_genres(text)

    if not scored:
        return {
            "primary": "drama",
            "confidence": 0.35,
            "secondary": [],
            "signals": [],
            "method": "keyword_heuristic"
        }

    primary, conf, hits = scored[0]
    secondary = [g for g, s, _ in scored[1:4] if s >= 0.25 and g != primary]

    # Confidence shaping (keep realistic)
    confidence = max(0.35, min(0.92, float(conf)))

    # Provide explainability signals
    signals = [{"genre": primary, "matched_keywords": hits[:12]}]
    for g, s, h in scored[1:3]:
        signals.append({"genre": g, "matched_keywords": h[:10]})

    return {
        "primary": primary,
        "confidence": round(confidence, 4),
        "secondary": secondary,
        "signals": signals,
        "method": "keyword_heuristic"
    }
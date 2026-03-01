import re
from typing import Dict, Any, List

# Lightweight sentiment lexicon (fast, no heavy libs)
POS_WORDS = {
    "love","happy","joy","smile","hope","brave","calm","success","win","laugh","beautiful",
    "safe","trust","friend","peace","excited","proud","relief","promise","good"
}

NEG_WORDS = {
    "hate","sad","anger","cry","fear","kill","dead","death","blood","gun","fight","panic",
    "hurt","pain","betray","loss","alone","danger","threat","bad","evil","terrified"
}

INTENSIFIERS = {"very","extremely","so","too","really","highly"}
NEGATORS = {"not","never","no","without","hardly"}

SCENE_HEADING_RE = re.compile(r"^\s*(INT\.|EXT\.|INT\/EXT\.|I\/E\.)\s+(.+)$", re.IGNORECASE)


def _tokenize(text: str) -> List[str]:
    text = text.lower()
    # keep words only
    return re.findall(r"[a-z']+", text)


def _score_tokens(tokens: List[str]) -> Dict[str, Any]:
    pos = 0
    neg = 0
    intensity = 0.0

    i = 0
    while i < len(tokens):
        w = tokens[i]
        prev = tokens[i - 1] if i > 0 else None
        prev2 = tokens[i - 2] if i > 1 else None

        is_negated = (prev in NEGATORS) or (prev2 in NEGATORS)
        is_intense = (prev in INTENSIFIERS) or (prev2 in INTENSIFIERS)

        if w in POS_WORDS:
            if is_negated:
                neg += 1
            else:
                pos += 1
            if is_intense:
                intensity += 0.5

        elif w in NEG_WORDS:
            if is_negated:
                pos += 1
            else:
                neg += 1
            if is_intense:
                intensity += 0.5

        i += 1

    total = pos + neg
    polarity = 0.0
    if total > 0:
        polarity = (pos - neg) / total  # -1 .. +1

    # Base intensity from total emotional words
    base_intensity = min(1.0, total / 40.0)  # 40 emotional hits = max
    intensity = min(1.0, base_intensity + intensity)

    return {
        "pos_hits": pos,
        "neg_hits": neg,
        "polarity": round(polarity, 4),
        "intensity": round(intensity, 4),
        "emotional_word_hits": total
    }


def analyze_sentiment(script_text: str) -> Dict[str, Any]:
    """
    Lightweight emotional analysis:
    - overall polarity/intensity
    - scene-level emotional arc using scene headings
    """
    lines = script_text.splitlines()

    # Split into scenes by headings (simple)
    scenes = []
    current = {"heading": "UNKNOWN", "text": []}

    for raw in lines:
        line = raw.strip()
        if not line:
            continue

        if SCENE_HEADING_RE.match(line):
            # push previous
            if current["text"]:
                scenes.append(current)
            current = {"heading": line, "text": []}
        else:
            current["text"].append(line)

    if current["text"]:
        scenes.append(current)

    # Overall
    all_tokens = _tokenize(script_text)
    overall = _score_tokens(all_tokens)

    # Scene arc
    arc = []
    for idx, s in enumerate(scenes, start=1):
        scene_text = " ".join(s["text"])
        tokens = _tokenize(scene_text)
        sc = _score_tokens(tokens)
        arc.append({
            "scene_number": idx,
            "heading": s["heading"],
            "polarity": sc["polarity"],
            "intensity": sc["intensity"]
        })

    # Tone label (simple)
    tone = "neutral"
    if overall["polarity"] >= 0.2:
        tone = "positive"
    elif overall["polarity"] <= -0.2:
        tone = "dark"

    return {
        "overall": overall,
        "tone": tone,
        "scene_arc": arc[:200]  # safety limit
    }
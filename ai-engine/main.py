from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import time

from app.modules.parser import parse_script
from app.modules.structure import analyze_structure
from app.modules.sentiment import analyze_sentiment
from app.modules.genre_predictor import predict_genre
from app.modules.audience_predictor import predict_audience
from app.modules.budget_engine import estimate_budget
from app.modules.casting_engine import suggest_casting
from app.modules.risk_engine import analyze_risk

app = FastAPI(title="Film Intelligence AI Engine", version="1.0.0")


@app.get("/health")
def health():
    return {"status": "ok", "engine": "hybrid-v1"}


@app.post("/analyze")
async def analyze(request: Request):
    start = time.time()

    content_type = (request.headers.get("content-type") or "").lower()

    script_id = None
    text = ""

    # ✅ Accept both JSON payload and raw body
    if "application/json" in content_type:
        data = await request.json()
        script_id = data.get("script_id")
        text = (data.get("text") or "")
    else:
        body = await request.body()
        text = body.decode("utf-8", errors="ignore")

    parsed_data = parse_script(text)
    structure_metrics = analyze_structure(parsed_data)
    sentiment_data = analyze_sentiment(text)
    genre_data = predict_genre(text)
    audience_data = predict_audience(text, genre_data)
    budget_data = estimate_budget(parsed_data, genre_data)
    casting_data = suggest_casting(parsed_data, genre_data, budget_data)
    risk_data = analyze_risk(parsed_data, structure_metrics)

    result = {
        "script_id": script_id,
        "processing_time_ms": int((time.time() - start) * 1000),

        "structural_metrics": structure_metrics,
        "continuity_issues": [],

        "characters": parsed_data.get("characters", []),
        "scenes": parsed_data.get("scenes", []),

        "sentiment_arc": sentiment_data,
        "genre_prediction": genre_data,
        "audience_prediction": audience_data,
        "budget_estimate": budget_data,
        "actor_suggestions": casting_data,
        "production_risk_flags": risk_data,
    }

    return JSONResponse(result)
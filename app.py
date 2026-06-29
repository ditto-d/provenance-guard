from datetime import datetime, timezone
import uuid

from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from config import RATE_LIMIT
from detectors.llm_detector import llm_signal
from detectors.repetition_detector import repetition_signal
from detectors.stylometric_detector import stylometric_signal
from services.appeals import submit_appeal
from services.audit import get_audit_log, log_submission
from services.confidence import combine_scores, determine_classification
from services.transparency import get_transparency_label


app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[],
    storage_uri="memory://",
)


# Home

@app.route("/")
def home():
    return jsonify({
        "message": "Provenance Guard API",
        "status": "running"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


# Submit Content

@app.route("/submit", methods=["POST"])
@limiter.limit(RATE_LIMIT)
def submit():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Missing JSON body."
        }), 400

    creator_id = data.get("creator_id")
    text = data.get("text")

    if not creator_id or not text:
        return jsonify({
            "error": "creator_id and text are required."
        }), 400

    content_id = str(uuid.uuid4())

    # Detection Pipeline

    llm_result = llm_signal(text)

    stylometric_score = stylometric_signal(text)

    repetition_score = repetition_signal(text)

    if llm_result["classification"] == "likely_ai":
        llm_score = llm_result["score"]
    else:
        llm_score = 1 - llm_result["score"]

    confidence = combine_scores(
        llm_score,
        stylometric_score,
        repetition_score
    )

    classification = determine_classification(confidence)

    signals = {
        "llm_classification": llm_result["classification"],
        "llm_confidence": llm_score,
        "stylometric_score": stylometric_score,
        "repetition_score": repetition_score
    }

    transparency_label = get_transparency_label(
        classification,
        confidence
    )

    status = "classified"

    # Console Debug

    print("\n================ PIPELINE ================\n")
    print(f"LLM Classification : {llm_result['classification']}")
    print(f"LLM Confidence     : {llm_score}")
    print(f"Stylometric Score  : {stylometric_score}")
    print(f"Repetition Score   : {repetition_score}")
    print(f"Combined Score     : {confidence}")
    print(f"Final Decision     : {classification}")
    print("\n==========================================\n")

    # Audit Log


    log_submission(
        content_id=content_id,
        creator_id=creator_id,
        classification=classification,
        confidence=confidence,
        signals=signals,
        transparency_label=transparency_label,
        status=status,
    )

    # API Response

    return jsonify({

        "content_id": content_id,

        "attribution": classification,

        "confidence": confidence,

        "confidence_percent": f"{confidence * 100:.1f}%",

        "signals": signals,

        "model": "llama-3.3-70b-versatile",

        "processed_at": datetime.now(timezone.utc).isoformat(),

        "transparency_label": transparency_label,

        "status": status

    })


# Appeal

@app.route("/appeal", methods=["POST"])
def appeal():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Missing JSON body."
        }), 400

    content_id = data.get("content_id")
    creator_reasoning = data.get("creator_reasoning")

    if not content_id or not creator_reasoning:
        return jsonify({
            "error": "content_id and creator_reasoning are required."
        }), 400

    result = submit_appeal(
        content_id,
        creator_reasoning
    )

    if result is None:
        return jsonify({
            "error": "Content not found."
        }), 404

    return jsonify({
        "message": "Appeal received successfully.",
        "status": "under_review",
        "content_id": content_id
    })


# Audit Log

@app.route("/log")
def log():

    return jsonify({
        "entries": get_audit_log()
    })


# Content Lookup

@app.route("/content/<content_id>")
def get_content(content_id):

    return jsonify({
        "message": "Content lookup coming next.",
        "content_id": content_id
    })


# Run


if __name__ == "__main__":
    app.run(debug=True)
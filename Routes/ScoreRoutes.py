from flask import Blueprint, request, jsonify
from Controllers.ScoreController import ScoreController,Score
from flask_jwt_extended import jwt_required, get_jwt_identity
score_bp = Blueprint("score_bp", __name__)

score_controller = ScoreController()

@score_bp.route("/scores", methods=["GET"])
@jwt_required()
def get_scores():
    scores = score_controller.get_scores()
    return jsonify([
        {"key_id": s.key_id, "evidence_id": s.evidence_id, "score": s.score, "scoring_date": str(s.scoring_date)}
        for s in scores
    ])


@score_bp.route("/scores/<int:key_id>/<int:evidence_id>", methods=["GET"])
def get_score(key_id, evidence_id):
    score = score_controller.get_score_by_key_and_evidence(key_id, evidence_id)
    if score:
        return jsonify({
            "key_id": score.key_id, "evidence_id": score.evidence_id,
            "score": score.score, "scoring_date": str(score.scoring_date)
        })
    return jsonify({"error": "Score not found"}), 404


@score_bp.route("/scores", methods=["POST"])
def add_score():
    data = request.json
    key_id = data.get("key_id")
    evidence_id = data.get("evidence_id")
    score_value = data.get("score")

    if not all([key_id, evidence_id, score_value]):
        return jsonify({"error": "Missing required fields"}), 400

    score = score_controller.add_score(key_id, evidence_id, score_value)
    return jsonify({"message": "Score added successfully", "score_id": [score.key_id, score.evidence_id]}), 201

@score_bp.route("/scores/<int:key_id>/<int:evidence_id>", methods=["PUT"])
def update_score(key_id, evidence_id):
    data = request.json
    new_score = data.get("score")

    score = score_controller.update_score(key_id, evidence_id, new_score)
    if score:
        return jsonify({"message": "Score updated successfully"})
    return jsonify({"error": "Score not found"}), 404

@score_bp.route("/scores/<int:key_id>/<int:evidence_id>", methods=["DELETE"])
def delete_score(key_id, evidence_id):
    score = score_controller.delete_score(key_id, evidence_id)
    if score:
        return jsonify({"message": "Score deleted successfully"})
    return jsonify({"error": "Score not found"}), 404

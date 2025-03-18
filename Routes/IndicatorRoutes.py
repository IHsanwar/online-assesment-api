from flask import Blueprint, request, jsonify
from Controllers.IndicatorsController import IndicatorController

indicator_bp = Blueprint('indicator', __name__)
controller = IndicatorController()

@indicator_bp.route("/indicators", methods=["GET"])
def get_indicators():
    return jsonify(controller.get_all_indicators())

@indicator_bp.route("/indicators/<int:indicator_id>", methods=["GET"])
def get_indicator(indicator_id):
    indicator = controller.get_indicator_by_id(indicator_id)
    if not indicator:
        return jsonify({"error": "Indicator not found"}), 404
    return jsonify(indicator)

@indicator_bp.route("/indicators", methods=["POST"])
def add_indicator():
    data = request.get_json()
    return jsonify(controller.add_indicator(
        role_id=data["role_id"],
        assessment_tool=data["assessment_tool"],
        description=data.get("description", ""),
        indicator_item=data["indicator_item"]
    ))

@indicator_bp.route("/indicators/<int:indicator_id>", methods=["PUT"])
def update_indicator(indicator_id):
    data = request.get_json()
    return jsonify(controller.update_indicator(
        indicator_id=indicator_id,
        role_id=data["role_id"],
        assessment_tool=data["assessment_tool"],
        description=data.get("description", ""),
        indicator_item=data["indicator_item"]
    ))

@indicator_bp.route("/indicators/<int:indicator_id>", methods=["DELETE"])
def delete_indicator(indicator_id):
    return jsonify(controller.delete_indicator(indicator_id))

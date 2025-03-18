from flask import Blueprint, request, jsonify
from Controllers.CompetencyCategory import CompetencyCategoryController

competency_category_bp = Blueprint('competency_category', __name__)
controller = CompetencyCategoryController()

@competency_category_bp.route("/competency_categories", methods=["GET"])
def get_competency_categories():
    return jsonify(controller.get_all_categories())

@competency_category_bp.route("/competency_categories/<int:category_id>", methods=["GET"])
def get_competency_category(category_id):
    category = controller.get_category_by_id(category_id)
    if not category:
        return jsonify({"error": "Category not found"}), 404
    return jsonify(category)

@competency_category_bp.route("/competency_categories", methods=["POST"])
def add_competency_category():
    data = request.get_json()
    return jsonify(controller.add_category(data["category_name"]))

@competency_category_bp.route("/competency_categories/<int:category_id>", methods=["PUT"])
def update_competency_category(category_id):
    data = request.get_json()
    return jsonify(controller.update_category(category_id, data["category_name"]))

@competency_category_bp.route("/competency_categories/<int:category_id>", methods=["DELETE"])
def delete_competency_category(category_id):
    return jsonify(controller.delete_category(category_id))

from flask import Blueprint, request, jsonify
from Controllers.CompetencyCategory import CompetencyCategoryController
from flask_jwt_extended import jwt_required

competency_category_bp = Blueprint('competency_category', __name__)
controller = CompetencyCategoryController()


@competency_category_bp.route("/competency_categories", methods=["GET"])
@jwt_required() 
def get_competency_categories():
    return jsonify(controller.get_all_categories())

@competency_category_bp.route("/competency_categories/<int:category_id>", methods=["GET"])
def get_competency_category(category_id):
    category = controller.get_category_by_id(category_id)
    if not category:
        return jsonify({"error": "Category not found"}), 404
    return jsonify(category)

@competency_category_bp.route('/competency_categories', methods=['POST'])
def add_category_route():
    data = request.json
    category_name = data.get("category_name")
    description = data.get("description")
    core = data.get("core")

    if not category_name:
        return {"error": "Category name is required"}, 400

    controller = CompetencyCategoryController()
    return controller.add_category(category_name, description, core)

@competency_category_bp.route("/competency_categories/<int:category_id>", methods=["PUT"])
def update_competency_category(category_id):
    data = request.get_json()
    return jsonify(controller.update_category(category_id, data["category_name"]))

@competency_category_bp.route("/competency_categories/<int:category_id>", methods=["DELETE"])
def delete_competency_category(category_id):
    return jsonify(controller.delete_category(category_id))

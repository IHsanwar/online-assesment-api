from flask import Blueprint, request
from Controllers.AssesmentRoleController import AssessmentRoleController   

assessment_role_bp = Blueprint("assessment_role", __name__)

@assessment_role_bp.route("/assessment_roles", methods=["GET"]) 
def get_all_assessment_roles(): 
    return AssessmentRoleController.get_all_assessment_roles()

@assessment_role_bp.route("/assessment_roles/<int:role_id>", methods=["GET"])
def get_assessment_role(role_id):
    return AssessmentRoleController.get_assessment_role(role_id)

@assessment_role_bp.route("/assessment_roles", methods=["POST"])
def add_assessment_role():
    data = request.get_json()
    return AssessmentRoleController.add_assessment_role(data)

@assessment_role_bp.route("/assessment_roles/<int:role_id>", methods=["PUT"])
def update_assessment_role(role_id):
    data = request.get_json()
    return AssessmentRoleController.update_assessment_role(role_id, data)

@assessment_role_bp.route("/assessment_roles/<int:role_id>", methods=["DELETE"])
def delete_assessment_role(role_id):
    return AssessmentRoleController.delete_assessment_role(role_id)

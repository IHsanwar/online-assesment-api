from flask import Blueprint, request, jsonify
from Controllers.CompetencyKeyController import CompetencyKeyController
from sqlalchemy.orm import sessionmaker

competency_key_bp = Blueprint('competency_key', __name__)

@competency_key_bp.route('/competency_keys', methods=['GET'])
def get_competency_key():
    get_competency_keys = CompetencyKeyController.get_competency_keys()
    return get_competency_keys

@competency_key_bp.route("/competency_keys/<int:key_id>", methods=["GET"])
def get_competency_key_by_id(key_id):
    return CompetencyKeyController.get_competency_key(key_id)

@competency_key_bp.route("/competency_keys", methods=["POST"])
def add_competency_key():
    return CompetencyKeyController.add_competency_key()

@competency_key_bp.route("/competency_keys/<int:key_id>", methods=["PUT"])
def update_competency_key(key_id):
    return CompetencyKeyController.update_competency_key(key_id)


@competency_key_bp.route("/competency_keys/<int:key_id>", methods=["DELETE"])
def delete_competency_key(key_id):
    return CompetencyKeyController.delete_competency_key(key_id)
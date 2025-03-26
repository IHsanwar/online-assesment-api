from flask import Blueprint, request, jsonify
from sqlalchemy.orm import sessionmaker
from Controllers.EvidenceController import *

evidence_bp = Blueprint('evidence_bp', __name__)

@evidence_bp.route('/evidences', methods=['GET'])
def get_evidences_route():
    evidences = evidenceController.get_evidences()
    return jsonify(evidences)


@evidence_bp.route('/evidences/<int:id>', methods=['GET'])
def get_evidence_route(id):
    evidence = evidenceController.get_evidence(id)
    if not evidence:
        return jsonify({'error': 'Evidence not found'}), 404
    return jsonify(evidence)


@evidence_bp.route('/evidences', methods=['POST'])
def create_evidence():
    data = request.json
    response = evidenceController.create_evidences(data)
    return jsonify(response)

@evidence_bp.route('/evidences/<int:id>', methods=['PUT'])
def update_evidence(id):
    data = request.json
    response = evidenceController.update_evidences(id, data)
    if not response:
        return jsonify({'error': 'Evidence not found'}), 404
    return jsonify(response)

@evidence_bp.route('/evidences/<int:id>', methods=['DELETE'])
def delete_evidences(id):
    response = evidenceController.delete_evidence(id)
    if not response:
        return jsonify({'error': 'Evidence not found'}), 404
    return jsonify(response)
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from Models.Connection import SessionLocal
from Models.CompetencyKey import CompetencyKey
from Models.CompetencyCategory import CompetencyCategory

class CompetencyKeyController:
    
    def get_competency_keys():
        with SessionLocal() as session:
            keys = session.query(CompetencyKey).all()
            return jsonify([
                {
                    "key_id": key.key_id,
                    "key_code": key.key_code,
                    "competency_name": key.competency_name,
                    "category_id": key.category_id,
                    "category_name": key.category.category_name  # Include category info
                } for key in keys
            ])

    def get_competency_key(key_id):
        with SessionLocal() as session:
            key = session.query(CompetencyKey).filter_by(key_id=key_id).first()
            if not key:
                return jsonify({"error": "Competency Key not found"}), 404

            return jsonify({
                "key_id": key.key_id,
                "key_code": key.key_code,
                "competency_name": key.competency_name,
                "category_id": key.category_id,
                "category_name": key.category.category_name  # Include category info
            })

    def add_competency_key():
        data = request.get_json()
        
        if not data or "key_code" not in data or "competency_name" not in data or "category_id" not in data:
            return jsonify({"error": "Missing required fields"}), 400

        with SessionLocal() as session:
            category = session.query(CompetencyCategory).filter_by(category_id=data["category_id"]).first()
            if not category:
                return jsonify({"error": "Invalid category_id"}), 400

            existing_key = session.query(CompetencyKey).filter_by(key_code=data["key_code"]).first()
            if existing_key:
                return jsonify({"error": "Competency Key code already exists"}), 400

            new_key = CompetencyKey(
                key_code=data["key_code"],
                competency_name=data["competency_name"],
                category_id=data["category_id"]
            )
            session.add(new_key)
            session.commit()

            return jsonify({"message": "Competency Key added successfully"}), 201

    def update_competency_key(key_id):
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        with SessionLocal() as session:
            key = session.query(CompetencyKey).filter_by(key_id=key_id).first()
            if not key:
                return jsonify({"error": "Competency Key not found"}), 404

            key.key_code = data.get("key_code", key.key_code)
            key.competency_name = data.get("competency_name", key.competency_name)

            if "category_id" in data:
                category = session.query(CompetencyCategory).filter_by(category_id=data["category_id"]).first()
                if not category:
                    return jsonify({"error": "Invalid category_id"}), 400
                key.category_id = data["category_id"]

            session.commit()
            return jsonify({"message": "Competency Key updated successfully"})

    def delete_competency_key(key_id):
        with SessionLocal() as session:
            key = session.query(CompetencyKey).filter_by(key_id=key_id).first()
            if not key:
                return jsonify({"error": "Competency Key not found"}), 404

            session.delete(key)
            session.commit()
            return jsonify({"message": "Competency Key deleted successfully"})

from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError
from Models.Connection import SessionLocal
from Models.AssessmentRole import AssessmentRole
from Models.JobFunction import JobFunction

class AssessmentRoleController:
    
    @staticmethod
    def get_all_assessment_roles():
        session = SessionLocal()
        try:
            roles = session.query(AssessmentRole).all()
            result = [
                {
                    "id": role.id,
                    "model": role.model,
                    "function_id": role.function_id,
                    "label": role.label
                }
                for role in roles
            ]
            return jsonify(result)
        except SQLAlchemyError as e:
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

    @staticmethod
    def get_assessment_role(role_id):
        session = SessionLocal()
        try:
            role = session.query(AssessmentRole).filter_by(id=role_id).first()
            if not role:
                return jsonify({"error": "Assessment Role not found"}), 404

            return jsonify({
                "id": role.id,
                "model": role.model,
                "function_id": role.function_id,
                "label": role.label
            })
        except SQLAlchemyError as e:
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

    @staticmethod
    def add_assessment_role(data):
        session = SessionLocal()
        try:
            # Validate function_id exists
            job_function = session.query(JobFunction).filter_by(id=data["function_id"]).first()
            if not job_function:
                return jsonify({"error": "Invalid function_id"}), 400

            new_role = AssessmentRole(
                model=data["model"],
                function_id=data["function_id"],
                label=data.get("label", None)
            )
            session.add(new_role)
            session.commit()

            return jsonify({"message": "Assessment Role added successfully", "id": new_role.id}), 201
        except SQLAlchemyError as e:
            session.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

    @staticmethod
    def update_assessment_role(role_id, data):
        session = SessionLocal()
        try:
            role = session.query(AssessmentRole).filter_by(id=role_id).first()
            if not role:
                return jsonify({"error": "Assessment Role not found"}), 404

            role.model = data.get("model", role.model)
            role.function_id = data.get("function_id", role.function_id)
            role.label = data.get("label", role.label)

            session.commit()
            return jsonify({"message": "Assessment Role updated successfully"})
        except SQLAlchemyError as e:
            session.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

    @staticmethod
    def delete_assessment_role(role_id):
        session = SessionLocal()
        try:
            role = session.query(AssessmentRole).filter_by(id=role_id).first()
            if not role:
                return jsonify({"error": "Assessment Role not found"}), 404

            session.delete(role)
            session.commit()
            return jsonify({"message": "Assessment Role deleted successfully"})
        except SQLAlchemyError as e:
            session.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

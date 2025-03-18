from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError
from Models.Connection import SessionLocal
from Models.Sector import Sector

class SectorController:
    
    @staticmethod
    def get_all_sectors():
        session = SessionLocal()
        try:
            sectors = session.query(Sector).all()
            result = [
                {
                    "id": sector.id,
                    "code": sector.code,
                    "name": sector.name,
                    "description": sector.description
                }
                for sector in sectors
            ]
            return jsonify(result)
        except SQLAlchemyError as e:
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

    @staticmethod
    def get_sector(sector_id):
        session = SessionLocal()
        try:
            sector = session.query(Sector).filter_by(id=sector_id).first()
            if not sector:
                return jsonify({"error": "Sector not found"}), 404

            return jsonify({
                "id": sector.id,
                "code": sector.code,
                "name": sector.name,
                "description": sector.description
            })
        except SQLAlchemyError as e:
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

    @staticmethod
    def add_sector(data):
        session = SessionLocal()
        try:
            new_sector = Sector(
                code=data["code"],
                name=data["name"],
                description=data.get("description", None)
            )
            session.add(new_sector)
            session.commit()

            return jsonify({"message": "Sector added successfully", "id": new_sector.id}), 201
        except SQLAlchemyError as e:
            session.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

    @staticmethod
    def update_sector(sector_id, data):
        session = SessionLocal()
        try:
            sector = session.query(Sector).filter_by(id=sector_id).first()
            if not sector:
                return jsonify({"error": "Sector not found"}), 404

            sector.code = data.get("code", sector.code)
            sector.name = data.get("name", sector.name)
            sector.description = data.get("description", sector.description)

            session.commit()
            return jsonify({"message": "Sector updated successfully"})
        except SQLAlchemyError as e:
            session.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

    @staticmethod
    def delete_sector(sector_id):
        session = SessionLocal()
        try:
            sector = session.query(Sector).filter_by(id=sector_id).first()
            if not sector:
                return jsonify({"error": "Sector not found"}), 404

            session.delete(sector)
            session.commit()
            return jsonify({"message": "Sector deleted successfully"})
        except SQLAlchemyError as e:
            session.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

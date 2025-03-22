from flask import Blueprint, request
from Controllers.SectorController import SectorController
from flask import jsonify 

sector_bp = Blueprint("sector", __name__)



@sector_bp.route("/sectors", methods=["GET"])
def get_all_sectors():
    return SectorController.get_all_sectors()

@sector_bp.route("/sectors/<int:sector_id>", methods=["GET"])
def get_sector(sector_id):
    return SectorController.get_sector(sector_id)

@sector_bp.route("/sectors", methods=["POST"])
def add_sector():
    data = request.get_json()
    return SectorController.add_sector(data)

@sector_bp.route("/sectors/<int:sector_id>", methods=["PUT"])
def update_sector(sector_id):
    data = request.get_json()
    return SectorController.update_sector(sector_id, data)

@sector_bp.route("/sectors/<int:sector_id>", methods=["DELETE"])
def delete_sector(sector_id):
    return SectorController.delete_sector(sector_id)

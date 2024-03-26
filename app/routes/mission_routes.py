from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request

from app.controllers.mission_controller import *

mission = Blueprint("mission_routes", __name__, url_prefix="/mission")


@mission.route("/", methods=["POST"])
@jwt_required()
def create_route():
    user_type = get_jwt_identity()["type"]
    name = request.json.get("name", None)
    device_ids = request.json.get("device_ids", None)
    user_ids = request.json.get("user_ids", None)
    return create(user_type, name, device_ids, user_ids)


@mission.route("/<mission_id>", methods=["GET"])
@jwt_required()
def get_info_route(mission_id):
    user_type = get_jwt_identity()["type"]
    return get_info(user_type, mission_id)


@mission.route("/", methods=["PUT"])
@jwt_required()
def update_route():
    user_type = get_jwt_identity()["type"]
    mission_id = request.json.get("mission_id", None)
    name = request.json.get("name", None)
    device_ids = request.json.get("device_ids", None)
    user_ids = request.json.get("user_ids", None)
    start_date = request.json.get("start_date", None)
    end_date = request.json.get("end_date", None)
    return update(
        user_type, mission_id, name, device_ids, user_ids, start_date, end_date
    )


@mission.route("/status", methods=["PUT"])
@jwt_required()
def status_route():
    user_type = get_jwt_identity()["type"]
    mission_id = request.json.get("mission_id", None)
    command = request.json.get("command", None)
    return change_status(user_type, mission_id, command)

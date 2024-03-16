from flask_jwt_extended import jwt_required
from flask import Blueprint, request

from app.controllers.mission_controller import *

mission = Blueprint("mission_routes", __name__, url_prefix="/mission")


@mission.route("/", methods=["POST"])
@jwt_required()
def create_route():
    name = request.json.get("name", None)
    start_date = request.json.get("start_date", None)
    robot_ids = request.json.get("robot_ids", None)
    user_ids = request.json.get("user_ids", None)
    return create(name, start_date, robot_ids, user_ids)


@mission.route("/<mission_id>", methods=["GET"])
@jwt_required()
def get_info_route(mission_id):
    return get_info(mission_id)

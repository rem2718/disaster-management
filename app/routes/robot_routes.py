from flask_jwt_extended import jwt_required
from flask import Blueprint, request

from app.controllers.robot_controller import *

robot = Blueprint("robot_routes", __name__, url_prefix="/robot")


@robot.route("/", methods=["POST"])
@jwt_required()
def register_route():
    name = request.json.get("name", None)
    mac = request.json.get("mac", None)
    type = request.json.get("type", None)
    return register(name, mac, type)


@robot.route("/deactivate", methods=["PUT"])
@jwt_required()
def deactivate_route():
    robot_id = request.json.get("robot_id", None)
    return deactivate(robot_id)

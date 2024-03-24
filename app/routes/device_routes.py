from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request

from app.controllers.device_controller import *

device = Blueprint("device_routes", __name__, url_prefix="/device")


@device.route("/", methods=["POST"])
@jwt_required()
def register_route():
    user_type = get_jwt_identity()["type"]
    name = request.json.get("name", None)
    mac = request.json.get("mac", None)
    type = request.json.get("type", None)
    return register(user_type, name, mac, type)


# check brokers
# list of users
# list of robots (name is unique)
# list of missions (name is unique)
# update mission
# get mission list users (admin) for mission
# list of missions


@device.route("/deactivate", methods=["PUT"])
@jwt_required()
def deactivate_route():
    user_type = get_jwt_identity()["type"]
    device_id = request.json.get("device_id", None)
    return deactivate(user_type, device_id)

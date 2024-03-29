from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request

from app.controllers.device_controller import *

DEF_PAGE_NUM = 1
DEF_PAGE_SIZE = 5

device = Blueprint("device_routes", __name__, url_prefix="/device")


@device.route("/", methods=["POST"])
@jwt_required()
def register_route():
    user_type = get_jwt_identity()["type"]
    name = request.json.get("name", None)
    mac = request.json.get("mac", None)
    type = request.json.get("type", None)
    return register(user_type, name, mac, type)


@device.route("/<device_id>", methods=["GET"])
@jwt_required()
def get_info_route(device_id):
    user_type = get_jwt_identity()["type"]
    return get_info(user_type, device_id)


@device.route("/all", methods=["GET"])
@jwt_required()
def get_all_route():
    user_type = get_jwt_identity()["type"]
    page_number = int(request.args.get("page-number"), DEF_PAGE_NUM)
    page_size = int(request.args.get("page-size"), DEF_PAGE_SIZE)
    return get_all(user_type, page_number, page_size)


@device.route("/<device_id>", methods=["PUT"])
@jwt_required
def update_route(device_id):
    user_type = get_jwt_identity()["type"]
    name = request.json.get("name", None)
    mac = request.json.get("mac", None)
    type = request.json.get("type", None)
    return update(user_type, device_id, name, mac, type)


# check brokers
# list of missions (name is unique)


@device.route("/<device_id>", methods=["DELETE"])
@jwt_required()
def deactivate_route(device_id):
    user_type = get_jwt_identity()["type"]
    return deactivate(user_type, device_id)

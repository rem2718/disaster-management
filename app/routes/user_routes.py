from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request

from app.controllers.user_controller import *


DEF_PAGE_NUM = 1
DEF_PAGE_SIZE = 5

user = Blueprint("user_routes", __name__, url_prefix="/api/users")


@user.route("/signup", methods=["POST"])
def signup_route():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    username = request.json.get("username", None)
    return signup(email, password, username)


@user.route("/login", methods=["POST"])
def login_route():
    email_or_username = request.json.get("email_or_username", None)
    password = request.json.get("password", None)
    return login(email_or_username, password)


@user.route("/logout", methods=["POST"])
@jwt_required()
def logout_route():
    user_id = get_jwt_identity()["id"]
    return logout(user_id)


@user.route("/", methods=["GET"])
@jwt_required()
def get_info_route():
    user_id = get_jwt_identity()["id"]
    return get_info(user_id)


@user.route("/<user_id>", methods=["GET"])
@jwt_required()
def get_user_info_route(user_id):
    user_type = get_jwt_identity()["type"]
    return get_user_info(user_type, user_id)


@user.route("/all", methods=["GET"])
@jwt_required()
def get_all_route():
    user_type = get_jwt_identity()["type"]
    page_number = int(request.args.get("page-number", DEF_PAGE_NUM))
    page_size = int(request.args.get("page-size", DEF_PAGE_SIZE))
    
    status_param = request.args.get("status")
    if status_param:
        statuses = [int(status) for status in status_param.split("&")]
    else:
        statuses = None

    type = (
        int(request.args.get("type")) if request.args.get("type") is not None else None
    )
    mission_id = (
        request.args.get("mission") if request.args.get("mission") is not None else None
    )
    return get_all(user_type, page_number, page_size, statuses, type, mission_id)


@user.route("/cur_missions", methods=["GET"])
@jwt_required()
def get_cur_missions_route():
    user_id = get_jwt_identity()["id"]
    return get_cur_missions(user_id)


@user.route("/<user_id>/approval", methods=["PUT"])
@jwt_required()
def approval_route(user_id):
    user_type = get_jwt_identity()["type"]
    approved = request.json.get("approved", None)
    type = request.json.get("type", UserType.REGULAR.value)
    return user_approval(user_type, user_id, approved, type)


@user.route("/", methods=["PUT"])
@jwt_required()
def update_info_route():
    user_id = get_jwt_identity()["id"]
    username = request.json.get("username", None)
    email = request.json.get("email", None)
    return update_info(user_id, username, email)


@user.route("/password", methods=["PUT"])
@jwt_required()
def update_password_route():
    user_id = get_jwt_identity()["id"]
    old_password = request.json.get("old_password", None)
    new_password = request.json.get("new_password", None)
    return update_password(user_id, old_password, new_password)


@user.route("/<user_id>", methods=["DELETE"])
@jwt_required()
def delete_user_route(user_id):
    user_type = get_jwt_identity()["type"]
    return delete_user(user_type, user_id)

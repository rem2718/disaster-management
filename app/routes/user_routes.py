from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request

from app.controllers.user_controller import *

user = Blueprint("user_routes", __name__, url_prefix="/user")


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
    user_id = get_jwt_identity()
    return get_info(user_id)


@user.route("/cur_missions", methods=["GET"])
@jwt_required()
def get_cur_missions_route():
    user_id = get_jwt_identity()["id"]
    return get_cur_missions(user_id)


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

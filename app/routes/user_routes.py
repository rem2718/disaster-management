from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request

from app.controllers.user_controller import signup, login, logout

user = Blueprint("user_routes", __name__)


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

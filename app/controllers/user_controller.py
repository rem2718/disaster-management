from bson import ObjectId

from mongoengine.queryset.visitor import Q
from flask import jsonify

from app.models.mission_model import Mission
from app.models.user_model import User
from app.utils.enums import Status
from app.utils.extensions import *
from app.utils.validators import *

MIN_LENGTH = 3
MAX_LENGTH = 20


@handle_exceptions
def signup(email, password, username):
    existing_user = User.objects(
        (Q(email=email) | Q(username=username)) & Q(status__ne=Status.INACTIVE)
    ).first()
    if existing_user:
        return err_res(409, "Email or Username is already taken.")

    minlength_validator("Username", username, MIN_LENGTH)
    maxlength_validator("Username", username, MAX_LENGTH)
    password_validator(password)

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    user = User(email=email, password=hashed_password, username=username)
    user.save()
    # create mqtt creds for the user
    token = user.generate_token()
    data = {
        "message": "User created successfully. Use the same credentials to establish a connection with the Cloud MQTT broker.",
        "user_id": str(user.id),
        "type": user.type.value,
        "token": token,
    }
    return jsonify(data), 201


@handle_exceptions
def login(email_or_username, password):
    null_validator("Email or Username", email_or_username)
    null_validator("Password", password)

    if User.is_email(email_or_username):
        user = User.objects(email=email_or_username).first()
    else:
        user = User.objects(username=email_or_username).first()

    if not user or not user.check_password(password):
        return err_res(401, "Invalid email or password.")

    token = user.generate_token()
    data = {
        "message": f"User {user.username} loggedin successfully.",
        "username": user.username,
        "token": token,
    }
    return jsonify(data), 200


@handle_exceptions
def logout(user_id):
    if not user_id:
        return err_res(400, "Invalid token")

    User.objects.get(id=user_id)
    return jsonify({"message": "User logged out successfully.", "token": ""}), 200


@handle_exceptions
def get_info(user_id):
    if not user_id:
        return err_res(400, "Invalid token")

    user = User.objects.get(id=user_id)
    data = {
        "user_id": str(user.id),
        "email": user.email,
        "username": user.username,
    }
    return jsonify(data), 200


@authorize_admin
@handle_exceptions
def get_user_info(user_type, user_id):
    null_validator("User ID", user_id)
    user = User.objects.get(id=user_id)
    data = {
        "user_id": str(user.id),
        "email": user.email,
        "username": user.username,
        "type": user.type,
        "status": user.status,
    }
    return jsonify(data), 200


@authorize_admin
@handle_exceptions
def get_all(user_type, page_number, page_size):
    offset = (page_number - 1) * page_size
    users = User.objects.skip(offset).limit(page_size)
    data = [{"id": str(user.id), "username": user.username} for user in users]
    return jsonify(data), 200


@handle_exceptions
def get_cur_missions(user_id):
    if not user_id:
        return err_res(400, "Invalid token")

    user = User.objects.get(id=user_id)
    missions = [
        {
            "mission_id": str(mission._id),
            "name": mission.name,
            "status": mission.status.value,
        }
        for mission in user.cur_missions
    ]
    data = {"cur_missions": missions}
    return jsonify(data), 200


@handle_exceptions
def update_info(user_id, username, email):
    if not user_id:
        return err_res(400, "Invalid token")

    user = User.objects.get(id=user_id)

    if username:
        if user.username != username:
            existing_user = User.objects(username=username).first()
            if existing_user:
                return err_res(409, "Username is already taken.")
        else:
            return err_res(
                409, "The username provided is identical to the current one."
            )

        minlength_validator("Username", username, MIN_LENGTH)
        maxlength_validator("Username", username, MAX_LENGTH)
        user.username = username

    if email:
        if user.email != email:
            existing_user = User.objects(email=email).first()
            if existing_user:
                return err_res(409, "Email is already taken.")
        else:
            return err_res(409, "The email provided is identical to the current one.")
        user.email = email

    user.save()
    data = {
        "message": "User information is updated successfully.",
        "email": user.email,
        "username": user.username,
    }
    return jsonify(data), 200


@handle_exceptions
def update_password(user_id, old_password, new_password):
    if not user_id:
        return err_res(400, "Invalid token")

    null_validator("Old password", old_password)
    null_validator("New password", new_password)

    if old_password == new_password:
        return err_res(409, "The new password is identical to the current one.")

    user = User.objects.get(id=user_id)

    if not user.check_password(old_password):
        return err_res(401, "Incorrect old password try again.")

    password_validator(new_password)

    user.password = bcrypt.generate_password_hash(new_password).decode("utf-8")
    user.save()
    return jsonify({"message": "Password is updated successfully."}), 200


@authorize_admin
@handle_exceptions
def delete_user(user_type, user_id):
    user = User.objects.get(id=user_id)
    if user.status == Status.INACTIVE:
        return err_res(409, "User is already Inactive.")

    for mission in user.cur_missions:
        Mission.objects(id=mission._id).update_one(pull__user_ids=ObjectId(user_id))

    User.objects(id=user_id).update(set__cur_missions=[], set__status=Status.INACTIVE)
    # delete mqtt creds for that user
    return jsonify({"message": "User is deleted successfully."}), 200

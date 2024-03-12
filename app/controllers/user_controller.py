from mongoengine.queryset.visitor import Q
from flask import jsonify

from app.models.user_model import User
from app.utils.extensions import bcrypt


def signup(email, password, username):
    try:
        existing_user = User.objects(Q(email=email) | Q(username=username)).first()
        if existing_user:
            err = "Conflict"
            msg = "Email or Username is already taken."
            return jsonify({"error": err, "message": msg}), 409

        if not User.validate_password(password):
            err = "Bad Request"
            msg = "Password should contain at least 8 characters, including at least one uppercase letter, one lowercase letter, one digit, and one special character."
            return jsonify({"error": err, "message": msg}), 400

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        user = User(email=email, password=hashed_password, username=username)
        user.save()
        msg = "User created successfully."
        return jsonify({"message": msg, "user_id": str(user.id)}), 201

    except Exception as e:
        err = "Internal Server Error"
        msg = str(e)
        return jsonify({"error": err, "message": msg}), 500


def login(email_or_username, password):
    try:
        if not email_or_username:
            err = "Bad Request"
            msg = "Email or Username is required."
            return jsonify({"error": err, "message": msg}), 400

        if not password:
            err = "Bad Request"
            msg = "Password is required."
            return jsonify({"error": err, "message": msg}), 400

        if User.is_email(email_or_username):
            user = User.objects(email=email_or_username).first()
        else:
            user = User.objects(username=email_or_username).first()
        if not user:
            err = "Unauthorized Error"
            msg = "Invalid email or password."
            return jsonify({"error": err, "message": msg}), 401

        if not user.check_password(password):
            err = "Unauthorized Error"
            msg = "Invalid email or password."
            return jsonify({"error": err, "message": msg}), 401

        token = user.generate_token()
        msg = f"User {user.username} loggedin successfully."
        return jsonify({"message": msg, "token": token}), 200

    except Exception as e:
        err = "Internal Server Error"
        msg = str(e)
        return jsonify({"error": err, "message": msg}), 500


def logout(user_id):
    try:
        if not user_id:
            err = "Bad Request"
            msg = "Invalid token"
            return jsonify({"error": err, "message": msg}), 400
        
        user = User.objects.get(id=user_id)
        if not user:
            err = "Not Found Error"
            msg = "User not found."
            return jsonify({"error": err, "message": msg}), 404

        msg = "User logged out successfully."
        return jsonify({"message": msg, "token": ""}), 200

    except Exception as e:
        err = "Internal Server Error"
        msg = str(e)
        return jsonify({"error": err, "message": msg}), 500

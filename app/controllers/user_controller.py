from mongoengine.errors import DoesNotExist, ValidationError
from mongoengine.queryset.visitor import Q
from flask import jsonify

from app.utils.extensions import bcrypt, err_res
from app.models.user_model import User


def signup(email, password, username):
    try:
        existing_user = User.objects(Q(email=email) | Q(username=username)).first()
        if existing_user:
            return err_res(409, "Email or Username is already taken.")

        if not User.validate_password(password):
            msg = "Password should contain at least 8 characters, including at least one uppercase letter, one lowercase letter, one digit, and one special character."
            return err_res(400, msg)

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        user = User(email=email, password=hashed_password, username=username)
        user.save()
        token = user.generate_token()
        data = {
            "message": "User created successfully.",
            "user_id": str(user.id),
            "token": token,
        }
        return jsonify(data), 201

    except ValidationError as ve:
        return err_res(400, str(ve.message))

    except Exception as e:
        return err_res(500, str(e))


def login(email_or_username, password):
    try:
        if not email_or_username:
            return err_res(400, "Email or Username is required.")

        if not password:
            return err_res(400, "Password is required.")

        if User.is_email(email_or_username):
            user = User.objects(email=email_or_username).first()
        else:
            user = User.objects(username=email_or_username).first()

        if not user or not user.check_password(password):
            return err_res(401, "Invalid email or password.")

        token = user.generate_token()
        data = {
            "message": f"User {user.username} loggedin successfully.",
            "token": token,
        }
        return jsonify(data), 200

    except Exception as e:
        return err_res(500, str(e))


def logout(user_id):
    try:
        if not user_id:
            return err_res(400, "Invalid token")

        User.objects.get(id=user_id)
        return jsonify({"message": "User logged out successfully.", "token": ""}), 200

    except DoesNotExist:
        return err_res(404, "User not found.")

    except Exception as e:
        return err_res(500, str(e))


def get_info(user_id):
    try:
        if not user_id:
            return err_res(400, "Invalid token")

        user = User.objects.get(id=user_id)
        data = {
            "user_id": str(user.id),
            "email": user.email,
            "username": user.username,
        }
        return jsonify(data), 200

    except DoesNotExist:
        return err_res(404, "User not found.")

    except Exception as e:
        return err_res(500, str(e))


def get_cur_missions(user_id):
    try:
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

    except DoesNotExist:
        return err_res(404, "User not found.")

    except Exception as e:
        return err_res(500, str(e))


def update_info(user_id, username, email):
    try:
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
            user.username = username

        if email:
            if user.email != email:
                existing_user = User.objects(email=email).first()
                if existing_user:
                    return err_res(409, "Email is already taken.")
            else:
                return err_res(
                    409, "The email provided is identical to the current one."
                )
            user.email = email

        user.save()
        data = {
            "message": "User information is updated successfully.",
            "email": user.email,
            "username": user.username,
        }
        return jsonify(data), 200

    except ValidationError as ve:
        return err_res(400, str(ve))

    except DoesNotExist:
        return err_res(404, "User not found.")

    except Exception as e:
        return err_res(500, str(e))


def update_password(user_id, old_password, new_password):
    try:
        if not user_id:
            return err_res(400, "Invalid token")

        if old_password == None or new_password == None:
            return err_res(400, "No password is provided.")

        if old_password == new_password:
            return err_res(409, "The new password is identical to the current one.")

        user = User.objects.get(id=user_id)

        if not user.check_password(old_password):
            return err_res(401, "Incorrect old password try again.")

        if not User.validate_password(new_password):
            msg = "Password should contain at least 8 characters, including at least one uppercase letter, one lowercase letter, one digit, and one special character."
            return err_res(400, msg)

        user.password = bcrypt.generate_password_hash(new_password).decode("utf-8")
        user.save()
        return jsonify({"message": "Password is updated successfully."}), 200

    except DoesNotExist:
        return err_res(404, "User not found.")

    except Exception as e:
        return err_res(500, str(e))

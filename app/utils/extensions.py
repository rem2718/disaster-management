from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask import jsonify

db = MongoEngine()
bcrypt = Bcrypt()
jwt = JWTManager()


def err_res(code, data):
    match code:
        case 400:
            err = "Bad Request"
        case 401:
            err = "Unauthorized Error"
        case 404:
            err = "Not Found Error"
        case 409:
            err = "Conflict"
        case 500:
            err = "Internal Server Error"

    return jsonify({"error": err, "message": data}), code
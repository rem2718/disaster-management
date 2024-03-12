from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

db = MongoEngine()
bcrypt = Bcrypt()
jwt = JWTManager()

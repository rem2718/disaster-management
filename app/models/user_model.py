from datetime import timedelta
import re

from flask_jwt_extended import create_access_token

from app.utils.enums import UserType, Status
from app.utils.extensions import db, bcrypt


class User(db.Document):
    email = db.EmailField(required=True)
    password = db.StringField(required=True)
    username = db.StringField(required=True)
    type = db.EnumField(UserType, default=UserType.Regular)
    status = db.EnumField(Status, default=Status.Active)
    meta = {"collection": "Users"}

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def generate_token(self):
        ident = {"id": str(self.id)}
        return create_access_token(identity=ident, expires_delta=timedelta(hours=24))

    @staticmethod
    def validate_password(password):
        if (
            len(password) < 8
            or not any(char.isupper() for char in password)
            or not any(char.islower() for char in password)
            or not any(char.isdigit() for char in password)
            or not any(char in "!@#$%^&*()-_+=<>,.?/:;{}[]~" for char in password)
        ):
            return False
        return True

    @staticmethod
    def is_email(string):
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(email_pattern, string) is not None

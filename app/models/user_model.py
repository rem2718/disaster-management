from datetime import timedelta
import re

from flask_jwt_extended import create_access_token
from mongoengine import EmbeddedDocumentField

from app.utils.enums import UserType, Status, MissionStatus
from app.utils.extensions import db, bcrypt


class cur_mission(db.EmbeddedDocument):
    _id = db.ObjectIdField(default=None)
    name = db.StringField()
    status = db.EnumField(MissionStatus, default=MissionStatus.CREATED)
    meta = {"collection": "cur_missions"}


class User(db.Document):
    email = db.EmailField(required=True)
    password = db.StringField(required=True)
    username = db.StringField(required=True)
    type = db.EnumField(UserType, default=UserType.REGULAR)
    status = db.EnumField(Status, default=Status.ACTIVE)
    cur_missions = db.ListField(
        EmbeddedDocumentField(cur_mission), required=False, default=[]
    )

    meta = {"collection": "Users"}

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def generate_token(self):
        ident = {"id": str(self.id), "type": self.type.value}
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

    @staticmethod
    def is_admin(type):
        return type == UserType.ADMIN.value

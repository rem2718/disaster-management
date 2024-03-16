from app.utils.enums import RobotType, Status
from app.utils.extensions import db


class Robot(db.Document):
    name = db.StringField(required=True)
    mac = db.StringField(required=True)
    type = db.EnumField(RobotType, default=RobotType.UGV)
    status = db.EnumField(Status, default=Status.ACTIVE)
    meta = {"collection": "Robots"}

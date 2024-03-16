from datetime import datetime

from app.utils.enums import MissionStatus
from app.models.robot_model import Robot
from app.models.user_model import User
from app.utils.extensions import db


class Mission(db.Document):
    name = db.StringField(default="Mission")
    start_date = db.DateTimeField(default=datetime.now())
    end_date = db.DateTimeField(default=None)
    status = db.EnumField(MissionStatus, default=MissionStatus.CREATED)
    robot_ids = db.ListField(db.ReferenceField(Robot), default=[])
    user_ids = db.ListField(db.ReferenceField(User), default=[])
    meta = {"collection": "Missions"}

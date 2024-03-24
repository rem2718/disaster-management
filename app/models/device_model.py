from app.utils.enums import DeviceType, Status
from app.utils.extensions import db


class Device(db.Document):
    name = db.StringField(required=True)
    mac = db.StringField(required=True)
    type = db.EnumField(DeviceType, default=DeviceType.UGV)
    status = db.EnumField(Status, default=Status.ACTIVE)
    meta = {"collection": "Devices"}

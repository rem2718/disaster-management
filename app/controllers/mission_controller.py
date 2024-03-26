from datetime import datetime

from flask import jsonify

from app.utils.enums import MissionStatus, MissionCommand
from app.models.user_model import User, cur_mission
from app.models.mission_model import Mission
from app.models.device_model import Device
from app.utils.validators import *
from app.utils.extensions import *


# update user, robot status
@authorize_admin
@handle_exceptions
def create(user_type, name, device_ids, user_ids):
    existing_mission = Mission.objects(name=name).first()
    if existing_mission:
        return err_res(409, "Mission name is already taken.")

    minlength_validator("Name", name, 3)
    maxlength_validator("Name", name, 20)
    device_validator(device_ids)
    user_validator(user_ids)

    mission = Mission(name=name, device_ids=device_ids, user_ids=user_ids)
    mission.save()

    for user_id in user_ids:
        user = User.objects.get(id=user_id)
        user.cur_missions.append(
            cur_mission(_id=mission.id, name=mission.name, status=mission.status)
        )
        user.save()

    data = {
        "message": "Mission created successfully.",
        "mission_id": str(mission.id),
    }
    return jsonify(data), 201


@handle_exceptions
def get_info(user_type, mission_id):
    mission = Mission.objects.get(id=mission_id)
    devices = []
    for r in mission.device_ids:
        device = Device.objects.get(id=str(r.id))
        devices.append(
            {"id": str(device.id), "name": device.name, "type": device.type.value}
        )

    data = {
        "id": str(mission.id),
        "name": mission.name,
        "start_date": mission.start_date,
        "end_date": mission.end_date,
        "status": mission.status.value,
        "devices": devices,
    }

    if user_type == UserType.ADMIN.value:
        users = []
        for r in mission.user_ids:
            user = User.objects.get(id=str(r.id))
            users.append({"id": str(user.id), "username": user.username})
        data["users"] = users

    return jsonify(data), 200


@authorize_admin
@handle_exceptions
def update(user_type, mission_id, name, device_ids, user_ids, start_date, end_date):
    mission = Mission.objects.get(id=mission_id)
    if name:
        minlength_validator("Name", name, 3)
        maxlength_validator("Name", name, 20)
        mission.name = name

    if device_ids:
        device_validator(device_ids)
        mission.device_ids = device_ids

    if user_ids:
        user_validator(user_ids)
        mission.user_ids = user_ids

    if start_date:
        mission.start_date = start_date

    if end_date:
        mission.end_date = end_date

    date_validator(mission.start_date, mission.end_date, mission.status)
    mission.save()


@authorize_admin
@handle_exceptions
def change_status(user_type, mission_id, status):
    mission = Mission.objects.get(id=mission_id)
    enum_validator("Mission command", status, MissionCommand)

    match status:
        case MissionCommand.START.value:
            mission.status = MissionStatus.ONGOING.value
            mission.start_date = datetime.now()
        case MissionCommand.PAUSE.value:
            mission.status = MissionStatus.PAUSED.value
        case MissionCommand.CONTINUE.value:
            mission.status = MissionStatus.ONGOING.value
        case MissionCommand.CANCEL.value:
            mission.status = MissionStatus.CANCELED.value
            mission.end_date = datetime.now()
        case MissionCommand.END.value:
            mission.status = MissionStatus.FINISHED.value
            mission.end_date = datetime.now()

    mission.save()

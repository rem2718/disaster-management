from datetime import datetime

from mongoengine.errors import DoesNotExist, ValidationError
from flask import jsonify

from app.models.user_model import User, cur_mission
from app.models.mission_model import Mission
from app.models.device_model import Device
from app.utils.extensions import err_res
from app.utils.enums import MissionStatus, MissionCommand


def create(user_type, name, device_ids, user_ids):
    try:
        if not User.is_admin(user_type):
            return err_res(401, "Admin access is required.")

        existing_mission = User.objects(name=name).first()
        if existing_mission:
            return err_res(409, "Mission name is already taken.")

        for device_id in device_ids:
            try:
                Device.objects.get(id=device_id)
            except DoesNotExist:
                return err_res(404, f"Invalid device ID, '{device_id}' doesn't exist")
        for user_id in user_ids:
            try:
                user = User.objects.get(id=user_id)
            except DoesNotExist:
                return err_res(404, f"Invalid user ID, '{user_id}' doesn't exist")

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

    except ValidationError as ve:
        return err_res(400, str(ve))

    except Exception as e:
        return err_res(500, str(e))


def get_info(mission_id):
    try:
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
        return jsonify(data), 200

    except DoesNotExist:
        return err_res(404, "Mission not found.")

    except Exception as e:
        return err_res(500, str(e))


def update(user_type, mission_id, name, device_ids, user_ids, start_date, end_date):
    try:
        if not User.is_admin(user_type):
            return err_res(401, "Admin access is required.")

        mission = Mission.objects.get(id=mission_id)
        mission.name = name
        mission.device_ids = device_ids
        mission.user_ids = user_ids
        mission.start_date = start_date
        mission.end_date = end_date

        mission.save()

    except DoesNotExist:
        return err_res(404, "Mission not found.")

    except Exception as e:
        return err_res(500, str(e))


def change_status(user_type, mission_id, status):
    try:
        if not User.is_admin(user_type):
            return err_res(401, "Admin access is required.")

        mission = Mission.objects.get(id=mission_id)
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
            case _:
                return err_res(400, "Invalid Mission Status")

        mission.save()

    except DoesNotExist:
        return err_res(404, "Mission not found.")

    except Exception as e:
        return err_res(500, str(e))

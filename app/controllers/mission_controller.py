from mongoengine.errors import DoesNotExist
from flask import jsonify

from app.models.mission_model import Mission
from app.utils.extensions import err_res
from app.models.robot_model import Robot


def create(name, start_date, robot_ids, user_ids):
    try:
        mission = Mission(
            name=name, start_date=start_date, robot_ids=robot_ids, user_ids=user_ids
        )
        mission.save()
        data = {
            "message": "Mission created successfully.",
            "mission_id": str(mission.id),
        }
        return jsonify(data), 201

    except Exception as e:
        return err_res(500, str(e))


def get_info(mission_id):
    try:
        mission = Mission.objects.get(id=mission_id)
        robots = []
        for robot_id in mission.robot_ids:
            robot = Robot.objects.get(id=robot_id)
            robots.append({"id": str(robot.id), "name": robot.name, "type": robot.type})
        data = {
            "id": str(mission.id),
            "name": mission.name,
            "start_date": mission.start_date,
            "end_date": mission.end_date,
            "status": mission.status,
            "robots": robots,
        }
        return jsonify(data), 200

    except DoesNotExist:
        return err_res(404, "Mission not found.")

    except Exception as e:
        return err_res(500, str(e))

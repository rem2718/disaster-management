from mongoengine.errors import DoesNotExist, ValidationError
from flask import jsonify

from app.models.user_model import User, cur_mission
from app.models.robot_model import Robot
from app.models.mission_model import Mission
from app.utils.extensions import err_res
from app.models.robot_model import Robot

from bson import ObjectId


def create(name, start_date, robot_ids, user_ids):
    try:
        for robot_id in robot_ids:
            try:
                Robot.objects.get(id=robot_id)
            except DoesNotExist:
                return err_res(404, f"Invalid robot ID, {robot_id} robot doesn't exist")
        for user_id in user_ids:
            try:
                user = User.objects.get(id=user_id)
            except DoesNotExist:
                return err_res(404, f"Invalid user ID, {user_id} user doesn't exist")

        mission = Mission(
            name=name, start_date=start_date, robot_ids=robot_ids, user_ids=user_ids
        )
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
        robots = []
        for r in mission.robot_ids:
            robot = Robot.objects.get(id=str(r.id))
            robots.append(
                {"id": str(robot.id), "name": robot.name, "type": robot.type.value}
            )
        data = {
            "id": str(mission.id),
            "name": mission.name,
            "start_date": mission.start_date,
            "end_date": mission.end_date,
            "status": mission.status.value,
            "robots": robots,
        }
        return jsonify(data), 200

    except DoesNotExist:
        return err_res(404, "Mission not found.")

    except Exception as e:
        return err_res(500, str(e))

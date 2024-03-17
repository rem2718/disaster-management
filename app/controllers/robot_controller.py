from mongoengine.errors import DoesNotExist, ValidationError
from flask import jsonify

from app.models.robot_model import Robot
from app.utils.enums import Status
from app.utils.extensions import err_res


def register(name, mac, type):
    try:
        existing_robot = Robot.objects(mac=mac).first()
        if existing_robot:
            return err_res(
                409, "A robot with the same MAC address is already registered."
            )

        robot = Robot(name=name, mac=mac, type=type)
        robot.save()
        data = {"message": "Robot registered successfully.", "robot_id": str(robot.id)}
        return jsonify(data), 201
    
    except ValidationError as ve:
        return err_res(400, str(ve))
    
    except Exception as e:
        return err_res(500, str(e))


def deactivate(robot_id):
    try:
        if not robot_id:
            return err_res(400, "Robot ID is required.")

        robot = Robot.objects.get(id=robot_id)
        robot.status = Status.INACTIVE
        robot.save()
        return jsonify({"message": "Robot is deactivated successfully."}), 200

    except DoesNotExist:
        return err_res(404, "Robot not found.")

    except Exception as e:
        return err_res(500, str(e))

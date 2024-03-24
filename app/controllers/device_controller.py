from mongoengine.errors import DoesNotExist, ValidationError
from mongoengine.queryset.visitor import Q
from flask import jsonify

from app.utils.extensions import err_res
from app.models.device_model import Device
from app.models.user_model import User
from app.utils.enums import Status


def register(user_type, name, mac, type):
    try:
        if not User.is_admin(user_type):
            return err_res(401, "Admin access is required.")

        existing_device = Device.objects(
            (Q(mac=mac) | Q(name=name)) & (Q(status__ne=Status.INACTIVE))
        ).first()
        if existing_device:
            return err_res(
                409, "A device with the same MAC address is already registered."
            )

        device = Device(name=name, mac=mac, type=type)
        device.save()
        data = {"message": "Device registered successfully.", "device_id": str(device.id)}
        return jsonify(data), 201

    except ValidationError as ve:
        return err_res(400, str(ve))

    except Exception as e:
        return err_res(500, str(e))


def deactivate(user_type, device_id):
    try:
        if not User.is_admin(user_type):
            return err_res(401, "Admin access is required.")

        if not device_id:
            return err_res(400, "Device ID is required.")

        device = Device.objects.get(id=device_id)

        if device.status == Status.INACTIVE:
            return err_res(409, "Device is already Inactive.")

        device.status = Status.INACTIVE
        device.save()
        return jsonify({"message": "Device is deactivated successfully."}), 200

    except DoesNotExist:
        return err_res(404, "Device not found.")

    except Exception as e:
        return err_res(500, str(e))

from mongoengine.queryset.visitor import Q
from flask import jsonify

from app.utils.enums import Status, DeviceType
from app.models.device_model import Device
from app.utils.validators import *
from app.utils.extensions import *

MIN_LENGTH = 3
MAX_LENGTH = 20


@authorize_admin
@handle_exceptions
def register(user_type, name, mac, type):
    minlength_validator("Name", name, 3)
    minlength_validator("Name", name, 20)
    mac_validator(mac)
    enum_validator("device", type, DeviceType)

    existing_device = Device.objects(
        (Q(mac=mac) | Q(name=name)) & (Q(status__ne=Status.INACTIVE))
    ).first()
    if existing_device:
        return err_res(409, "A device with the same MAC address is already registered.")

    device = Device(name=name, mac=mac, type=type)
    device.save()
    data = {"message": "Device registered successfully.", "device_id": str(device.id)}
    return jsonify(data), 201


@authorize_admin
@handle_exceptions
def get_info(user_type, device_id):
    null_validator("Device ID", device_id)
    device = Device.objects.get(id=device_id)
    data = {
        "device_id": str(device.id),
        "name": device.namr,
        "mac": device.mac,
        "type": device.type,
        "status": device.status,
    }
    return jsonify(data), 200


@authorize_admin
@handle_exceptions
def get_all(user_type, page_number, page_size):
    offset = (page_number - 1) * page_size
    users = Device.objects.only("id", "name").skip(offset).limit(page_size)
    return jsonify(users), 200


@authorize_admin
@handle_exceptions
def update(user_type, device_id, name, mac, type):
    device = Device.objects.get(id=device_id)

    if name:
        if device.name != name:
            existing_device = Device.objects(username=name).first()
            if existing_device:
                return err_res(409, "Name is already taken.")
        else:
            return err_res(409, "The name provided is identical to the current one.")
        minlength_validator("Name", name, MIN_LENGTH)
        maxlength_validator("Name", name, MAX_LENGTH)
        device.name = name

    if mac:
        if device.mac != mac:
            existing_device = Device.objects(mac=mac).first()
            if existing_device:
                return err_res(409, "MAC Address is already taken.")
        else:
            return err_res(
                409, "The MAC Address provided is identical to the current one."
            )
        mac_validator(mac)
        device.mac = mac

    if type:
        enum_validator("Device Type", type, DeviceType)
        device.type = type

    device.save()
    data = {
        "message": "Device information is updated successfully.",
        "name": device.name,
        "mac": device.mac,
        "type": device.type,
    }
    return jsonify(data), 200


@authorize_admin
@handle_exceptions
def deactivate(user_type, device_id):
    null_validator("Device ID", device_id)
    device = Device.objects.get(id=device_id)
    if device.status == Status.INACTIVE:
        return err_res(409, "Device is already Inactive.")
    # for cur_mission in user.cur_missions:
    #     mission = Mission.objects.get(id=cur_mission.id)
    #     mission.user_ids.remove(user_id)
    # user.cur_missions = []
    device.status = Status.INACTIVE
    device.save()
    return jsonify({"message": "Device is deactivated successfully."}), 200

from bson import ObjectId

from mongoengine.queryset.visitor import Q
from flask import jsonify

from app.utils.enums import Status, DeviceType, MissionStatus
from app.models.mission_model import Mission
from app.models.device_model import Device
from app.utils.validators import *
from app.utils.extensions import *

MIN_LENGTH = 3
MAX_LENGTH = 20


@authorize_admin
@handle_exceptions
def register(user_type, name, mac, type):
    minlength_validator("Name", name, MIN_LENGTH)
    maxlength_validator("Name", name, MAX_LENGTH)
    mac_validator(mac)
    enum_validator("device", type, DeviceType)
    existing_device = Device.objects(
        (Q(mac=mac) | Q(name=name)) & (Q(status__ne=Status.INACTIVE))
    ).first()
    if existing_device:
        return err_res(409, "A device with the same MAC address is already registered.")

    device = Device(name=name, mac=mac, type=type)
    device.save()
    data = {
        "message": "Device is registered successfully.",
        "device_id": str(device.id),
    }
    return jsonify(data), 201


@authorize_admin
@handle_exceptions
def get_info(user_type, device_id):
    null_validator("Device ID", device_id)
    device = Device.objects.get(id=device_id)
    data = {
        "device_id": str(device.id),
        "name": device.name,
        "mac": device.mac,
        "type": device.type,
        "status": device.status,
    }
    return jsonify(data), 200


@authorize_admin
@handle_exceptions
def get_all(user_type, page_number, page_size, status, type, mission_id):
    offset = (page_number - 1) * page_size
    query, data = {}, []

    if status is not None:
        query["status"] = status
    if type is not None:
        query["type"] = type
    devices = Device.objects(**query).skip(offset).limit(page_size)

    if mission_id is not None:
        mission_devs = []
        mission = Mission.objects.get(id=mission_id)
        for dev in mission.device_ids:
            mission_devs.append(str(dev.id))
            device = Device.objects.get(id=str(dev.id))
            data.append({"id": str(device.id), "name": device.name, "in_mission": True})
        data += [
            {"id": str(device.id), "name": device.name, "in_mission": False}
            for device in devices
            if str(device.id) not in mission_devs
        ]
    else:
        data = [{"id": str(device.id), "name": device.name} for device in devices]

    return jsonify(data), 200


@authorize_admin
@handle_exceptions
def update(user_type, device_id, name, mac, type):
    device = Device.objects.get(id=device_id)

    if name:
        if device.name != name:
            existing_device = Device.objects(name=name).first()
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

    missions = Mission.objects(
        device_ids__in=[ObjectId(device_id)],
        status__in=[MissionStatus.CREATED, MissionStatus.ONGOING, MissionStatus.PAUSED],
    )
    for mission in missions:
        mission.update(pull__device_ids=ObjectId(device_id))

    Device.objects(id=device_id).update(set__status=Status.INACTIVE)
    return jsonify({"message": "Device is deactivated successfully."}), 200

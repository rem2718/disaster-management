from enum import IntEnum


class UserType(IntEnum):
    REGULAR = 1
    ADMIN = 2


class DeviceType(IntEnum):
    UGV = 1
    UAV = 2
    DOG = 3
    CHARGING_STATION = 4
    BROKER = 5


class Status(IntEnum):
    ACTIVE = 1
    ASSIGNED = 2
    INACTIVE = 3


class MissionStatus(IntEnum):
    CREATED = 1
    ONGOING = 2
    PAUSED = 3
    CANCELED = 4
    FINISHED = 5


class MissionCommand(IntEnum):
    START = 1
    PAUSE = 2
    CONTINUE = 3
    CANCEL = 4
    END = 5

from enum import Enum


class UserType(Enum):
    REGULAR = 1
    ADMIN = 2


class RobotType(Enum):
    UGV = 1
    UAV = 2
    DOG = 3


class Status(Enum):
    ACTIVE = 1
    ASSIGNED = 2
    INACTIVE = 3


class MissionStatus(Enum):
    CREATED = 1
    ONGOING = 2
    PAUSED = 3
    CANCELED = 4
    FINISHED = 5

from enum import Enum

class UserType(Enum):
    Regular = 1
    Admin = 2
    
class Status(Enum):
    Active = 1
    Assigned = 2
    Inactive = 3

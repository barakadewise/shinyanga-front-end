from enum import Enum
class Status(Enum):
    SUCCESS="Success",
    ERROR="Error",


class Roles(Enum):
    ADMIN='Admin'
    MEMBER='Member'
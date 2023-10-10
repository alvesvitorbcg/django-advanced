from enum import Enum


class Status(Enum):
    NEW = 0
    APPROVED = 1
    REJECTED = 2


class VerificationStatus(Enum):
    PENDING = 0
    ASSIGNED = 1
    VERIFIED = 2
    FAILED = 3

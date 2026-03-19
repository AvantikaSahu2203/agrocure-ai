import enum

class UserRole(str, enum.Enum):
    FARMER = "FARMER"
    ADMIN = "ADMIN"
    STORE_OWNER = "STORE_OWNER"

class CropStatus(str, enum.Enum):
    HEALTHY = "HEALTHY"
    INFECTED = "INFECTED"
    HARVESTED = "HARVESTED"

class DetectionStatus(str, enum.Enum):
    PENDING = "PENDING"
    PROCESSED = "PROCESSED"
    COMPLETED = "COMPLETED"
    REVIEWED = "REVIEWED"

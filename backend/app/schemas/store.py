from typing import Optional, Any, Dict
from pydantic import BaseModel
from uuid import UUID

# Shared properties
class StoreBase(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    inventory: Optional[Dict[str, Any]] = None

# Properties to receive on creation
class StoreCreate(StoreBase):
    name: str

# Properties to receive on update
class StoreUpdate(StoreBase):
    pass

# Properties shared by models stored in DB
class StoreInDBBase(StoreBase):
    id: UUID
    owner_id: UUID

    class Config:
        orm_mode = True

# Properties to return to client
class Store(StoreInDBBase):
    pass

from typing import Optional
from pydantic import BaseModel
from .medicine import Medicine
from .store import Store

class InventoryBase(BaseModel):
    quantity: int = 0
    unit_price: float

class InventoryCreate(InventoryBase):
    store_id: str
    medicine_id: str

class InventoryUpdate(InventoryBase):
    quantity: Optional[int] = None
    unit_price: Optional[float] = None

class InventoryInDBBase(InventoryBase):
    id: str
    store_id: str
    medicine_id: str

    class Config:
        orm_mode = True

class Inventory(InventoryInDBBase):
    medicine: Optional[Medicine] = None
    store: Optional[Store] = None

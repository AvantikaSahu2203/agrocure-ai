from typing import Optional
from pydantic import BaseModel

class MedicineBase(BaseModel):
    name: str
    description: Optional[str] = None
    manufacturer: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None

class MedicineCreate(MedicineBase):
    pass

class MedicineUpdate(MedicineBase):
    pass

class MedicineInDBBase(MedicineBase):
    id: str

    class Config:
        orm_mode = True

class Medicine(MedicineInDBBase):
    pass

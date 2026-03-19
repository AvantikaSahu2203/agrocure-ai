from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.medicine import Medicine
from app.models.inventory import StoreInventory
from app.schemas.medicine import MedicineCreate, MedicineUpdate
from app.schemas.inventory import InventoryCreate, InventoryUpdate

class CRUDMedicine(CRUDBase[Medicine, MedicineCreate, MedicineUpdate]):
    def get_by_category(self, db: Session, category: str) -> List[Medicine]:
        return db.query(Medicine).filter(Medicine.category == category).all()

medicine = CRUDMedicine(Medicine)

class CRUDInventory(CRUDBase[StoreInventory, InventoryCreate, InventoryUpdate]):
    def get_by_store(self, db: Session, store_id: str) -> List[StoreInventory]:
        return db.query(StoreInventory).filter(StoreInventory.store_id == store_id).all()
        
    def get_multi_with_medicine(self, db: Session, skip: int = 0, limit: int = 100) -> List[StoreInventory]:
        # Perform join load if needed, but default lazy load works with Pydantic ORM mode if session is open
        return db.query(StoreInventory).offset(skip).limit(limit).all()

inventory = CRUDInventory(StoreInventory)

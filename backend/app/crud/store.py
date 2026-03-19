from typing import List, Optional
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.models.store import Store
from app.schemas.store import StoreCreate, StoreUpdate

class CRUDStore:
    def get(self, db: Session, id: UUID) -> Optional[Store]:
        return db.query(Store).filter(Store.id == id).first()

    def get_multi_by_owner(
        self, db: Session, *, owner_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[Store]:
        return (
            db.query(Store)
            .filter(Store.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_with_owner(
        self, db: Session, *, obj_in: StoreCreate, owner_id: UUID
    ) -> Store:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = Store(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: Store, obj_in: StoreUpdate
    ) -> Store:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: UUID) -> Store:
        obj = db.query(Store).get(id)
        db.delete(obj)
        db.commit()
        return obj

store = CRUDStore()

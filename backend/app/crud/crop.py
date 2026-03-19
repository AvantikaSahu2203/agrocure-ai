from typing import List, Optional
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.models.crop import Crop
from app.schemas.crop import CropCreate, CropUpdate

class CRUDCrop:
    def get(self, db: Session, id: UUID) -> Optional[Crop]:
        return db.query(Crop).filter(Crop.id == id).first()

    def get_multi_by_owner(
        self, db: Session, *, owner_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[Crop]:
        return (
            db.query(Crop)
            .filter(Crop.user_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_with_owner(
        self, db: Session, *, obj_in: CropCreate, owner_id: UUID
    ) -> Crop:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = Crop(**obj_in_data, user_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: Crop, obj_in: CropUpdate
    ) -> Crop:
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

    def remove(self, db: Session, *, id: UUID) -> Crop:
        obj = db.query(Crop).get(id)
        db.delete(obj)
        db.commit()
        return obj

crop = CRUDCrop()

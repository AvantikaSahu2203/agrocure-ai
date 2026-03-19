from typing import List, Optional
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.models.disease import DiseaseDetection
from app.schemas.disease import DiseaseDetectionCreate, DiseaseDetectionUpdate

class CRUDDisease:
    def get(self, db: Session, id: UUID) -> Optional[DiseaseDetection]:
        return db.query(DiseaseDetection).filter(DiseaseDetection.id == id).first()

    def get_multi_by_owner(
        self, db: Session, *, owner_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[DiseaseDetection]:
        return (
            db.query(DiseaseDetection)
            .filter(DiseaseDetection.user_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_with_owner(
        self, db: Session, *, obj_in: DiseaseDetectionCreate, owner_id: UUID
    ) -> DiseaseDetection:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = DiseaseDetection(**obj_in_data, user_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: DiseaseDetection, obj_in: DiseaseDetectionUpdate
    ) -> DiseaseDetection:
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

    def remove(self, db: Session, *, id: UUID) -> DiseaseDetection:
        obj = db.query(DiseaseDetection).get(id)
        db.delete(obj)
        db.commit()
        return obj

disease = CRUDDisease()

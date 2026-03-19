from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.DiseaseDetection])
def read_detections(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve disease detections.
    """
    detections = crud.disease.get_multi_by_owner(
        db=db, owner_id=current_user.id, skip=skip, limit=limit
    )
    return detections

@router.post("/", response_model=schemas.DiseaseDetection)
def create_detection(
    *,
    db: Session = Depends(deps.get_db),
    detection_in: schemas.DiseaseDetectionCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Submit image for disease detection.
    This endpoint would trigger the AI agent/model.
    """
    detection = crud.disease.create_with_owner(
        db=db, obj_in=detection_in, owner_id=current_user.id
    )
    # TODO: Trigger AI analysis here
    return detection

@router.get("/{id}", response_model=schemas.DiseaseDetection)
def read_detection(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get detection result by ID.
    """
    detection = crud.disease.get(db=db, id=id)
    if not detection:
        raise HTTPException(status_code=404, detail="Detection not found")
    if detection.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return detection

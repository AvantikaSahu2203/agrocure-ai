from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Crop])
def read_crops(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve crops.
    """
    crops = crud.crop.get_multi_by_owner(
        db=db, owner_id=current_user.id, skip=skip, limit=limit
    )
    return crops

@router.post("/", response_model=schemas.Crop)
def create_crop(
    *,
    db: Session = Depends(deps.get_db),
    crop_in: schemas.CropCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new crop.
    """
    crop = crud.crop.create_with_owner(db=db, obj_in=crop_in, owner_id=current_user.id)
    return crop

@router.put("/{id}", response_model=schemas.Crop)
def update_crop(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    crop_in: schemas.CropUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a crop.
    """
    crop = crud.crop.get(db=db, id=id)
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    if crop.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    crop = crud.crop.update(db=db, db_obj=crop, obj_in=crop_in)
    return crop

@router.get("/{id}", response_model=schemas.Crop)
def read_crop(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get crop by ID.
    """
    crop = crud.crop.get(db=db, id=id)
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    if crop.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return crop

@router.delete("/{id}", response_model=schemas.Crop)
def delete_crop(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a crop.
    """
    crop = crud.crop.get(db=db, id=id)
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    if crop.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    crop = crud.crop.remove(db=db, id=id)
    return crop

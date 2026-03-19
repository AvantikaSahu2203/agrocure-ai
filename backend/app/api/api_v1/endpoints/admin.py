from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.models.user import UserRole

router = APIRouter()

def check_admin_privileges(current_user: models.User):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="The user doesn't have enough privileges",
        )

@router.get("/stats", response_model=Dict[str, int])
def read_system_stats(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get system statistics (Admin only).
    """
    check_admin_privileges(current_user)
    
    user_count = db.query(models.User).count()
    crop_count = db.query(models.Crop).count()
    detection_count = db.query(models.DiseaseDetection).count()
    store_count = db.query(models.Store).count()

    return {
        "users": user_count,
        "crops": crop_count,
        "detections": detection_count,
        "stores": store_count
    }

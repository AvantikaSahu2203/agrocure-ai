from fastapi import APIRouter, Depends
from app.api import deps
from app.models import User
from app.schemas.advisory import AdvisoryRequest, AdvisoryResponse
from app.services.advisory_service import generate_crop_advice

router = APIRouter()

@router.post("/get-advice", response_model=AdvisoryResponse)
def get_crop_advice(
    data: AdvisoryRequest,
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Get comprehensive crop advisory based on weather, growth stage, and soil data.
    """
    return generate_crop_advice(data, current_user)

from typing import Any

from fastapi import APIRouter, Depends, Query
from app.api import deps
from app.models import User
from app.services.maps import geocode_address

router = APIRouter()

@router.get("/geocode")
def geocode(
    address: str = Query(..., description="Address to geocode"),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Geocode an address.
    """
    return geocode_address(address)

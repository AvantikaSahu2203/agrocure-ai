from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
from app.crud.crud_market import medicine, inventory

router = APIRouter()

@router.get("/products", response_model=List[schemas.Inventory])
def read_products(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    category: str = None
) -> Any:
    """
    Retrieve products (inventory items joined with medicine details).
    """
    products = inventory.get_multi_with_medicine(db, skip=skip, limit=limit)
    return products

@router.post("/medicines", response_model=schemas.Medicine)
def create_medicine(
    *,
    db: Session = Depends(deps.get_db),
    medicine_in: schemas.MedicineCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new medicine (Admin/Store Owner only).
    """
    # In a real app, check permissions
    return medicine.create(db=db, obj_in=medicine_in)

@router.post("/inventory", response_model=schemas.Inventory)
def add_inventory_item(
    *,
    db: Session = Depends(deps.get_db),
    item_in: schemas.InventoryCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Add item to store inventory.
    """
    return inventory.create(db=db, obj_in=item_in)

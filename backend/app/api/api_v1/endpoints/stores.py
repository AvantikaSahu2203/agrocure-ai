from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Store])
def read_stores(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve stores.
    """
    stores = crud.store.get_multi_by_owner(
        db=db, owner_id=current_user.id, skip=skip, limit=limit
    )
    return stores

@router.post("/", response_model=schemas.Store)
def create_store(
    *,
    db: Session = Depends(deps.get_db),
    store_in: schemas.StoreCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new store.
    """
    store = crud.store.create_with_owner(db=db, obj_in=store_in, owner_id=current_user.id)
    return store

@router.get("/{id}", response_model=schemas.Store)
def read_store(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get store by ID.
    """
    store = crud.store.get(db=db, id=id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    if store.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return store

@router.put("/{id}", response_model=schemas.Store)
def update_store(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    store_in: schemas.StoreUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a store.
    """
    store = crud.store.get(db=db, id=id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    if store.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    store = crud.store.update(db=db, db_obj=store, obj_in=store_in)
    return store

@router.delete("/{id}", response_model=schemas.Store)
def delete_store(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a store.
    """
    store = crud.store.get(db=db, id=id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    if store.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    store = crud.store.remove(db=db, id=id)
    return store

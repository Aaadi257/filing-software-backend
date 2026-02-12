from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import crud
import schemas
from database import get_db

router = APIRouter(
    prefix="/movements",
    tags=["movements"],
)

@router.post("/", response_model=schemas.Movement)
def create_movement(movement: schemas.MovementCreate, db: Session = Depends(get_db)):
    return crud.create_movement(db=db, movement=movement)

@router.get("/", response_model=List[schemas.Movement])
def read_movements(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_movements(db, skip=skip, limit=limit)

@router.put("/{movement_id}/return", response_model=schemas.Movement)
def update_movement_status(movement_id: int, movement_update: schemas.MovementUpdate, db: Session = Depends(get_db)):
    return crud.update_movement_status(db, movement_id=movement_id, actual_return_date=movement_update.actual_return_date)

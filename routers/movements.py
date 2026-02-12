from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import crud, schemas
from database import get_db

router = APIRouter(
    prefix="/movements",
    tags=["movements"],
)

@router.post("/", response_model=schemas.Movement)
def create_movement(movement: schemas.MovementCreate, db: Session = Depends(get_db)):
    # Ensure the file exists before creating a movement
    db_file = crud.get_file(db, movement.file_id)
    if not db_file:
        raise HTTPException(status_code=400, detail="Referenced file does not exist")
    return crud.create_movement(db=db, movement=movement)

@router.get("/", response_model=List[schemas.Movement])
def read_movements(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_movements(db, skip=skip, limit=limit)

@router.put("/{movement_id}/return", response_model=schemas.Movement)
def update_movement_status(movement_id: int, movement_update: schemas.MovementUpdate, db: Session = Depends(get_db)):
    return crud.update_movement_status(db, movement_id=movement_id, actual_return_date=movement_update.actual_return_date)

@router.delete("/{movement_id}")
def delete_movement(movement_id: int, db: Session = Depends(get_db)):
    db_movement = crud.delete_movement(db, movement_id=movement_id)
    if not db_movement:
        raise HTTPException(status_code=404, detail="Movement not found")
    return {"message": "Movement deleted successfully"}

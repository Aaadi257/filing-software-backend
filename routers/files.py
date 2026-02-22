from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

class ReassignRackRequest(BaseModel):
    rack_id: int

from backend import crud, models, schemas
from backend.database import get_db

router = APIRouter(
    prefix="/files",
    tags=["files"],
)

@router.post("/", response_model=schemas.File)
def create_file(file: schemas.FileCreate, db: Session = Depends(get_db)):
    return crud.create_file(db=db, file=file)

@router.get("/", response_model=List[schemas.File])
def read_files(skip: int = 0, limit: int = 100, search: Optional[str] = None, db: Session = Depends(get_db)):
    return crud.get_files(db, skip=skip, limit=limit, search=search)

@router.delete("/{file_id}")
def delete_file(file_id: int, db: Session = Depends(get_db)):
    db_file = crud.delete_file(db, file_id=file_id)
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")
    return {"message": "File deleted successfully"}

@router.put("/{file_id}/reassign-rack")
def reassign_rack(file_id: int, request: ReassignRackRequest, db: Session = Depends(get_db)):
    db_file = db.query(models.File).filter(models.File.id == file_id).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")
    
    db_rack = db.query(models.Rack).filter(models.Rack.id == request.rack_id).first()
    if not db_rack:
        raise HTTPException(status_code=404, detail="Rack not found")
        
    db_file.rack_id = request.rack_id
    db.commit()
    db.refresh(db_file)
    return {"message": "Rack reassigned successfully"}

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response
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
def read_files(
    skip: int = 0, 
    limit: int = 100, 
    search: Optional[str] = None, 
    company_id: Optional[int] = Query(None),
    category_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    return crud.get_files(
        db, 
        skip=skip, 
        limit=limit, 
        search=search, 
        company_id=company_id, 
        category_id=category_id
    )

from openpyxl import Workbook
from io import BytesIO

@router.get("/export")
def export_files(
    company_id: Optional[int] = Query(None),
    category_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    # Fetch filtered files using existing crud logic (no limit)
    files = crud.get_files(
        db, 
        skip=0, 
        limit=1000000, 
        search=None, 
        company_id=company_id, 
        category_id=category_id
    )
    
    # Create Excel workbook
    wb = Workbook()
    ws = wb.active
    
    # Determine dynamic filename based on filters
    filename_parts = []
    sheet_title = "All Files"
    
    if company_id:
        company = crud.get_company(db, company_id)
        if company:
            # e.g PACIFIC_JASOLA_Files.xlsx
            company_name_sanitized = company.name.replace(' ', '_').upper()
            filename_parts.append(f"{company_name_sanitized}")
            sheet_title = company.name.upper()
            
    elif category_id: # Usually UI only allows one or other or both but fallback to category if both
        category = crud.get_category(db, category_id)
        if category:
            category_name_sanitized = category.name.replace(' ', '_').upper()
            filename_parts.append(f"{category_name_sanitized}")
            sheet_title = category.name.upper()
            
    if not filename_parts:
        filename_parts.append("ALL")
        
    filename = "_".join(filename_parts) + "_Files.xlsx"
    
    # Set max 31 char limit for excel sheet title
    ws.title = sheet_title[:31]
    
    # Define columns exactly matching File Repository table
    columns = [
        "Reference Code", 
        "File Name", 
        "Company", 
        "Rack", 
        "Category", 
        "Created On", 
        "Creator"
    ]
    ws.append(columns)
    
    # Append rows
    for f in files:
        ws.append([
            f.reference_code,
            f.name,
            f.company.name if f.company else "",
            f.rack.code if f.rack else "",
            f.category.name if f.category else "",
            f.creation_date.strftime("%d %b %Y") if f.creation_date else "",
            f.creator_name
        ])
    
    # Save into memory
    file_stream = BytesIO()
    wb.save(file_stream)
    file_stream.seek(0)

    return Response(
        content=file_stream.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

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

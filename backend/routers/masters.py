from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, models, schemas
from ..database import get_db


router = APIRouter(
    prefix="/masters",
    tags=["masters"],
)

@router.post("/companies/", response_model=schemas.Company)
def create_company(company: schemas.CompanyCreate, db: Session = Depends(get_db)):
    db_company = crud.get_company_by_name(db, name=company.name)
    if db_company:
        raise HTTPException(status_code=400, detail="Company already exists")
    return crud.create_company(db=db, company=company)

@router.get("/companies/", response_model=List[schemas.Company])
def read_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_companies(db, skip=skip, limit=limit)

@router.post("/racks/", response_model=schemas.Rack)
def create_rack(rack: schemas.RackCreate, db: Session = Depends(get_db)):
    db_rack = crud.get_rack_by_code(db, code=rack.code)
    if db_rack:
        raise HTTPException(status_code=400, detail="Rack already exists")
    return crud.create_rack(db=db, rack=rack)

@router.get("/racks/", response_model=List[schemas.Rack])
def read_racks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_racks(db, skip=skip, limit=limit)

@router.post("/categories/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_category = crud.get_category_by_name(db, name=category.name)
    if db_category:
        raise HTTPException(status_code=400, detail="Category name already exists")
    db_category = crud.get_category_by_code(db, code=category.code)
    if db_category:
        raise HTTPException(status_code=400, detail="Category code already exists")
    return crud.create_category(db=db, category=category)

@router.get("/categories/", response_model=List[schemas.Category])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_categories(db, skip=skip, limit=limit)

@router.delete("/companies/{company_id}")
def delete_company(company_id: int, db: Session = Depends(get_db)):
    db_company = crud.delete_company(db, company_id=company_id)
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    return {"message": "Company deleted successfully"}

@router.delete("/racks/{rack_id}")
def delete_rack(rack_id: int, db: Session = Depends(get_db)):
    db_rack = crud.delete_rack(db, rack_id=rack_id)
    if not db_rack:
        raise HTTPException(status_code=404, detail="Rack not found")
    return {"message": "Rack deleted successfully"}

@router.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = crud.delete_category(db, category_id=category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted successfully"}

from sqlalchemy.orm import Session
from sqlalchemy import or_
from . import models, schemas
from datetime import datetime, date

# Company
def get_company(db: Session, company_id: int):
    return db.query(models.Company).filter(models.Company.id == company_id).first()

def get_company_by_name(db: Session, name: str):
    return db.query(models.Company).filter(models.Company.name == name).first()

def get_companies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Company).offset(skip).limit(limit).all()

def create_company(db: Session, company: schemas.CompanyCreate):
    db_company = models.Company(name=company.name)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

# Rack
def get_rack(db: Session, rack_id: int):
    return db.query(models.Rack).filter(models.Rack.id == rack_id).first()

def get_rack_by_code(db: Session, code: str):
    return db.query(models.Rack).filter(models.Rack.code == code).first()

def get_racks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Rack).offset(skip).limit(limit).all()

def create_rack(db: Session, rack: schemas.RackCreate):
    db_rack = models.Rack(code=rack.code)
    db.add(db_rack)
    db.commit()
    db.refresh(db_rack)
    return db_rack

# Category
def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def get_category_by_name(db: Session, name: str):
    return db.query(models.Category).filter(models.Category.name == name).first()

def get_category_by_code(db: Session, code: str):
    return db.query(models.Category).filter(models.Category.code == code).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()

def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(name=category.name, code=category.code)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# File
def get_file(db: Session, file_id: int):
    return db.query(models.File).filter(models.File.id == file_id).first()

def get_files(db: Session, skip: int = 0, limit: int = 100, search: str = None):
    query = db.query(models.File)
    if search:
        query = query.filter(
            or_(
                models.File.name.ilike(f"%{search}%"),
                models.File.reference_code.ilike(f"%{search}%")
            )
        )
    return query.offset(skip).limit(limit).all()

def create_file(db: Session, file: schemas.FileCreate):
    company = get_company(db, file.company_id)
    category = get_category(db, file.category_id)
    
    year = datetime.now().year
    
    company_code = company.name[:3].upper()
    category_prefix = category.name[:3].upper()
    
    prefix = f"{company_code}/{year}/{category_prefix}"
    
    last_file = db.query(models.File).filter(models.File.reference_code.like(f"{prefix}%")).order_by(models.File.id.desc()).first()
    
    if last_file:
        try:
            last_number = int(last_file.reference_code.split('/')[-1])
            running_number = last_number + 1
        except ValueError:
            running_number = 1
    else:
        running_number = 1
    
    reference_code = f"{prefix}/{running_number:04d}"
    
    db_file = models.File(
        name=file.name,
        creation_date=file.creation_date,
        creator_name=file.creator_name,
        company_id=file.company_id,
        rack_id=file.rack_id,
        category_id=file.category_id,
        reference_code=reference_code
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

# Movement
def create_movement(db: Session, movement: schemas.MovementCreate):
    db_movement = models.Movement(**movement.dict())
    db.add(db_movement)
    db.commit()
    db.refresh(db_movement)
    return db_movement

def get_movements(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Movement).offset(skip).limit(limit).all()

def update_movement_status(db: Session, movement_id: int, actual_return_date: date):
    db_movement = db.query(models.Movement).filter(models.Movement.id == movement_id).first()
    if db_movement:
        db_movement.actual_return_date = actual_return_date
        db_movement.status = "Received"
        db.commit()
        db.refresh(db_movement)
    return db_movement

# Delete functions
def delete_company(db: Session, company_id: int):
    db_company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if db_company:
        db.delete(db_company)
        db.commit()
    return db_company

def delete_rack(db: Session, rack_id: int):
    db_rack = db.query(models.Rack).filter(models.Rack.id == rack_id).first()
    if db_rack:
        db.delete(db_rack)
        db.commit()
    return db_rack

def delete_category(db: Session, category_id: int):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category

def delete_file(db: Session, file_id: int):
    db_file = db.query(models.File).filter(models.File.id == file_id).first()
    if db_file:
        db.delete(db_file)
        db.commit()
    return db_file

def delete_movement(db: Session, movement_id: int):
    db_movement = db.query(models.Movement).filter(models.Movement.id == movement_id).first()
    if db_movement:
        db.delete(db_movement)
        db.commit()
    return db_movement

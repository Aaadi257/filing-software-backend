from pydantic import BaseModel
from typing import List, Optional
from datetime import date

# Company Schemas
class CompanyBase(BaseModel):
    name: str

class CompanyCreate(CompanyBase):
    pass

class Company(CompanyBase):
    id: int
    class Config:
        from_attributes = True

# Rack Schemas
class RackBase(BaseModel):
    code: str

class RackCreate(RackBase):
    pass

class Rack(RackBase):
    id: int
    class Config:
        from_attributes = True

# Category Schemas
class CategoryBase(BaseModel):
    name: str
    code: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    class Config:
        from_attributes = True

# File Schemas
class FileBase(BaseModel):
    name: str
    creation_date: date
    creator_name: str
    company_id: int
    rack_id: int
    category_id: int

class FileCreate(FileBase):
    pass

class File(FileBase):
    id: int
    reference_code: str
    company: Company
    rack: Rack
    category: Category
    class Config:
        from_attributes = True

# Movement Schemas
class MovementBase(BaseModel):
    file_id: int
    handed_over_to: str
    transfer_date: date
    expected_return_date: date
    purpose: str

class MovementCreate(MovementBase):
    pass

class MovementUpdate(BaseModel):
    actual_return_date: date
    status: str

class Movement(MovementBase):
    id: int
    actual_return_date: Optional[date] = None
    status: str
    file: File
    class Config:
        from_attributes = True

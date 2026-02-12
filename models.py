from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    files = relationship("File", back_populates="company")

class Rack(Base):
    __tablename__ = "racks"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True) # Alphanumeric e.g., A1, B2

    files = relationship("File", back_populates="rack")

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    code = Column(String, unique=True) # Used for generating reference code (first 3 letters)

    files = relationship("File", back_populates="category")

class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    reference_code = Column(String, unique=True, index=True)
    creation_date = Column(Date)
    creator_name = Column(String)
    
    company_id = Column(Integer, ForeignKey("companies.id"))
    rack_id = Column(Integer, ForeignKey("racks.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))

    company = relationship("Company", back_populates="files")
    rack = relationship("Rack", back_populates="files")
    category = relationship("Category", back_populates="files")
    movements = relationship("Movement", back_populates="file")

class Movement(Base):
    __tablename__ = "movements"
    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("files.id"))
    handed_over_to = Column(String)
    transfer_date = Column(Date)
    expected_return_date = Column(Date)
    actual_return_date = Column(Date, nullable=True)
    purpose = Column(String)
    status = Column(String, default="Moved") # Moved / Received

    file = relationship("File", back_populates="movements")

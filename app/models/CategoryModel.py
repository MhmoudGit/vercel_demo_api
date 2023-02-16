# import base from db file for the schemas
from ..data.db import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from .ProductModel import ProductCreate
from typing import List

# postgres model for product of the postgres database
class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, nullable=False)
    category_name = Column(String, nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')) 
    
    products = relationship('Product', back_populates='category')


# pydantic model for creating categories from api for fastapi
class CategoryCreate(BaseModel):
    category_name: str 
    
#pydantic model for geting categories from api for fastapi
class CategoryGet(BaseModel):
    category_name: str 
    products: List[ProductCreate]

    class Config:
        orm_mode = True
    
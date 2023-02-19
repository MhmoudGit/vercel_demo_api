# import base from db file for the schemas
from ..data.db import Base
from sqlalchemy import Column, Integer, String, Boolean, Numeric, TIMESTAMP, text, ForeignKey
from pydantic import BaseModel, validator
from sqlalchemy.orm import relationship


# postgres model for product of the postgres database
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)
    available = Column(Boolean, nullable=False)
    price_kg = Column(Numeric, nullable=True)
    price_item = Column(Numeric, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')) 
    image = Column(String)

    category = relationship('Category', back_populates='products')  


# pydantic model for creating products from api for fastapi
class ProductCreate(BaseModel):
    name: str 
    category_id: int 
    available: bool
    price_kg: float | None
    price_item: float | None
    image: str
    # category_name: CategoryCreate
    class Config:
        orm_mode = True

# validation for either one of the prices and not both exist or doesnt exist
@validator('price_kg', 'price_item', pre=True)
def check_exclusivity(cls, value, values):
        if value is not None and values.get('price_item') is not None:
            raise ValueError('only one of price_kg or price_item can be set')
        if value is None and values.get('price_item') is None:
            raise ValueError('either price_kg or price_item must be set')
        return value

@validator('price_item', 'price_kg', pre=True)
def check_exclusivity2(cls, value, values):
        if value is not None and values.get('price_kg') is not None:
            raise ValueError('only one of price_kg or price_item can be set')
        if value is None and values.get('price_kg') is None:
            raise ValueError('either price_kg or price_item must be set')
        return value
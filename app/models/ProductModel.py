# import base from db file for the schemas
from ..data.db import Base
from sqlalchemy import Column, Integer, String, Boolean, Numeric, TIMESTAMP, text
from pydantic import BaseModel

# model for product of the postgres database
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    available = Column(Boolean, nullable=False)
    price_kg = Column(Numeric, nullable=True)
    price_item = Column(Numeric, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')) 

#model for creating products from api for fastapi
class ProductCreate(BaseModel):
    name: str
    category: str
    available: bool
    price_kg: float = None
    price_item: float = None
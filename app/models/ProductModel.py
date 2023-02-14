# import base from db file for the schemas
from ..data.db import Base
from sqlalchemy import Column, Integer, String, Boolean, Numeric

# model for product
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    available = Column(Boolean, nullable=False)
    price_kg = Column(Numeric, nullable=True)
    price_item = Column(Numeric, nullable=True)
    # created_at = Column(TIMESTAMP.timezone, nullable=False)


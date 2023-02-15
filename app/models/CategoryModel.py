# import base from db file for the schemas
from ..data.db import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from pydantic import BaseModel

# postgres model for product of the postgres database
class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, nullable=False)
    category_name = Column(String, nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')) 


# pydantic model for creating products from api for fastapi
class CategoryCreate(BaseModel):
    category_name: str
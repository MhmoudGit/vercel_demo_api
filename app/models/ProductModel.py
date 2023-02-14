# importing pydantic for schemas
from pydantic import BaseModel

# model for product
class Product(BaseModel):
    name: str
    category: str
    available: bool
    price_kg: int = None
    price_item: int = None
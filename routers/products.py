# import apirouter to be able to use this file in main.py
from fastapi import APIRouter, HTTPException
# importing models for schemas
from models.ProductModel import Product
from random import randrange
from data.db import my_products


# create an instance of apirouter and call it
router = APIRouter(
    prefix="/products", 
    tags=["products"],
)


# get_products path
@router.get('/')  #its jus '/' because the prefix is set to products so no need to write '/products'
def get_products():
    return {'data': my_products}


# post_products to products path
@router.post('/')
def create_product(product: Product):
    if product.price_kg is None and product.price_item is None:
        raise HTTPException(
            status_code=400, detail="Either price_kg or price_item must be specified")
    product_dict = product.dict()
    product_dict["id"] = randrange(0, 10000000)
    my_products.append(product_dict)
    return {'data': product_dict}


# find poroduct by id
def find_product(id: int):
    for p in my_products:
        if p["id"] == id:
            return p


# get single product
@router.get('/{id}')
def get_product(id: int):
    p = find_product(id)
    if p:
        return p
    else:
        raise HTTPException(
            status_code=400, detail="Product doesnt exist")

# import apirouter to be able to use this file in main.py
from fastapi import APIRouter, HTTPException
# importing models for schemas
from models import ProductModel
from random import randrange
from data import my_products


# create an instance of apirouter and call it
router = APIRouter()
# model for product
Product = ProductModel.Product



# get_products path
@router.get('/products')
def get_products():
    return {'data': my_products}


# post_products to products path
@router.post('/products')
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
@router.get('/products/{id}')
def get_product(id: int):
    p = find_product(id)
    if p:
        return p
    else:
        raise HTTPException(
            status_code=400, detail="Product doesnt exist")

# import apirouter to be able to use this file in main.py
from fastapi import APIRouter, HTTPException, status
# importing models for schemas
from models.ProductModel import Product
from random import randrange
from data.db import my_products

# ------needed logic -------#
# find poroduct by id
def find_product(id: int):
    for p in my_products:
        if p["id"] == id:
            return p


# create an instance of apirouter and call it
router = APIRouter(
    prefix="/products",
    tags=["products"],
)

# get all products path
@router.get('/')    # its just '/' because the prefix is set to products so no need to write '/products'
def get_products():
    return {'data': my_products}

# post/create product to products path
@router.post('/', status_code=status.HTTP_201_CREATED)
def create_product(product: Product):
    if (product.price_kg is None and product.price_item is None) or (product.price_kg and product.price_item):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Either price_kg or price_item must be specified and not both")
    product_dict = product.dict()
    product_dict["id"] = randrange(0, 10000000)
    my_products.append(product_dict)
    return {'data': product_dict}

# get single product
@router.get('/{id}')
def get_product(id: int):
    p = find_product(id)
    if p:
        return p
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {id} doesnt exist")

#delete a single product
@router.delete('/{id}')
def delete_product(id: int):
    p = find_product(id)
    if p:
        my_products.remove(p)
        return p
    else: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {id} doesnt exist")

# updating a product
@router.put('/{id}')
def update_product(id: int, product: Product):
    p = find_product(id)
    product_dict = product.dict()
    if p is not None and p['id'] == id:
        product_dict['id'] = id
        my_products[my_products.index(p)] = product_dict
    else: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {id} doesnt exist")
    print(p)
    return {'data' : product}

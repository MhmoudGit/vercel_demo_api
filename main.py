# firstly import fastapi
from fastapi import FastAPI, HTTPException
# importing models for schemas
from models import ProductModel
from random import randrange


# create an instance of fastapi and call it
app = FastAPI()
# model for product
Product = ProductModel.Product


# products db example:
my_products = [
    {
        'name': 'ex_name',
        'category': 'ex_category',
        'available': True,
        'price_kg': 100,
        'price_item': None,
        'id': 1
    }
]

# routes/path operations
# decorator initialized by '@' then the instance of fastapi then the http method then the path or route'/'
@app.get('/')
def home():  # function
    return {'message': 'this is the home/login path'}


# get_products path
@app.get('/products')
def get_products():
    return {'data': my_products}


# post_products to products path
@app.post('/products')
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


@app.get('/products/{id}')
def get_product(id: int):
    p = find_product(id)
    if p:
        return p
    else:
        raise HTTPException(
            status_code=400, detail="Product doesnt exist")

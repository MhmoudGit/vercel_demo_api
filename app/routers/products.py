# import apirouter to be able to use this file in main.py
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
# importing models for schemas
from ..models.ProductModel import Product, ProductCreate
from ..data.db import get_db


# create an instance of apirouter and call it
router = APIRouter(
    prefix="/products",
    tags=["products"],
)

# get all products path
# its just '/' because the prefix is set to products so no need to write '/products'
@router.get('/')
def get_products(db: Session = Depends(get_db), limit: int = 10, skip:int = 0):
    products = db.query(Product).limit(limit).offset(skip).all()
    return {'data': products}

# post/create product to products path
@router.post('/', status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    if (product.price_kg is None and product.price_item is None) or (product.price_kg and product.price_item):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Either price_kg or price_item must be specified and also not both at the same time")

    new_product = Product(**product.dict())
    query = db.query(Product).filter(Product.name == new_product.name and Product.category_name == product.category_name).first()
    if query is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="this product already exist")
            
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {'data': new_product}


# get single product
@router.get('/{id}')
def get_product(id: int, db: Session = Depends(get_db)):
    single_product = db.query(Product).filter(Product.id == id).first()
    if single_product:
        return single_product
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {id} doesnt exist")


#delete a single product
@router.delete('/{id}')
def delete_product(id: int, db: Session = Depends(get_db)):
    product_to_delete = db.query(Product).filter(Product.id == id)
    if product_to_delete.first():
        product_to_delete.delete(synchronize_session=False)
        db.commit()
        return {'message': f'product with id {id} was deleted successfully'}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {id} doesnt exist")


# updating a product
@router.put('/{id}')
def update_product(id: int, product: ProductCreate, db: Session = Depends(get_db)):
    product_to_update = db.query(Product).filter(Product.id == id)
    if product_to_update.first() is not None:
        product_to_update.update(product.dict(), synchronize_session=False)
        db.commit()
        return {'data' : product_to_update.first()}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {id} doesnt exist")
    

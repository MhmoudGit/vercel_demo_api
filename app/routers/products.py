# import apirouter to be able to use this file in main.py
from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
# importing models for schemas
from ..models.ProductModel import Product, ProductCreate
from ..data.db import get_db
from typing import Optional

# create an instance of apirouter and call it
router = APIRouter(
    prefix="/products",
    tags=["products"],
)

# get all products path
# its just '/' because the prefix is set to products so no need to write '/products'
@router.get('/')
def get_products(db: Session = Depends(get_db), limit: int = 10, skip:int = 0, search: Optional[str] = ''):
    products = db.query(Product).filter(Product.name.contains(search)).limit(limit).offset(skip).all()
    return {'data': products}

# post/create product to products path
@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_product(name:str = Form(...), category_id: int = Form(...), available: bool = Form(...), price_kg: float = Form(None), price_item: float = Form(None), image: UploadFile = File(...), db: Session = Depends(get_db)):
        if (price_kg is None and price_item is None) or (price_kg and price_item):
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Either price_kg or price_item must be specified and also not both at the same time")
        
        product: ProductCreate = {"name":name, "category_id":category_id, "available": available, "price_kg": price_kg, "price_item":price_item, "image":f"/images/{image.filename}"}
        
        with open(f"app/images/{image.filename}", "wb") as img_out:
            img_out.write(await image.read())
        new_product = Product(**product)
        
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
async def update_product(id: int,name:str = Form(...), category_id: int = Form(...), available: bool = Form(...), price_kg: float = Form(None), price_item: float = Form(None),db: Session = Depends(get_db), image: UploadFile = File(...)):
    if (price_kg is None and price_item is None) or (price_kg is not None and price_item is not None):
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Either price_kg or price_item must be specified and also not both at the same time")
    
    product: ProductCreate = {"name":name, "category_id":category_id, "available": available, "price_kg": price_kg, "price_item":price_item, "image":f"/images/{image.filename}"}
    with open(f"app/images/{image.filename}", "wb") as img_out:
        img_out.write(await image.read())
    
    product_to_update = db.query(Product).filter(Product.id == id)
    if product_to_update.first() is not None:
        product_to_update.update(product, synchronize_session=False)
        db.commit()
        return product_to_update.first()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {id} doesnt exist")
    













# ProductCreate(name=product.name,category_id=product.category_id, available=product.available, price_item=product.price_item,price_kg=product.price_kg,image=file)

#name:str = Form(...), category_id: int = Form(...), available: bool = Form(...), price_kg: float = Form(...), price_item: float = Form(...),db: Session = Depends(get_db), image: UploadFile = File(...)





# to get the img in response FileResponse(f"app/images/{image.filename}", media_type="image/jpeg")
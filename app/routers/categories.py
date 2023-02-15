# import apirouter to be able to use this file in main.py
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
# importing models for schemas
from ..models.CategoryModel import Category, CategoryCreate, CategoryGet
from ..data.db import get_db


# create an instance of apirouter and call it
router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)

# get all categorys path
# its just '/' because the prefix is set to categorys so no need to write '/categorys'
@router.get('/')
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return {'data': categories}

# post/create category to categorys path
@router.post('/', status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    new_category = Category(**category.dict())
    query = db.query(Category).filter(Category.category_name == category.category_name).first()
    if query is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="this category already exist")
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return {'data': new_category}


# get single category
@router.get('/{id}')
def get_category(id: int, db: Session = Depends(get_db)):
    single_category = db.query(Category).filter(Category.id == id).first()
    if single_category:
        return {'data': single_category}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"category with id {id} doesnt exist")


# get single category products
@router.get('/{id}/products')
def get_category(id: int, db: Session = Depends(get_db)):
    single_category = db.query(Category).filter(Category.id == id).first()
    if single_category:
        return {'data': single_category.products}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"category with id {id} doesnt exist")


#delete a single Category
@router.delete('/{id}')
def delete_category(id: int, db: Session = Depends(get_db)):
    category_to_delete = db.query(Category).filter(Category.id == id)
    if category_to_delete.first():
        category_to_delete.delete(synchronize_session=False)
        db.commit()
        return {'message': f'category with id {id} was deleted successfully'}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"category with id {id} doesnt exist")


# updating a category
@router.put('/{id}')
def update_categoryt(id: int, category: CategoryCreate, db: Session = Depends(get_db)):
    category_to_update = db.query(Category).filter(Category.id == id)
    filter_name = db.query(Category).filter(Category.category_name == category.category_name).first()
    if category_to_update.first() is not None and filter_name is None:
        category_to_update.update(category.dict(), synchronize_session=False)
        db.commit()
        return {'data' : category_to_update.first()}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"category with id {id} doesnt exist or the new category name already exist")
    

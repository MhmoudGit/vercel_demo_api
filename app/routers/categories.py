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
    categories = db.query(Category).filter(Category.category_name == 'بقوليات').first()
    
    return {'data': categories.products}

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
        return single_category
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"category with id {id} doesnt exist")
    


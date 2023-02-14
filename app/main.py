# firstly import fastapi
from fastapi import FastAPI, Depends
# importing routes from routers file
from .routers import products
from .models import ProductModel
from .data.db import engine, get_db

# initiate the database and create the tables 
ProductModel.Base.metadata.create_all(bind=engine)

# create an instance of fastapi and call it
app = FastAPI()


# routes/path operations
@app.get('/') # decorator initialized by '@' then the instance of fastapi then the http method then the path or route'/'
def home():  # function
    return {'message': 'this is the home/login path'}

#products route
app.include_router(products.router)



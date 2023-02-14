# firstly import fastapi
from fastapi import FastAPI
from routers import products


# create an instance of fastapi and call it
app = FastAPI()

# routes/path operations
# decorator initialized by '@' then the instance of fastapi then the http method then the path or route'/'
@app.get('/')
def home():  # function
    return {'message': 'this is the home/login path'}

#products route
app.include_router(products.router)



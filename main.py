# firstly import fastapi
from fastapi import FastAPI


# create an instance of fastapi and call it
app = FastAPI()

# routes/path operations
# decorator initialized by '@' then the instance of fastapi then the http method then the path or route'/'
@app.get('/')
def home():  # function
    return {'message': 'this is the home/login path'}



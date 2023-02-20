import uvicorn
from app.main import app

uvicorn.run(app, host="localhost", port=8000)
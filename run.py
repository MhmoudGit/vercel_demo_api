import uvicorn
from app.main import app
import os

uvicorn.run(app, host="localhost", port=int(os.environ.get("PORT", 8000)))
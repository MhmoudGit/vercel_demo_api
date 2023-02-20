import uvicorn
from app.main import app
import os

uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
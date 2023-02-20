import uvicorn
from app.main import app
import os

@app.on_event("startup")
async def startup():
    # Add startup code here
    print("Starting up...")

@app.on_event("shutdown")
async def shutdown():
    # Add shutdown code here
    print("Shutting down...")
    
uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))


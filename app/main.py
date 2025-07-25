
from fastapi import FastAPI

from fastapi import Depends
from app.dependencies import require_role


app = FastAPI()  # Initialize FastAPI app

# Define a simple route
@app.get("/")   
def read_root(): 
    return {"message": "FastAPI Chat App is running!"}


@app.get("/admin-only")
def admin_dashboard(admin: bool = Depends(require_role("admin"))):
    return {"message": "Welcome, admin!"}


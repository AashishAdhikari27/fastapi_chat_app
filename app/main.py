
from fastapi import FastAPI

app = FastAPI()  # Initialize FastAPI app

# Define a simple route
@app.get("/")   
def read_root(): 
    return {"message": "FastAPI Chat App is running!"}


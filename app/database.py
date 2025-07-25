


import os
from dotenv import load_dotenv

from sqlalchemy import create_engine   # Create SQLAlchemy engine
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker # sessionmaker for creating sessions because we need to interact with the database

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine for the database connection
engine = create_engine(DATABASE_URL)

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

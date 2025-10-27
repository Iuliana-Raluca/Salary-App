import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")  
    MANAGER_API_KEY = os.getenv("MANAGER_API_KEY") 
    DEFAULT_CURRENCY = os.getenv("DEFAULT_CURRENCY", "RON")

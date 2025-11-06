import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")  
    MANAGER_API_KEY = os.getenv("MANAGER_API_KEY") 
    DEFAULT_CURRENCY = os.getenv("DEFAULT_CURRENCY", "RON")
    STORAGE_OUT = os.getenv("STORAGE_OUT", "storage/out")
    STORAGE_ARCHIVE = os.getenv("STORAGE_ARCHIVE", "storage/archives")
    SMTP_HOST = os.getenv("SMTP_HOST")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER = os.getenv("SMTP_USER")
    SMTP_PASS = os.getenv("SMTP_PASS")
    SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USER)

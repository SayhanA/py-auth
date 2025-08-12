import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    MONGO_URI = os.getenv('MONGO_URI')
    
    # Flask-Mail Config
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT') 
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS') 
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')  
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')     
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER') 

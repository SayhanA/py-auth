import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    MONGO_URI = os.getenv('MONGO_URI')
    
    # Flask-Mail Config
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'sayhanahmed05@gmail.com'   
    MAIL_PASSWORD = 'piuw vxur pssq yiih'    
    MAIL_DEFAULT_SENDER = 'sayhanahmed05@gmail.com'

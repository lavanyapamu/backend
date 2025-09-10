import os
from dotenv import load_dotenv

load_dotenv()

user=os.getenv("DB_USER")
password=os.getenv("DB_PASSWORD")
dbname=os.getenv("DB_Name")
port=os.getenv("DB_PORT")
host=os.getenv("DB_HOST")


class Config:
    SQLALCHEMY_DATABASE_URI=f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_ENGINE_OPTIONS ={
        "connect_args":{
            "options": "-c search_path=artflare"
        }
    }

    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT"))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS") == 'True'
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL") == 'True'
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
    FRONTEND_URL = os.getenv("FRONTEND_URL")
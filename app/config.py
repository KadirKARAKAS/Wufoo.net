import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'defaultsecretkey')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://root:12345678@localhost/wufoonet')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
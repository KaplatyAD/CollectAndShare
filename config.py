from dotenv import load_dotenv
import os


load_dotenv()


DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
ACCESS_TOKEN_EXPIRE_MIN = os.getenv('ACCESS_TOKEN_EXPIRE_MIN')
ALGORITHM = os.getenv('ALGORITHM')
SECRET_KEY = os.getenv('SECRET_KEY')
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER=os.environ.get('DB_USER')
DB_PASS=os.environ.get('DB_PASS')
DB_HOST=os.environ.get('DB_HOST')
DB_PORT=os.environ.get('DB_PORT')
DB_NAME=os.environ.get('DB_NAME')



class DB():
    USER=os.environ.get('DB_USER')
    PASS=os.environ.get('DB_PASS')
    HOST=os.environ.get('DB_HOST')
    PORT=os.environ.get('DB_PORT')
    NAME=os.environ.get('DB_NAME')
    
    
SECRET_AUTH = os.environ.get("SECRET_AUTH")

SMTP_USERNAME=os.environ.get('SMTP_USERNAME')
SMTP_PASSWORD=os.environ.get('SMTP_PASSWORD')

TG_TOKEN=os.environ.get('TG_TOKEN')

CAPTCHA_SECRET=os.environ.get('CAPTCHA_SECRET')

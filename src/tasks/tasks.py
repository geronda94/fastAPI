import smtplib
from celery import Celery
from email.message import EmailMessage

class SMTP:
    HOST = 'smtp.gmail.com'
    PORT = 465
    PASSWORD ='snyyschkavvdtwnm'
    USERNAME = 'iiiliev.igor94@gmail.com'
    

celery = Celery('tasks', broker='redis://localhost:6379/0')

def get_email_remplate_dashboard(username:str, body:str | None = None):
    email = EmailMessage()
    email['Subject'] = 'Пробник Тема сообщения'
    email['From'] = SMTP.USERNAME
    email['To'] = 'iiiliev.igor@gmail.com'   
    email.set_content(f'<div><h1>Привет {username}, Это пробная отправка сообщения {body}</h1></div>', subtype='html')
    
    return email


@celery.task
def send_email_report_dashboard(username: str):
    email = get_email_remplate_dashboard(username)
    with smtplib.SMTP_SSL(SMTP.HOST, SMTP.PORT) as server:
        server.login(SMTP.USERNAME, SMTP.PASSWORD)
        server.send_message(email)

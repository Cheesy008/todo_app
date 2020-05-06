from time import sleep
from celery import shared_task
from django.core.mail import send_mail
from todo_app.celery import app


@app.task()
def send_email_task():
    sleep(10)
    print('done')
    send_mail('Переключен', 'Переключен', 'mr.world008@gmail.com', ['tines22109@mailop7.com'])
    return None

from time import sleep
from django.core.mail import send_mail
from todo_app.celery import app


@app.task
def send_email_task(user_email, message):
    sleep(10)
    print('done')
    send_mail(
        'Изменён статус',
        message,
        'mr.world008@gmail.com',
        [user_email]
    )
    return None

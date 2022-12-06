from django.conf import settings
from django.core.mail import send_mail

def send_email_token(email, token):
    try:
        subject='welcome to my Django login system'
        message= f'please verify on this link http://127.0.0.1:8000/verify/{token}'
        from_email=settings.EMAIL_HOST_USER
        to_list = [email,]
        send_mail(subject,message,from_email,to_list)
    except Exception as e:
        return False

    return True
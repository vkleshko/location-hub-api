from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_password_reset_email_task(email: str, reset_link: str):
    send_mail(
        subject="LocationHub Password Reset",
        message=f"To reset your password, click the link: {reset_link}",
        from_email=None,
        recipient_list=[email],
    )

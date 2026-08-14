from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from apps.reviews.models import Review


@shared_task
def send_new_review_email_task(review_id):
    try:
        review = Review.objects.get(id=review_id)
    except Review.DoesNotExist:
        return

    location = review.location

    if review.user_id == location.author.id:
        return

    subject = f"New review for your location '{location.name}'"
    message = (
        f"{review.user.email} left a new review for your location '{location.name}':\n\n"
        f"Rating: {review.rating}/5\n"
        f"Comment: {review.comment or 'No comment'}\n\n"
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[location.author.email],
        fail_silently=False,
    )

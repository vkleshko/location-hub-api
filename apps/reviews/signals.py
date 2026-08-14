from django.core.cache import cache
from django.db import transaction
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.reviews.models import Review
from .tasks import send_new_review_email_task

@receiver([post_save, post_delete], sender=Review)
def review_changed_handler(sender, instance, created=False, **kwargs):
    cache.delete_pattern("*locations_list*")

    if created:
        transaction.on_commit(
            lambda: send_new_review_email_task.delay(instance.id)
        )
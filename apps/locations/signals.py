from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Location


@receiver([post_save, post_delete], sender=Location)
def location_changed_handler(sender, instance, **kwargs):
    cache.delete_pattern("locations_list:*")

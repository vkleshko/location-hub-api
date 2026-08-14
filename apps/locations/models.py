from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.categories.models import Category


class Location(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Name",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="locations",
        verbose_name="Category",
    )
    address = models.CharField(
        max_length=255,
        verbose_name="Address",
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="Latitude",
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="Longitude",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="locations",
        verbose_name="Author",
    )
    is_deleted = models.BooleanField(
        default=False,
        verbose_name="Is deleted",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created at",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated at",
    )

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    def __str__(self):
        return self.name


class LocationView(models.Model):
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="views",
    )
    created_at = models.DateTimeField(auto_now_add=True)

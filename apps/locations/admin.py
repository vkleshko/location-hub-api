from django.contrib import admin
from .models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "category",
        "address",
        "author",
        "is_deleted",
        "created_at",
    )
    list_display_links = (
        "id",
        "name",
    )
    list_filter = (
        "is_deleted",
        "category",
        "created_at",
    )
    search_fields = (
        "name",
        "address",
        "author__email",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    ordering = ("-created_at",)
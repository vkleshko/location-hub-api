from django.contrib import admin
from .models import Review, ReviewReaction


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "location",
        "user",
        "rating",
        "created_at",
    )
    list_display_links = (
        "id",
        "location",
    )
    list_filter = (
        "rating",
        "created_at",
    )


@admin.register(ReviewReaction)
class ReviewReactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "review",
        "user",
        "reaction",
        "created_at",
    )
    list_display_links = (
        "id",
        "review",
    )
    list_filter = (
        "reaction",
        "created_at",
    )

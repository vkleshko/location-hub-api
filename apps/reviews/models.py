from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from apps.locations.models import Location


class ReactionChoices(models.TextChoices):
    LIKE = "like", "Like"
    DISLIKE = "dislike", "Dislike"


class Review(models.Model):
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Location",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="User",
    )
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
        verbose_name="Rating",
    )
    comment = models.TextField(
        verbose_name="Comment",
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
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        constraints = [
            models.UniqueConstraint(
                fields=["location", "user"],
                name="unique_user_location_review",
            )
        ]

    def __str__(self):
        return f"Review by {self.user} for {self.location.name} ({self.rating}/5)"


class ReviewReaction(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="reactions",
        verbose_name="Review",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="review_reactions",
        verbose_name="User",
    )
    reaction = models.CharField(
        max_length=10,
        choices=ReactionChoices.choices,
        verbose_name="Reaction",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created at",
    )

    class Meta:
        verbose_name = "Review Reaction"
        verbose_name_plural = "Review Reactions"
        constraints = [
            models.UniqueConstraint(
                fields=["review", "user"],
                name="unique_user_review_reaction",
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.reaction} for Review #{self.review_id}"

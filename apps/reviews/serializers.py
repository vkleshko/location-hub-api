from rest_framework import serializers
from .models import Review, ReviewReaction, ReactionChoices


class ReviewReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewReaction
        fields = ["reaction"]


class ReviewSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source="user.email")
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()
    user_reaction = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            "id",
            "location",
            "user",
            "user_email",
            "rating",
            "comment",
            "likes_count",
            "dislikes_count",
            "user_reaction",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        request = self.context.get("request")
        location = attrs.get("location")

        if request and request.method == "POST":
            if Review.objects.filter(location=location, user=request.user).exists():
                raise serializers.ValidationError(
                    {"detail": "You have already left a review for this location."}
                )

        return attrs

    def get_likes_count(self, obj):
        return obj.reactions.filter(reaction=ReactionChoices.LIKE).count()

    def get_dislikes_count(self, obj):
        return obj.reactions.filter(reaction=ReactionChoices.DISLIKE).count()

    def get_user_reaction(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            reaction = obj.reactions.filter(user=request.user).first()
            return reaction.reaction if reaction else None
        return None

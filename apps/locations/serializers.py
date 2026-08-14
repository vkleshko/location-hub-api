from rest_framework import serializers
from apps.categories.serializers import CategorySerializer
from .models import Location


class LocationSerializer(serializers.ModelSerializer):
    category_detail = CategorySerializer(source="category", read_only=True)
    author_email = serializers.ReadOnlyField(source="author.email")
    rating = serializers.ReadOnlyField()
    popularity = serializers.ReadOnlyField()
    views_7_days = serializers.ReadOnlyField()

    class Meta:
        model = Location
        fields = [
            "id",
            "name",
            "description",
            "category",
            "category_detail",
            "address",
            "latitude",
            "longitude",
            "author",
            "author_email",
            "rating",
            "popularity",
            "views_7_days",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "author",
            "rating",
            "popularity",
            "views_7_days",
            "created_at",
            "updated_at",
        ]

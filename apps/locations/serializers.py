from rest_framework import serializers
from apps.categories.serializers import CategorySerializer
from .models import Location


class LocationSerializer(serializers.ModelSerializer):
    category_detail = CategorySerializer(source="category", read_only=True)
    author_email = serializers.ReadOnlyField(source="author.email")

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
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "author",
            "created_at",
            "updated_at",
        ]

import django_filters
from .models import Location


class LocationFilter(django_filters.FilterSet):
    category = django_filters.NumberFilter(field_name="category_id")
    author = django_filters.NumberFilter(field_name="author_id")

    rating = django_filters.NumberFilter(field_name="rating")
    min_rating = django_filters.NumberFilter(field_name="rating", lookup_expr="gte")
    max_rating = django_filters.NumberFilter(field_name="rating", lookup_expr="lte")

    class Meta:
        model = Location
        fields = ["category", "author", "rating", "min_rating", "max_rating"]

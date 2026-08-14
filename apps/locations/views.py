from datetime import timedelta

from django.db.models import F, FloatField, Avg, Count, Q, ExpressionWrapper
from django.db.models.functions import Coalesce
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import LocationFilter
from .models import Location, LocationView
from django.core.cache import cache
from .permissions import IsAuthorOrAdminOrReadOnly
from .serializers import LocationSerializer
from .utils import generate_locations_export


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthorOrAdminOrReadOnly]
    filterset_class = LocationFilter
    search_fields = ["name", "description"]
    ordering_fields = ["created_at", "rating", "popularity"]
    ordering = ["-created_at"]

    def get_queryset(self):
        seven_days_ago = timezone.now() - timedelta(days=7)

        return (
            Location.objects.filter(is_deleted=False)
            .annotate(
                rating=Coalesce(
                    Avg("reviews__rating"),
                    0.0,
                    output_field=FloatField(),
                ),
                reviews_count=Count("reviews", distinct=True),
                views_7_days=Count(
                    "views",
                    filter=Q(views__created_at__gte=seven_days_ago),
                    distinct=True,
                ),
                popularity=ExpressionWrapper(
                    (F("rating") * 2.0)
                    + (F("reviews_count") * 1.5)
                    + (F("views_7_days") * 0.2),
                    output_field=FloatField(),
                ),
            )
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user.is_authenticated:
            user_id = f"user_{request.user.id}"
        else:
            if not request.session.session_key:
                request.session.save()
            user_id = f"session_{request.session.session_key}"

        cache_key = f"location_view:{instance.id}:{user_id}"

        if cache.add(cache_key, True, timeout=3600):
            LocationView.objects.create(location=instance)

        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        query_string = request.GET.urlencode()
        cache_key = f"locations_list:{query_string}"

        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)

        if response.status_code == 200:
            cache.set(cache_key, response.data)

        return response

    @action(
        detail=False,
        methods=["get"],
        url_path="export",
        permission_classes=[IsAuthenticated],
    )
    def export_locations(self, request):
        export_format = request.query_params.get("file_format", "json").lower()
        queryset = self.filter_queryset(self.get_queryset())

        return generate_locations_export(queryset, export_format)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()

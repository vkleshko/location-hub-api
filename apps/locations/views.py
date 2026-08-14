from rest_framework import viewsets
from .models import Location, LocationView
from django.core.cache import cache
from .permissions import IsAuthorOrAdminOrReadOnly
from .serializers import LocationSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthorOrAdminOrReadOnly]

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

    def get_queryset(self):
        return Location.objects.filter(is_deleted=False)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()

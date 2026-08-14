from rest_framework import viewsets
from .models import Location
from .permissions import IsAuthorOrAdminOrReadOnly
from .serializers import LocationSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthorOrAdminOrReadOnly]

    def get_queryset(self):
        return Location.objects.filter(is_deleted=False)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()

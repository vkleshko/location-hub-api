from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.locations.permissions import IsAuthorOrAdminOrReadOnly
from .models import Review, ReviewReaction
from .serializers import ReviewReactionSerializer, ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().select_related("user", "location")
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrAdminOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        location_id = self.request.query_params.get("location")
        if location_id:
            queryset = queryset.filter(location_id=location_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated],
        serializer_class=ReviewReactionSerializer,
    )
    def react(self, request, pk=None):
        review = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        reaction_type = serializer.validated_data["reaction"]

        reaction, created = ReviewReaction.objects.get_or_create(
            review=review,
            user=request.user,
            defaults={"reaction": reaction_type},
        )

        if not created:
            if reaction.reaction == reaction_type:
                reaction.delete()
                return Response(
                    data={"detail": "Reaction removed."},
                    status=status.HTTP_200_OK,
                )
            else:
                reaction.reaction = reaction_type
                reaction.save()
                return Response(
                    data={"detail": f"Reaction updated to {reaction_type}."},
                    status=status.HTTP_200_OK,
                )

        return Response(
            {"detail": f"Reaction {reaction_type} added."},
            status=status.HTTP_201_CREATED,
        )

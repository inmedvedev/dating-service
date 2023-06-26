from rest_framework.mixins import CreateModelMixin, ListModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache

from .models import Preference, Rating, Participant
from .serializers import (
    PreferenceSerializer,
    PreferenceCreateSerializer,
    RatingSerializer,
)
from .tasks import make_rating


class PreferenceViewSet(GenericViewSet, CreateModelMixin, ListModelMixin):
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'list':
            return PreferenceSerializer
        if self.action == 'create':
            return PreferenceCreateSerializer

    def get_queryset(self):
        return Preference.objects.filter(participant=self.request.user.participant)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(participant=request.user.participant)
        return Response(serializer.data)


class PreferenceDeleteViewSet(GenericViewSet, DestroyModelMixin):
    permission_classes = (IsAuthenticated,)
    lookup_field = 'name'

    def get_queryset(self):
        return Preference.objects.filter(participant=self.request.user.participant)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class RatingViewSet(GenericViewSet, ListModelMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = RatingSerializer

    def get_queryset(self):
        return Rating.objects.filter(participant=self.request.user.participant)

    def list(self, request, *args, **kwargs):
        try:
            participant = self.request.user.participant
        except Participant.DoesNotExist:
            return Response(
                data={
                    'Message': 'Participant for user not found, probably you login as superuser'
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        rating = Rating.objects.filter(participant=participant)
        if not rating:
            if cache.get(f'{self.request.user.id}-rating') is None:
                cache.set(
                    f'{self.request.user.id}-rating',
                    1,
                    timeout=30 * 60,
                )
                make_rating.delay(
                    self.request.user.id, self.request.user.participant.id
                )
            return Response(data={'Message': 'Ranking, refresh page later'})

        return super().list(request, *args, **kwargs)

from rest_framework.routers import DefaultRouter
from account.viewsets import EmailAuthViewSet
from participant.viewsets import (
    PreferenceViewSet,
    PreferenceDeleteViewSet,
    RatingViewSet,
)

router = DefaultRouter()

router.register(r'', EmailAuthViewSet, basename='auth')
router.register(r'preference', PreferenceViewSet, basename='preference')
router.register(
    r'preference/delete', PreferenceDeleteViewSet, basename='delete_preference'
)
router.register(r'rating', RatingViewSet, basename='rating')

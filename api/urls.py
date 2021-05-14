from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework import routers

from api.viewsets import TrackViewSet, PlaylistViewSet

router = routers.DefaultRouter()
router.register('track', TrackViewSet)
router.register('playlist', PlaylistViewSet)

urlpatterns = [
    path('token/', obtain_jwt_token),
    path('refresh_token/', refresh_jwt_token),
    path('v1/', include(router.urls)),
]

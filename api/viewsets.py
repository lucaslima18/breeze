from music_manager.models import Music, Playlist
from rest_framework import viewsets, request

from api.serializers import TrackSerializer, PlaylistSerializer


class TrackViewSet(viewsets.ModelViewSet):
    queryset = Music.objects.all()
    serializer_class = TrackSerializer


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

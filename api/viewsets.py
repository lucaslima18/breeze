from music_manager.models import Music, Playlist
from rest_framework import viewsets

from api.serializers import PlaylistSerializer, TrackSerializer


class TrackViewSet(viewsets.ModelViewSet):
    '''
        this view define the visalisation
        of track music data
    '''
    queryset = Music.objects.all()
    serializer_class = TrackSerializer


class PlaylistViewSet(viewsets.ModelViewSet):
    '''
        this view define the visalisation
        of playlist music data
    '''
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

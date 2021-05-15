from music_manager.models import Music, Playlist
from rest_framework import serializers


class TrackSerializer(serializers.ModelSerializer):
    '''
        This serializer provides data from stored
        music in local database
    '''
    class Meta:
        model = Music
        fields = (
                    'user',
                    'pk',
                    'music_name',
                    'music_url',
                    'music_artist',
                    'album',
                    'album_url',
                    'music_duration'
                )


class PlaylistSerializer(serializers.ModelSerializer):
    '''
        This serializer provides data from stored
        music in local database
    '''
    class Meta:
        model = Playlist
        fields = (
                    'user',
                    'pk',
                    'name',
                    'playlist_author',
                    'playlist_url',
                    'playlist_uuid'
                )

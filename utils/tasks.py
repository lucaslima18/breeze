import django
django.setup()

from music_manager.models import Playlist


def playlist_objects_info():
    playlists = Playlist.objects.all()
    return f"{playlists}"

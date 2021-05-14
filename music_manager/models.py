from django.db import models
from users.models import CustomUser


class Music(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    music_name = models.CharField(max_length=255, blank=True, null=True)
    music_url = models.CharField(max_length=255, blank=True, null=True)
    music_artist = models.CharField(max_length=255, blank=True, null=True)
    album = models.CharField(max_length=255, blank=True, null=True)
    album_url = models.CharField(max_length=255, blank=True, null=True)
    music_duration = models.IntegerField(blank=True, null=True)
    played = models.BooleanField(default=False)

    def __str__(self):
        return self.music_url


class Playlist(models.Model):
    user = models.OneToOneField(
                CustomUser,
                on_delete=models.CASCADE,
                null=False,
                blank=False
            )
    name = models.CharField(max_length=255, blank=True, null=True)
    playlist_author = models.CharField(max_length=255, blank=True, null=True)
    playlist_url = models.CharField(max_length=255)
    playlist_uuid = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.playlist_url


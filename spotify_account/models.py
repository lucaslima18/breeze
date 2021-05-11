from django.db import models
from django.contrib.auth.models import User


class SpotifyData(models.Model):
    user = models.OneToOneField(
                User, on_delete=models.CASCADE,
                null=False,
                blank=False
            )
    client_id = models.CharField(max_length=255)
    client_secret = models.CharField(max_length=255)
    auth_token = models.CharField(max_length=255, default="") # TODO: trocar por blank null
    playlist_url = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username
from django.db import models
from users.models import CustomUser


class SpotifyData(models.Model):
    user = models.OneToOneField(
                CustomUser,
                on_delete=models.CASCADE,
                null=False,
                blank=False
            )
    auth_code = models.CharField(max_length=700, blank=True, null=True)
    auth_token = models.CharField(max_length=700, blank=True, null=True)
    refresh_token = models.CharField(max_length=700, blank=True, null=True)

    def __str__(self):
        return self.user.username
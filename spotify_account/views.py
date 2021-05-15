from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from utils.spotify_auth import refresh_auth_token

from spotify_account.models import SpotifyData


class ResetTokenTemplateView(LoginRequiredMixin, TemplateView):
    """
        This class call a function for get the auth token for a user
        manual update
    """
    model = SpotifyData
    template_name = 'spotify_account/update_token.html'
    success_url = reverse_lazy('home')

    def get(self, *args, **kwargs):
        resp = super().get(*args, **kwargs)
        user = self.request.user
        spotify_account = SpotifyData.objects.get(user=user)
        auth_token = refresh_auth_token(spotify_account.refresh_token, user)
        if auth_token is not None:
            return resp
        else:
            return redirect(reverse_lazy('create_code'))


def get_code(request):
    '''
        on this method i give the authentication url for spotify authentication
        OBS: replace this link for test in your app.
        for generate this url follow the first step of spotify authorization
        flow
        for more informations follow the link↓
        https://developer.spotify.com/documentation/general/guides/authorization-guide/#authorization-code-flow
    '''
    return redirect("https://accounts.spotify.com/authorize?client_id=82184a930a664f96827a6eb2d97590b1&scope=user-read-playback-state%20user-read-currently-playing%20playlist-modify-public%20playlist-modify-private&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fmusic_manager%2F")

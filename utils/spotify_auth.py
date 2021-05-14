import requests
from spotify_account.models import SpotifyData
from users.models import CustomUser
from decouple import config
from django.urls import reverse_lazy


def get_auth_token(code, user):
    """
        doing an lookup for a token
        this token is for future requests
    """
    client = CustomUser.objects.get(username=user)
    spotify_data = SpotifyData(user=client)
    client_id = config('SPOTIFY_CLIENT_ID')
    client_secret = config('SPOTIFY_CLIENT_SECRET')
    token_url = "https://accounts.spotify.com/api/token"
    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://localhost:8000/music_manager/",
        "client_id": client_id,
        "client_secret": client_secret
    }

    response = requests.post(token_url, data=token_data, headers="")
    response_data = response.json()
    print(response_data)

    auth_token = response_data.get('access_token')
    refresh_token = response_data.get('refresh_token')

    if auth_token is not None and refresh_token is not None:
        spotify_data.auth_token = auth_token
        spotify_data.auth_code = code
        spotify_data.refresh_token = refresh_token
        spotify_data.save()

    return response.json()


def refresh_auth_token(refresh_token, user):
    
    spotify_data = SpotifyData.objects.get(user=user)
    client_id = config('SPOTIFY_CLIENT_ID')
    client_secret = config('SPOTIFY_CLIENT_SECRET')
    token_url = "https://accounts.spotify.com/api/token"
    token_data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "redirect_uri": "http://localhost:8000/music_manager/",
        "client_id": client_id,
        "client_secret": client_secret
    }

    response = requests.post(token_url, data=token_data, headers="")
    response_data = response.json()
    print(response_data)

    error = response_data.get('error')
    auth_token = response_data.get('access_token')
    print(auth_token)
    if error is not None:
        return reverse_lazy('create_code')

    elif auth_token is not None:
        spotify_data.auth_token = auth_token
        print(spotify_data.auth_token)
        spotify_data.save()
        print("SALVOU")
    
    return response.json()

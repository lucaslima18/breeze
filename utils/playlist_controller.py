import json

import requests
from music_manager.models import Music, Playlist


def get_playlist_overview(auth_token, user):
    '''
        this function explore the spotify api,
        get the playlist info and save in the
        local db
    '''
    playlist = Playlist.objects.get(user=user)

    playlist.playlist_uuid = url_to_uuid(playlist.playlist_url)
    url = f"https://api.spotify.com/v1/playlists/{playlist.playlist_uuid}"
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    request = requests.get(url, headers=headers)
    response = request.json()

    playlist.name = response['name']
    playlist.playlist_author = response['owner']['display_name']
    playlist.save()

    return response


def get_playlist_tracks(playlist_url, auth_token, user):
    '''
        this funtion explore the spotify api for obtain
        the tracks based in the user playlist
    '''
    try:
        Music.objects.filter(user=user).delete()

    except:
        pass

    playlist_uuid = url_to_uuid(playlist_url)
    url = f"https://api.spotify.com/v1/playlists/{playlist_uuid}"
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    next_call = False

    while url is not None:
        request = requests.get(url, headers=headers)
        response = request.json()
        error = response.get('error')
     
        if error is None:
            if next_call is not True:
                item = 0
                tracks = response['tracks']['items']

                for track in tracks:
                    int(item)
                    music = Music(user=user)
                    music.music_name = tracks[item]['track']['name']
                    music.music_url = tracks[item]['track']['external_urls']['spotify']
                    music.music_artist = tracks[item]['track']['artists'][0]['name']
                    music.album_url = tracks[item]['track']['album']['external_urls']['spotify']
                    music.album = tracks[item]['track']['album']['name']
                    music.music_duration = tracks[item]['track']['duration_ms']
                    music.save()
                    item = item+1   
                url = tracks = response['tracks']['next']
                next_call = True
          
            else:
                item = 0
                tracks = response['items']

                for track in tracks:
                    int(item)
                    music.music = Music(user=user)
                    music.music_name = tracks[item]['track']['name']
                    music.music_url = tracks[item]['track']['external_urls']['spotify']
                    music.music_uri = tracks[item]['track']['uri']
                    music.music_artist = tracks[item]['track']['artists'][0]['name']
                    music.album_url = tracks[item]['track']['album']['external_urls']['spotify']
                    music.album = tracks[item]['track']['album']['name']
                    music.music_duration = tracks[item]['track']['duration_ms']
                    music.save()
                    item = item+1      
                next_call = True
                url = tracks = response['next']


def insert_music(music_url, playlist_url, auth_token):
    '''
        this function insert tracks on spotify user
        playlist
    '''
    music_uri = url_to_uri(music_url)
    playlist_uuid = url_to_uuid(playlist_url)

    url = f"https://api.spotify.com/v1/playlists/{playlist_uuid}/tracks"
    data = {
        "uris": [f"{music_uri}"]
    }   
    headers = {
        "authorization": f"Bearer {auth_token}"
    }

    request = requests.post(url, data=json.dumps(data), headers=headers)
    response = request.json()

    if response.get('snapshot_id') is not None:
        print("Success", response.get('snapshot_id'))  
    else:
        print(response)


def delete_music(music_url, playlist_url, auth_token):
    '''
        this function delete tracks on spotify user
        playlist
    '''
    music_uri = url_to_uri(music_url)
    playlist_uuid = url_to_uuid(playlist_url)

    url = f"https://api.spotify.com/v1/playlists/{playlist_uuid}/tracks"
    data = {
        "uris": [f"{music_uri}"]
    }    
    headers = {
        "authorization": f"Bearer {auth_token}"
    }

    request = requests.delete(url, data=json.dumps(data), headers=headers)
    response = request.json()

    if response.get('snapshot_id') is not None:
        print("Success", response.get('snapshot_id'))


def url_to_uuid(url):
    '''
        this function format the url for one acceptable
        value for the spotify api requests, in this case
        the uuid from a music or playlist
    '''
    splited = url.split('?')
    pre_url = splited[0]
    splited = pre_url.split("/")
    uuid = splited[4]
    return uuid


def url_to_uri(url):
    '''
        this function format the url for one acceptable
        value for the spotify api requests, in this case
        the uri of the music or playlist
    '''
    splited = url.split("?")
    pre_url = splited[0]
    splited = pre_url.split("/")
    uri = f"spotify:{splited[3]}:{splited[4]}"

    return uri

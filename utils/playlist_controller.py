import json


import requests
from music_manager.models import Music, Playlist
from spotify_account.models import SpotifyData


def get_playlist_overview(auth_token, user):
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
                    print("----------------------------------------------")       
                    print(f"{music}\n{music.music_name}\n{music.music_url}\n{music.music_artist}\n{music.album_url}\n{music.music_duration}\n")       
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
                    print("----------------------------------------------")
                    print(f"{music}\n{music.music_name}\n{music.music_artist}\n{music.music_duration}\n{music.music_url}\n{music.music_uri}\n{music.album}\n{music.album_url}")       
                next_call = True
                url = tracks = response['next']


def insert_music(music_url, playlist_url, auth_token):   
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
    print(request)
    response = request.json()

    if response.get('snapshot_id') != None:
        print("Success", response.get('snapshot_id'))  
    else:
        print(response)

def delete_music(music_url, playlist_url, auth_token):
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
    print(request)
    response = request.json()

    if response.get('snapshot_id') != None:
        print("Success", response.get('snapshot_id'))


def url_to_uuid(url):
    splited = url.split('?')
    pre_url = splited[0]
    splited = pre_url.split("/")
    uuid = splited[4]
    return uuid


def url_to_uri(url):
    splited = url.split("?")
    pre_url = splited[0]
    splited = pre_url.split("/")
    uri = f"spotify:{splited[3]}:{splited[4]}"

    return uri

if __name__ == '__main__':
    playlist="https://open.spotify.com/playlist/0PfsxAklcBs7DZPxZkB6zB"
    get_playlist(playlist)
    music_link="https://open.spotify.com/track/1jWJcuTUgO99gntArSPmrB?si=e2048993a1784679" 
    insert_music(music_link, playlist)
    delete_music(music_link, playlist)

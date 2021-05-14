from django.urls import path
from music_manager import views


urlpatterns = [
    path('', views.HomeTemplateView.as_view(), name='home'),
    path(
            'playlist_register',
            views.PostPlaylist.as_view(),
            name='playlist_register'
        ),
    path(
            'sync_playlist',
            views.SyncPlaylistData.as_view(),
            name='sync_playlist'
        ),
    path(
            'my_playlist',
            views.MyPlaylistDetailView.as_view(),
            name='my_playlist'
        ),
    path(
            '<int:pk>/playlist_switch',
            views.PlaylistSwitchUpdateView.as_view(),
            name='playlist_switch'
        ),
    path(
            'no_playlist',
            views.NoPlaylistTemplateView.as_view(),
            name='no_playlist'
        ),
    path(
            'sync_tracks',
            views.SyncMusicData.as_view(),
            name='sync_tracks'
        ),
    path(
            'tracks',
            views.MusicListView.as_view(),
            name='tracks'
        ),
    path(
            'insert_music',
            views.PostMusicCreateView.as_view(),
            name='insert_music'
        ),
    path(
            '<int:pk>/delete_music',
            views.RemoveMusicDeleteView.as_view(),
            name='delete_music'
        ),
]
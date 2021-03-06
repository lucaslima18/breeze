from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView)

from django.views.generic.edit import UpdateView
from spotify_account.models import SpotifyData
from utils.playlist_controller import (delete_music, get_playlist_overview,
                                       get_playlist_tracks, insert_music)
from utils.spotify_auth import get_auth_token, refresh_auth_token

from music_manager.models import Music, Playlist


class HomeTemplateView(LoginRequiredMixin, TemplateView):
    '''
        this model will run some checks to see if the 
        user has the updated auth token of the spotify api,
        if not, the system will generate a new one. if the
        user is logged in but has not yet authorized the
        application it will redirect to the spotify
        authentication screen. a check is also made for
        the existence of a registered playlist, if not, the
        site will direct the user to a screen where he can
        register his playlist.
    '''

    template_name = 'index.html'
    login_url = 'login'

    def get(self, *args, **kwargs):
        resp = super().get(*args, **kwargs)
        try:
            Playlist.objects.get(user=user)
            user = self.request.user
            code = self.request.GET.get('code')
            user = self.request.user
            auth_token = get_auth_token(code, user)

            if auth_token is not None:
                return resp
            return redirect(reverse_lazy('create_code'))

        except:
            user = self.request.user
            code = self.request.GET.get('code')
            user = self.request.user
            auth_token = get_auth_token(code, user)

            if auth_token.get('error') is not None:
                return resp
            else:
                return redirect(reverse_lazy('no_playlist'))


class NoPlaylistTemplateView(LoginRequiredMixin, TemplateView):
    '''
        view to redirect users to register playlist
    '''

    template_name = 'music_manager/no_playlist.html'
    login_url = 'login'


class SyncPlaylistData(LoginRequiredMixin, TemplateView):
    '''
        View for update the playlist data
    '''
    template_name = 'index.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)     

        user = self.request.user
        spotify_data = SpotifyData.objects.get(user=user)
        refresh_token = spotify_data.refresh_token
        refresh_auth_token(refresh_token, user)

        auth_token = SpotifyData.objects.get(user=user)
        auth_token = auth_token.auth_token
        get_playlist_overview(auth_token, user)     

        return context


class SyncMusicData(LoginRequiredMixin, TemplateView):
    '''
        View for update the music data
    '''
    template_name = 'music_manager/music_list.html'
    login_url = 'login'

    def get(self, *args, **kwargs):    
        user = self.request.user
        spotify_data = SpotifyData.objects.get(user=user)
        playlist = Playlist.objects.get(user=user)
        playlist_url = playlist.playlist_url
        refresh_token = spotify_data.refresh_token
        refresh_auth_token(refresh_token, user)

        auth_token = SpotifyData.objects.get(user=user)
        auth_token = auth_token.auth_token
        get_playlist_tracks(playlist_url, auth_token, user)   

        return redirect(reverse_lazy('tracks'))


class MyPlaylistDetailView(LoginRequiredMixin, ListView):
    '''
        View for detail the playlist of user
    '''
    model = Playlist
    context_object_name = 'object'
    template_name = 'music_manager/playlist_details.html'
    login_url = 'login'

    def get_queryset(self):
        user = self.request.user
        queryset = Playlist.objects.filter(user=user)
        return queryset


class MusicListView(LoginRequiredMixin, ListView):
    '''
        list of musics from spotify api
    '''
    model = Music
    context_object_name = 'object_list'
    template_name = 'music_manager/music_list.html'
    login_url = 'login'

    def get_queryset(self):
        user = self.request.user
        queryset = Music.objects.filter(user=user)
        return queryset


class PostPlaylist(LoginRequiredMixin, CreateView):
    '''
        view for insert musics, the method form_valid
        here is used for define th user.
        when a song is added to the site, it is 
        automatically added to the playlist
    '''
    model = Playlist
    template_name = 'music_manager/playlist_register.html'
    fields = ['playlist_url']
    success_url = reverse_lazy('sync_playlist')
    login_url = 'login'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PostPlaylist, self).form_valid(form)


class PlaylistSwitchUpdateView(LoginRequiredMixin, UpdateView):
    '''
        this view allows the user to change the playlist
        he wants to monitor
    '''
    model = Playlist
    template_name = 'music_manager/playlist_register.html'
    fields = ['playlist_url']
    success_url = reverse_lazy('sync_playlist')
    login_url = 'login'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PlaylistSwitchUpdateView, self).form_valid(form)


class PlaylistData(LoginRequiredMixin, DetailView):
    '''
        this view list the user playlist data
    '''
    model = Playlist
    login_url = 'login'


class PostMusicCreateView(LoginRequiredMixin,  CreateView):
    '''
        that view use form valid function for call token
        update functions and also to post this song
        directly on spotify and in local database
    '''
    model = Music
    template_name = 'music_manager/insert_music.html'
    fields = ['music_url']
    login_url = 'login'
    success_url = reverse_lazy('sync_tracks')

    def form_valid(self, form):
        self.object = form.save(commit=False)

        # things
        user = self.request.user
        music_url = self.object.music_url

        playlist = Playlist.objects.get(user=user)
        playlist_url = playlist.playlist_url

        spotify_data = SpotifyData.objects.get(user=user)
        refresh_token = spotify_data.refresh_token
        refresh_auth_token(refresh_token, user)

        auth_token = SpotifyData.objects.get(user=user)
        auth_token = auth_token.auth_token
        insert_music(music_url, playlist_url, auth_token)

        return HttpResponseRedirect(self.get_success_url())


class RemoveMusicDeleteView(LoginRequiredMixin, DeleteView):
    '''
        that view use form valid function for call token
        update functions and also to delete this song
        directly on spotify and on local database
    '''
    model = Music
    template_name = 'music_manager/music_delete.html'
    login_url = 'login'
    success_url = reverse_lazy('sync_tracks')

    def get(self, *args, **kwargs):
        resp = super().get(*args, **kwargs)
        # things
        user = self.request.user
        music_url = self.object.music_url
        playlist = Playlist.objects.get(user=user)
        playlist_url = playlist.playlist_url
        spotify_data = SpotifyData.objects.get(user=user)
        refresh_token = spotify_data.refresh_token
        refresh_auth_token(refresh_token, user)
        auth_token = SpotifyData.objects.get(user=user)
        auth_token = auth_token.auth_token
        delete_music(music_url, playlist_url, auth_token)
        return resp

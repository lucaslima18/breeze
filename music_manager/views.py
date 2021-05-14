from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic import CreateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView

from music_manager.models import Music, Playlist
from spotify_account.models import SpotifyData
from utils.spotify_auth import get_auth_token, refresh_auth_token
from utils.playlist_controller import get_playlist_overview, insert_music
from utils.playlist_controller import get_playlist_tracks, delete_music
from django.shortcuts import redirect
from django.http import HttpResponseRedirect


class HomeTemplateView(LoginRequiredMixin, TemplateView):
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
            print("NAO ACHOU")
            user = self.request.user
            code = self.request.GET.get('code')
            user = self.request.user
            auth_token = get_auth_token(code, user)

            if auth_token.get('error') is not None:
                return resp
            else:
                return redirect(reverse_lazy('no_playlist'))   


class NoPlaylistTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'music_manager/no_playlist.html'
    login_url = 'login'


class SyncPlaylistData(LoginRequiredMixin, TemplateView):
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
        print(auth_token)
        get_playlist_overview(auth_token, user)     
        return context


class SyncMusicData(LoginRequiredMixin, TemplateView):
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
        print(auth_token)
        get_playlist_tracks(playlist_url, auth_token, user)     
        return redirect(reverse_lazy('tracks'))


class MyPlaylistDetailView(LoginRequiredMixin, ListView):
    model = Playlist
    context_object_name = 'object'
    template_name = 'music_manager/playlist_details.html'
    login_url = 'login'

    def get_queryset(self):
        user = self.request.user
        queryset = Playlist.objects.filter(user=user)
        return queryset


class MusicListView(LoginRequiredMixin, ListView):
    model = Music
    context_object_name = 'object_list'
    template_name = 'music_manager/music_list.html'
    login_url = 'login'

    def get_queryset(self):
        user = self.request.user
        queryset = Music.objects.filter(user=user)
        return queryset


class PostPlaylist(LoginRequiredMixin, CreateView):
    model = Playlist
    template_name = 'music_manager/playlist_register.html'
    fields = ['playlist_url']
    success_url = reverse_lazy('sync_playlist')
    login_url = 'login'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PostPlaylist, self).form_valid(form)


class PlaylistSwitchUpdateView(LoginRequiredMixin, UpdateView):
    model = Playlist
    template_name = 'music_manager/playlist_register.html'
    fields = ['playlist_url']
    success_url = reverse_lazy('sync_playlist')
    login_url = 'login'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PostPlaylist, self).form_valid(form)


class PlaylistData(LoginRequiredMixin, DetailView):
    model = Playlist
    login_url = 'login'


class PostMusicCreateView(LoginRequiredMixin,  CreateView):
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
        print(playlist_url)
        spotify_data = SpotifyData.objects.get(user=user)
        refresh_token = spotify_data.refresh_token
        refresh_auth_token(refresh_token, user)
        auth_token = SpotifyData.objects.get(user=user)
        auth_token = auth_token.auth_token
        print(music_url)
        insert_music(music_url, playlist_url, auth_token)
        return HttpResponseRedirect(self.get_success_url())


class RemoveMusicDeleteView(LoginRequiredMixin, DeleteView):
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
        print(playlist_url)
        spotify_data = SpotifyData.objects.get(user=user)
        refresh_token = spotify_data.refresh_token
        refresh_auth_token(refresh_token, user)
        auth_token = SpotifyData.objects.get(user=user)
        auth_token = auth_token.auth_token
        print(music_url)
        delete_music(music_url, playlist_url, auth_token)
        return resp
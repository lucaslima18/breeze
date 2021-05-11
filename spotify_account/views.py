from django.views.generic import ListView, DetailView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from spotify_account.models import SpotifyData
from utils.spotify_auth import get_auth_token


class SpotifyAccountListView(ListView):
    model = SpotifyData
    template_name = 'spotify_account/account_list.html'


class SpotifyAccountDetailView(DetailView):
    model = SpotifyData
    template_name = 'spotify_account/account_data_.html'


class SpotifyAccountCreateView(CreateView):
    model = SpotifyData
    template_name = 'spotify_account/create_spotify_data.html'
    fields = ['user', 'client_id', 'client_secret', 'playlist_url']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        self.object = form.save(commit=True)
       

        # things
        token = get_auth_token(self.object.pk)
        #import pdb
        #pdb.set_trace()
        self.object.auth_token = token.get('access_token')
        self.object.save()
        return  super(SpotifyAccountCreateView, self).form_valid(form)



class SpotifyAccountUpdateView(UpdateView):
    model = SpotifyData
    template_name = 'spotify_account/update_spotify_data.html'
    fields = ['user', 'client_id', 'client_secret', 'playlist_url']
    success_url = reverse_lazy('home')  


class SpotifyAccountDeleteView(DeleteView):
    model = SpotifyData
    template_name = 'spotify_account/delete_spotify_data.html'
    success_url = reverse_lazy('home')

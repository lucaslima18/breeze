from django.urls import path
from spotify_account import views


urlpatterns = [
    path('', views.SpotifyAccountListView.as_view(), name='home'),
    path('<int:pk>', views.SpotifyAccountDetailView.as_view(), name='detail'),
    path(
            'create/',
            views.SpotifyAccountCreateView.as_view(),
            name='create'
        ),
    path('<int:pk>/update', views.SpotifyAccountUpdateView.as_view(), name='update'),
    path('<int:pk>/delete', views.SpotifyAccountDeleteView.as_view(), name='delete'),
]

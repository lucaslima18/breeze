from django.contrib import admin
from django.urls import include, path
from music_manager import views


urlpatterns = [
    path('', views.HomeTemplateView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('spotify_account/', include('spotify_account.urls')),
    path('music_manager/', include('music_manager.urls')),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('api/', include('api.urls')),
]

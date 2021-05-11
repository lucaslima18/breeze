from django.contrib import admin
from django.urls import path, include


urlpatterns = [ 
    path('admin/', admin.site.urls),
    path('spotify_account/', include('spotify_account.urls'))
]

from django.urls import path


from spotify_account import views


urlpatterns = [
    path(
        'reset_token',
        views.ResetTokenTemplateView.as_view(),
        name='reset_token'
    ),
    path('create_code/', views.get_code, name='create_code'),
]

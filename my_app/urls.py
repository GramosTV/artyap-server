from django.urls import path
from .views import ArtworkSearchView, ArtworkDetailView, random_artwork, random_artworks,art_of_the_day, login_view, logout_view , register_view, get_csrf_token # Make sure the import is correct

urlpatterns = [
    path('search/', ArtworkSearchView.as_view(), name='artwork-search'),
    path('artwork/<int:pk>/', ArtworkDetailView.as_view(), name='artwork-detail'),
    path('art-of-the-day/', art_of_the_day, name='art_of_the_day'),
    path('random-artwork/', random_artwork, name='random_artwork'),
     path('random-artworks/', random_artworks, name='random_artworks'),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('register', register_view, name='register'),
    path('csrf', get_csrf_token, name='csrf'),
]

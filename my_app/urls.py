from django.urls import path
from .views import (
    ArtworkSearchView, 
    ArtworkDetailView, 
    random_artwork, 
    random_artworks,
    art_of_the_day, 
    login_view, 
    logout_view, 
    register_view, 
    get_csrf_token, 
    add_comment, 
    get_authenticated_user, 
    trending_artworks,
    change_password,
    change_username,
)

urlpatterns = [
    path('search/', ArtworkSearchView.as_view(), name='artwork_search'),
    path('artwork/<int:pk>/', ArtworkDetailView.as_view(), name='artwork_detail'),
    path('art-of-the-day/', art_of_the_day, name='art_of_the_day'),
    path('random-artwork/', random_artwork, name='random_artwork'),
    path('random-artworks/', random_artworks, name='random_artworks'),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('register', register_view, name='register'),
    path('csrf', get_csrf_token, name='csrf'),
    path('add-comment', add_comment, name='add_comment'),
    path("auth/user/", get_authenticated_user, name="auth-user"),
    path("trending", trending_artworks, name="trending"),
    path("change-password", change_password, name="change_password"),
    path("change-username", change_username, name="change_username"),
]

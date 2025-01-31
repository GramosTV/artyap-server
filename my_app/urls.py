from django.urls import path
from .views import ArtworkSearchView, ArtworkDetailView, random_artwork, art_of_the_day  # Make sure the import is correct

urlpatterns = [
    path('search/', ArtworkSearchView.as_view(), name='artwork-search'),
    path('artwork/<int:pk>/', ArtworkDetailView.as_view(), name='artwork-detail'),
    path('art-of-the-day/', art_of_the_day, name='art_of_the_day'),
    path('random-artwork/', random_artwork, name='random_artwork'),
]

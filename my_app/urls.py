from django.urls import path
from .views import ArtworkSearchView  # Make sure the import is correct

urlpatterns = [
    path('search/', ArtworkSearchView.as_view(), name='artwork-search'),
]

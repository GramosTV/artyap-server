from rest_framework import serializers
from .models import Artwork

class ArtworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artwork
        fields = ['id', 'title', 'main_reference_number', 'artist_display', 'place_of_origin', 'dimensions', 'medium_display']

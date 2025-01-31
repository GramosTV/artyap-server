from rest_framework import serializers
from .models import Artwork, Artist

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'title', 'birth_date', 'death_date']

class ArtworkSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)

    class Meta:
        model = Artwork
        fields = ['id', 'title', 'main_reference_number', 'description', 'artist_display', 'place_of_origin', 'dimensions', 'medium_display', 'image_id', 'artist']

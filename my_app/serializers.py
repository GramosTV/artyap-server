from rest_framework import serializers
from .models import Artwork, Artist, Comment
from django.contrib.auth import get_user_model

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'title', 'birth_date', 'death_date']

class ArtworkSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)
    material_titles = serializers.JSONField()
    technique_titles = serializers.JSONField()
    theme_titles = serializers.JSONField()
    section_titles = serializers.JSONField()

    class Meta:
        model = Artwork
        fields = ['id', 'title', 'main_reference_number', 'description', 'artist_display', 'place_of_origin', 'dimensions', 'medium_display', 'image_id', 'artist', 'material_titles', 'technique_titles', 'theme_titles', 'section_titles', 'date_start', 'date_end']
        
class ArtworkIdSerializer(serializers.ModelSerializer):

    class Meta:
        model = Artwork
        fields = ['id', 'image_id']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class UserForCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username']

class CommentSerializer(serializers.ModelSerializer):
    user = UserForCommentSerializer()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'artwork', 'parent', 'text', 'created_at', 'replies']
        read_only_fields = ['user', 'created_at']

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []

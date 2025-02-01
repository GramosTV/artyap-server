from django.http import JsonResponse
from django.views import View
from .models import Artwork
from django.db.models import Q, Min, Max
from rest_framework import generics, viewsets, permissions
from .serializers import ArtworkSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
import random
from datetime import date
from django.core.cache import cache
from random import randint
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.middleware.csrf import get_token

class ArtworkSearchView(generics.ListAPIView):
    serializer_class = ArtworkSerializer

    def get_queryset(self):
        query = self.request.GET.get('title', '')
        return Artwork.objects.filter(Q(title__icontains=query))[:10]


class ArtworkDetailView(generics.RetrieveAPIView):
    queryset = Artwork.objects.all()
    serializer_class = ArtworkSerializer

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        artwork = self.get_object()
        other_artworks = Artwork.objects.filter(artist=artwork.artist).exclude(id=artwork.id).values_list('image_id', flat=True)[:5]
        response.data = {
            "data": response.data,
            "other_artworks": list(other_artworks)
        }
        return response

@api_view(['GET'])
def random_artwork(request):
    count = Artwork.objects.count()
    if count == 0:
        return Response({"error": "No artworks available"}, status=404)
    
    random_object = Artwork.objects.all()[randint(0, count - 1)]
    serializer = ArtworkSerializer(random_object)
    other_artworks = Artwork.objects.filter(artist=random_object.artist).exclude(id=random_object.id).values_list('image_id', flat=True)[:5]
    return Response({
        "data": serializer.data,
        "other_artworks": list(other_artworks)
    })

@api_view(['GET'])
def random_artworks(request):
    count = Artwork.objects.count()
    if count < 60:
        return Response({"error": "Not enough artworks available"}, status=404)
    
    random_indices = random.sample(range(count), 60)
    random_objects = [Artwork.objects.all()[i] for i in random_indices]
    serializer = ArtworkSerializer(random_objects, many=True)
    return Response(serializer.data)

class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

@api_view(['GET'])
def art_of_the_day(_request):
    today = date.today()
    cache_key = f'art_of_the_day_{today}'
    cached_artwork = cache.get(cache_key)
    
    if cached_artwork is not None:
        return Response(cached_artwork)

    min_max = Artwork.objects.aggregate(min_pk=Min('pk'), max_pk=Max('pk'))
    min_pk, max_pk = min_max['min_pk'], min_max['max_pk']
    
    if None in (min_pk, max_pk):
        return Response(status=404)

    random.seed(str(today))
    random_pk = random.randint(min_pk, max_pk)
    
    artwork = Artwork.objects.filter(pk__gte=random_pk).order_by('pk').first() or \
              Artwork.objects.filter(pk=max_pk).first()
    
    serializer = ArtworkSerializer(artwork)
    cache.set(cache_key, serializer.data, timeout=60*60*24)
    return Response(serializer.data)

@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({'message': 'Logout successful'})

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    
    if user:
        login(request, user)
        return Response({'message': 'Login successful'})
    return Response({'error': 'Invalid Credentials'}, status=400)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_view(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Registration successful'}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})
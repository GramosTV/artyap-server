from django.http import JsonResponse
from django.views import View
from .models import Artwork
from django.db.models import Q, Min, Max
from rest_framework import generics
from .serializers import ArtworkSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
import random
from datetime import date
from django.core.cache import cache
from random import randint

class ArtworkSearchView(View):
    def get(self, request):
        query = request.GET.get('title', '')
        artworks = Artwork.objects.filter(
            Q(title__icontains=query)
        )[:10]
        results = [{"title": artwork.title, "id": artwork.id} for artwork in artworks]
        return JsonResponse({"data": results})
    
class ArtworkDetailView(View):
    def get(self, request, pk):
        try:
            artwork = Artwork.objects.get(pk=pk)
        except Artwork.DoesNotExist:
            return JsonResponse({"error": "Artwork not found"}, status=404)
        
        serializer = ArtworkSerializer(artwork)
        other_artworks = Artwork.objects.filter(artist=artwork.artist).exclude(id=artwork.id).values_list('image_id', flat=True)[:5]
        return JsonResponse({
            "data": serializer.data,
            "other_artworks": list(other_artworks)
        })

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



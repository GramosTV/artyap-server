from django.http import JsonResponse
from django.views import View
from .models import Artwork
from django.db.models import Q

class ArtworkSearchView(View):
    def get(self, request):
        query = request.GET.get('name', '')
        artworks = Artwork.objects.filter(
            Q(title__icontains=query)
        )[:10]
        results = [{"title": artwork.title} for artwork in artworks]
        return JsonResponse({"results": results})

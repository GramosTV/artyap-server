import os
import json
from django.core.management.base import BaseCommand
from my_app.models import Artwork, Artist, Gallery, ArtworkType
from django.conf import settings
import re

class Command(BaseCommand):
    help = 'Imports artworks from JSON files into the database'

    def handle(self, *args, **kwargs):
        artworks_folder = os.path.join(settings.BASE_DIR, 'artic-data', 'artworks')
        for filename in os.listdir(artworks_folder):
            if filename.endswith('.json'):
                filepath = os.path.join(artworks_folder, filename)
                with open(filepath, 'r') as file:
                    data = json.load(file)
                    
                    if not data.get('image_id'):
                        continue

                    artist = None
                    if data.get('artist_id'):
                        artist, _ = Artist.objects.get_or_create(id=data['artist_id'])

                    gallery = None
                    if data.get('gallery_id'):
                        gallery, _ = Gallery.objects.get_or_create(id=data['gallery_id'])

                    artworktype = None
                    if data.get('artwork_type_id'):
                        artworktype, _ = ArtworkType.objects.get_or_create(id=data['artwork_type_id'])

                    description = data.get('description', '')
                    if description:
                        description = re.sub(r'<[^>]+>', '', description)

                    artwork_data = {
                        'title': data.get('title'),
                        'artist': artist,
                        'gallery': gallery,
                        'artworktype': artworktype,
                        'description': description,
                        'main_reference_number': data.get('main_reference_number'),
                        'date_start': data.get('date_start'),
                        'date_end': data.get('date_end'),
                        'date_display': data.get('date_display'),
                        'date_qualifier_title': data.get('date_qualifier_title'),
                        'artist_display': data.get('artist_display'),
                        'place_of_origin': data.get('place_of_origin'),
                        'short_description': data.get('short_description'),
                        'dimensions': data.get('dimensions'),
                        'medium_display': data.get('medium_display'),
                        'credit_line': data.get('credit_line'),
                        'catalogue_display': data.get('catalogue_display'),
                        'publication_history': data.get('publication_history'),
                        'exhibition_history': data.get('exhibition_history'),
                        'provenance_text': data.get('provenance_text'),
                        'edition': data.get('edition'),
                        'is_public_domain': data.get('is_public_domain'),
                        'copyright_notice': data.get('copyright_notice'),
                        'is_on_view': data.get('is_on_view'),
                        'department_id': data.get('department_id'),
                        'style_id': data.get('style_id'),
                        'image_id': data.get('image_id'),
                        'material_titles': json.dumps(data.get('material_titles', [])),  
                        'technique_titles': json.dumps(data.get('technique_titles', [])),  
                        'theme_titles': json.dumps(data.get('theme_titles', [])),  
                        'section_titles': json.dumps(data.get('section_titles', []))
                    }

                    Artwork.objects.update_or_create(
                        id=data['id'],
                        defaults=artwork_data
                    )
                self.stdout.write(self.style.SUCCESS(f'Successfully imported {filename}'))

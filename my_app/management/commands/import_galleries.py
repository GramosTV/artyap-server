import os
import json
from django.core.management.base import BaseCommand
from my_app.models import Gallery
from django.conf import settings

class Command(BaseCommand):
    help = 'Imports galleries from JSON files into the database'

    def handle(self, *args, **kwargs):
        galleries_folder = os.path.join(settings.BASE_DIR, 'artic-data', 'galleries')
        for filename in os.listdir(galleries_folder):
            if filename.endswith('.json'):
                filepath = os.path.join(galleries_folder, filename)
                with open(filepath, 'r') as file:
                    data = json.load(file)

                    gallery_data = {
                        'title': data.get('title'),
                        'latitude': data.get('latitude'),
                        'longitude': data.get('longitude'),
                        'tgn_id': data.get('tgn_id'),
                        'is_closed': data.get('is_closed', False),
                        'number': data.get('number'),
                        'floor': data.get('floor'),
                    }

                    Gallery.objects.update_or_create(
                        id=data['id'],
                        defaults=gallery_data
                    )
                
                self.stdout.write(self.style.SUCCESS(f'Successfully imported {filename}'))

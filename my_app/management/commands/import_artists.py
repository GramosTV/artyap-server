import os
import json
from django.core.management.base import BaseCommand
from my_app.models import Artist
from django.conf import settings
import re

class Command(BaseCommand):
    help = 'Imports artists from JSON files into the database'

    def handle(self, *args, **kwargs):
        artists_folder = os.path.join(settings.BASE_DIR, 'artic-data', 'agents')
        for filename in os.listdir(artists_folder):
            if filename.endswith('.json'):
                filepath = os.path.join(artists_folder, filename)
                with open(filepath, 'r') as file:
                    data = json.load(file)
                    
                    description = data.get('description', '')
                    if description:
                        description = re.sub(r'<[^>]+>', '', description)
                    
                    artist_data = {
                        'title': data.get('title'),
                        'sort_title': data.get('sort_title'),
                        'is_artist': data.get('is_artist', True),
                        'birth_date': data.get('birth_date'),
                        'death_date': data.get('death_date'),
                        'description': description,
                    }

                    Artist.objects.update_or_create(
                        id=data['id'],
                        defaults=artist_data
                    )
                self.stdout.write(self.style.SUCCESS(f'Successfully imported {filename}'))
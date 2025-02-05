import os
import json
from django.core.management.base import BaseCommand
from my_app.models import ArtworkType
from django.conf import settings

class Command(BaseCommand):
    help = 'Imports artwork types from JSON files into the database'

    def handle(self, *args, **kwargs):
        artwork_types_folder = os.path.join(settings.BASE_DIR, 'artic-data', 'artwork-types')
        for filename in os.listdir(artwork_types_folder):
            if filename.endswith('.json'):
                filepath = os.path.join(artwork_types_folder, filename)
                with open(filepath, 'r') as file:
                    data = json.load(file)

                    artwork_data = {
                        'title': data.get('title'),
                    }

                    ArtworkType.objects.update_or_create(
                        id=data['id'],
                        defaults=artwork_data
                    )

                self.stdout.write(self.style.SUCCESS(f'Successfully imported {filename}'))

from django.core.management.base import BaseCommand
import time
from my_app.bot import post_random_comment

class Command(BaseCommand):
    help = "ChatGPT bot that comments on a random artwork every minute"

    def handle(self, *args, **kwargs):
        while True:
            post_random_comment()
            time.sleep(10)
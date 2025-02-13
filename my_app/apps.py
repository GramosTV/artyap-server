import threading
import time
from django.apps import AppConfig


class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'my_app'
    
    def ready(self):
        from decouple import config
        from my_app.bot import post_random_comment
        def start_bot():
            while True:
                post_random_comment()
                time.sleep(20)
        if (config('RUN_BOT', default=False, cast=bool)):
            thread = threading.Thread(target=start_bot, daemon=True)
            thread.start()

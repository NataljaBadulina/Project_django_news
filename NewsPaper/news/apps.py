from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'      #  'simpleapp'-in lessons

    def ready(self):
        from . import signals     # выполнение модуля -> регистрация сигналов

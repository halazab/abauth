from django.apps import AppConfig


class AbauthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'abauth'
    verbose_name = 'Advanced Authentication System'

    def ready(self):
        try:
            import abauth.signals  # noqa
        except ImportError:
            pass 
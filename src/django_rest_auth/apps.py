from django.apps import AppConfig
class DjangoRestAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = "django_rest_auth"
    verbose_name = "Rest Auth"

    def ready(self):
        import django_rest_auth.signals
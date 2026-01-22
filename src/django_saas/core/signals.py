from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def create_model_list_permissions(sender, **kwargs):
    """
    Cria automaticamente permissão 'list_<modelo>'
    apenas para apps definidos em settings.MY_APPS
    """

    allowed_apps = [app.split('.')[-1] for app in getattr(settings, 'MY_APPS', [])]

    if not allowed_apps:
        return

    for model in apps.get_models():
        if model._meta.app_label not in allowed_apps:
            continue

        content_type = ContentType.objects.get_for_model(model)
        model_name = model._meta.model_name
        verbose_name = model._meta.verbose_name

        Permission.objects.get_or_create(
            codename=f'list_{model_name}',
            content_type=content_type,
            defaults={'name': f'Can list {verbose_name}'}
        )

from django.apps import apps
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def create_model_list_permissions(sender, **kwargs):
    """
    Cria automaticamente permissão 'list_<modelo>' para todos os modelos
    do projeto após as migrações.
    """
    for model in apps.get_models():
        content_type = ContentType.objects.get_for_model(model)
        model_name = model._meta.model_name  # em minúsculas
        verbose_name = model._meta.verbose_name

        perm_codename = f"list_{model_name}"
        perm_name = f"Can list {verbose_name}"

        # Cria a permissão se não existir
        Permission.objects.get_or_create(
            codename=perm_codename,
            content_type=content_type,
            defaults={'name': perm_name}
        )
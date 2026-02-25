from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver
import importlib


@receiver(post_migrate)
def create_model_list_permissions(sender, **kwargs):
    """
    Auto cria:
    ✔ list_<model>
    ✔ scaffold perms
    e adiciona tudo ao grupo Admin
    """

    # 🔥 roda apenas uma vez (evita N execuções)
    if sender.name != "django_saas":
        return

    MY_APPS = getattr(settings, "MY_APPS", []) + ["django.contrib.auth"]
    allowed_apps = [app.split(".")[-1] for app in MY_APPS]

    admin_group, _ = Group.objects.get_or_create(name="SuperAdmin")

    # ==================================================
    # MODEL LIST PERMISSIONS
    # ==================================================
    for model in apps.get_models():

        if model._meta.app_label not in allowed_apps:
            continue

        ct = ContentType.objects.get_for_model(model)

        perm, _ = Permission.objects.get_or_create(
            codename=f"list_{model._meta.model_name}",
            content_type=ct,
            defaults={"name": f"Can list {model._meta.verbose_name}"},
        )
        admin_group.permissions.add(perm)

        perm, _ = Permission.objects.get_or_create(
            codename=f"restore_{model._meta.model_name}",
            content_type=ct,
            defaults={"name": f"Can restore {model._meta.verbose_name}"},
        )
        admin_group.permissions.add(perm)

        perm, _ = Permission.objects.get_or_create(
            codename=f"hard_delete_{model._meta.model_name}",
            content_type=ct,
            defaults={"name": f"Can hard delete {model._meta.verbose_name}"},
        )
        admin_group.permissions.add(perm)


    # ==================================================
    # SCAFFOLD PERMISSIONS
    # ==================================================
    ct, _ = ContentType.objects.get_or_create(
        app_label="django_saas",
        model="command",
    )

    for codename, name in [
        ("add_modulo", "Can add modulo"),
        ("change_modulo", "Can change modulo"),
        ("view_scaffold", "Can view scaffold"),
        ("view_crud", "Can view crud"),
        ("add_scaffold", "Can add scaffold"),
        ("change_scaffold", "Can change scaffold"),
        ("delete_scaffold", "Can delete scaffold"),
    ]:
        perm, _ = Permission.objects.get_or_create(
            codename=codename,
            content_type=ct,
            defaults={"name": name},
        )

        admin_group.permissions.add(perm)

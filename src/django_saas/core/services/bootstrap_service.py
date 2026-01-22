from django.contrib.auth.models import Group
from django.db import transaction

from django_saas.models.tipo_entidade import TipoEntidade
from django_saas.models.entidade import Entidade
from django_saas.models.sucursal import Sucursal
from django_saas.models.entidade_user import EntidadeUser
from django_saas.models.sucursal_user import SucursalUser
from django_saas.models.sucursal_user_group import SucursalUserGroup


class BootstrapService:

    @classmethod
    @transaction.atomic
    def run(cls, user, stdout=None, style=None):

        tipo = cls.create_tipo_entidade(stdout, style)
        entidade = cls.create_entidade(tipo, user, stdout, style)
        sucursal = cls.create_sucursal(entidade, user, stdout, style)
        grupo = cls.create_grupo(user, sucursal, stdout, style)

        return {
            "tipo_entidade": tipo,
            "entidade": entidade,
            "sucursal": sucursal,
            "grupo": grupo,
        }

    # ------------------------
    # TipoEntidade
    # ------------------------
    @staticmethod
    def create_tipo_entidade(stdout=None, style=None):
        tipo, _ = TipoEntidade.objects.get_or_create(
            nome="Saas",
            defaults={"estado": 1}
        )

        if stdout and style:
            stdout.write(style.SUCCESS(f"✔ {'TipoEntidade:':20} {tipo.nome}"))

        return tipo

    # ------------------------
    # Entidade + EntidadeUser
    # ------------------------
    @staticmethod
    def create_entidade(tipo_entidade, user, stdout=None, style=None):
        entidade, _ = Entidade.objects.get_or_create(
            nome="Mytech",
            tipo_entidade=tipo_entidade
        )

        entidade.admins.add(user)

        EntidadeUser.objects.get_or_create(
            user=user,
            entidade=entidade
        )

        if stdout and style:
            stdout.write(style.SUCCESS(f"✔ {'Entidade:':20} {entidade.nome}"))

        return entidade

    # ------------------------
    # Sucursal + SucursalUser
    # ------------------------
    @staticmethod
    def create_sucursal(entidade, user, stdout=None, style=None):
        sucursal, _ = Sucursal.objects.get_or_create(
            nome="Sede",
            entidade=entidade
        )

        SucursalUser.objects.get_or_create(
            user=user,
            sucursal=sucursal
        )

        if stdout and style:
            stdout.write(style.SUCCESS(f"✔ {'Sucursal:':20} {sucursal.nome}"))

        return sucursal

    # ------------------------
    # Grupo + SucursalUserGroup
    # ------------------------
    @staticmethod
    def create_grupo(user, sucursal, stdout=None, style=None):
        grupo, _ = Group.objects.get_or_create(name="Admin")

        user.groups.add(grupo)

        SucursalUserGroup.objects.get_or_create(
            user=user,
            sucursal=sucursal,
            group=grupo
        )

        if stdout and style:
            stdout.write(style.SUCCESS(f"✔ {'Grupo:':20} {grupo.name}"))

        return grupo

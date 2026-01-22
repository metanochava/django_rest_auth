from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from getpass import getpass
from django_saas.models.tipo_entidade import TipoEntidade
from django_saas.models.entidade import Entidade
from django_saas.models.sucursal import Sucursal
from django_saas.models.entidade_user import EntidadeUser
from django_saas.models.sucursal_user import SucursalUser
from django_saas.models.sucursal_user_group import SucursalUserGroup
from django.contrib.auth.models import Group

User = get_user_model()


class Command(BaseCommand):
    help = "Cria um superuser estático se não existir"

    def handle(self, *args, **options):
        email = "root@co.m"
        username = "root"

        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING("Superuser já existe")
            )
            return

        # 🔐 pedir password pelo teclado (sem mostrar)
        while True:
            password = getpass("Password do superuser: ")
            password_confirm = getpass("Confirme a password: ")

            if not password:
                self.stdout.write(
                    self.style.ERROR("A password não pode estar vazia")
                )
                continue

            if password != password_confirm:
                self.stdout.write(
                    self.style.ERROR("As passwords não coincidem")
                )
                continue

            break

        user = User.objects.create_superuser(
            email=email,
            username=username,
            password=password,
        )

        user.set_password(password)
        user.save()


        data = {
            "tipo_entidade": "Saas",
            "entidade": "Mytech",
            "sucursal": "Sede",
            "grupo": "Admin",
        }

        # ------------------------
        # 1. TipoEntidade
        # ------------------------
        tipo_entidade, _ = TipoEntidade.objects.get_or_create(
            nome=data["tipo_entidade"],
            defaults={"estado": 1}
        )

        # ------------------------
        # 2. Entidade
        # ------------------------
        entidade, created_entidade = Entidade.objects.get_or_create(
            nome=data["entidade"],
            tipo_entidade=tipo_entidade
        )

        # ManyToMany → DEPOIS
        entidade.admins.add(user)

        EntidadeUser.objects.get_or_create(
            user=user,
            entidade=entidade
        )

        # ------------------------
        # 3. Sucursal
        # ------------------------
        sucursal, _ = Sucursal.objects.get_or_create(
            nome=data["sucursal"],
            entidade=entidade
        )

        SucursalUser.objects.get_or_create(
            user=user,
            sucursal=sucursal
        )

        # ------------------------
        # 4. Grupo
        # ------------------------
        grupo, _ = Group.objects.get_or_create(
            name=data["grupo"]
        )

        SucursalUserGroup.objects.get_or_create(
            user=user,
            sucursal=sucursal,
            group=grupo
        )

        user.groups.add(grupo)
        self.stdout.write(self.style.HTTP_INFO(f""))
        self.stdout.write(self.style.HTTP_INFO(f""))
        self.stdout.write(self.style.HTTP_INFO(f"{'':10} {'✔ Superuser criado:'}"))
        self.stdout.write(self.style.HTTP_INFO(f""))
        self.stdout.write(self.style.HTTP_INFO(f"{'Email:':20} {user.email}"))
        self.stdout.write(self.style.SUCCESS(f"{'User:':20} {user.username}"))
        self.stdout.write(self.style.HTTP_SUCCESS(f"{'TipoEntidade:':20} {tipo_entidade.nome}"))
        self.stdout.write(self.style.HTTP_NOT_MODIFIED(f"{'Entidade:':20} {entidade.nome}"))
        self.stdout.write(self.style.HTTP_SERVER_ERROR(f"{'Sucursal:':20} {sucursal.nome}"))
        self.stdout.write(self.style.WARNING(f"{'Grupo:':20} {grupo.name}"))
        self.stdout.write(self.style.ERROR("⚠️  Guarde estas credenciais com segurança"))
        self.stdout.write(self.style.HTTP_INFO(f""))
        self.stdout.write(self.style.HTTP_INFO(f""))


       


import getpass
from django.contrib.auth import get_user_model

User = get_user_model()


class UserService:

    @staticmethod
    def get_or_create_superuser(stdout=None, style=None):
        email = "admin@saas.local"
        username = "admin"

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "username": username,
                "is_staff": True,
                "is_superuser": True,
            }
        )

        if created:
            password = getpass.getpass("🔐 Password do superuser: ")
            user.set_password(password)
            user.save()

            if stdout and style:
                stdout.write(
                    style.SUCCESS(f"✔ Superuser criado: \t {user.email} \n")
                )
                stdout.write(
                    style.NOTICE(f"👤 Username: \t {user.username} \n")
                )
        else:
            if stdout and style:
                stdout.write(
                    style.WARNING("✔  Superuser já existe \n ")
                )
                stdout.write(style.WARNING(f"✉️ Email: \t {user.email}"))
                stdout.write(style.SUCCESS(f"👤Username: \t {user.username} \n"))

        return user

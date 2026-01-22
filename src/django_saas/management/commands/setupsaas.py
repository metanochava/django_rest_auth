from django.core.management.base import BaseCommand
from django_saas.core.services.user_service import UserService
from django_saas.core.services.bootstrap_service import BootstrapService
from django_saas.core.services.idioma_service import IdiomaService
from django_saas.core.services.frontend_service import FrontEndService
from django_saas.core.services.traducao_service import TraducaoService





class Command(BaseCommand):
    help = "Bootstrap inicial do SaaS"

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("🚀 Bootstrap SaaS \n\n"))

        # 1️⃣ Superuser
        user = UserService.get_or_create_superuser(self.stdout, style=self.style)
        # 2️⃣ Estrutura base
        result = BootstrapService.run(user, stdout=self.stdout, style=self.style)
        IdiomaService.load_defaults( stdout=self.stdout, style=self.style )
        # 3️⃣ FrontEnd (Quasar, etc)
        FrontEndService.load_defaults( stdout=self.stdout,  style=self.style  )

        TraducaoService.load_defaults( stdout=self.stdout, style=self.style )


        self.stdout.write(self.style.SUCCESS("\n 🛠 ⚙️ Sistema pronto para uso\n"))

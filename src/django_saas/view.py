from django.http import HttpResponse
from django.conf import settings
import os
import stat
import subprocess



def home(request):
    return HttpResponse("Página inicial funcionando 🚀")





# 🔐 Token de segurança
DEPLOY_TOKEN = "12121212"

# 📄 Conteúdo do script (dinâmico)
DEPLOY_SCRIPT_CONTENT = """#!/bin/bash

set -e

LOCK_FILE="/tmp/deploy.lock"

if [ -f "$LOCK_FILE" ]; then
    echo "🚫 Deploy já em execução"
    exit 1
fi

trap "rm -f $LOCK_FILE" EXIT
touch $LOCK_FILE

echo "🚀 Iniciando deploy..."

# 🔥 Detectar projeto automaticamente
BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$(dirname "$BASE_DIR")")/back"

echo "📁 Projeto detectado em: $PROJECT_DIR"

cd "$PROJECT_DIR" || exit

echo "📥 Atualizando código..."
git pull

echo "🐍 Ativando ambiente virtual..."
source venv/bin/activate

echo "📦 Instalando dependências..."
pip install -r requirements.txt

echo "🗄️ Aplicando migrações..."
python manage.py migrate

echo "📁 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "🔄 Reiniciando Gunicorn..."
systemctl restart gunicorn_dev_back

echo "✅ Deploy concluído com sucesso!"
"""


def deploy(request):
    # 🔐 Segurança
    if request.GET.get("token") != DEPLOY_TOKEN:
        return HttpResponse("Unauthorized", status=403)

    path = getattr(settings, "DEPLOY_FILE_PATH", "/tmp/deploy.sh")

    try:
        # 🔍 Criar script se não existir
        if not os.path.exists(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)

            with open(path, "w") as f:
                f.write(DEPLOY_SCRIPT_CONTENT)

            # 🔐 Permissão execução
            os.chmod(path, os.stat(path).st_mode | stat.S_IEXEC)

        # 📄 Log file
        log_file = "/tmp/deploy.log"

        # 🚀 Executar em background
        subprocess.Popen(
            [path],
            stdout=open(log_file, "a"),
            stderr=subprocess.STDOUT,
        )

        return HttpResponse("🚀 Deploy iniciado com sucesso!")

    except Exception as e:
        return HttpResponse(f"❌ Erro no deploy: {str(e)}", status=500)
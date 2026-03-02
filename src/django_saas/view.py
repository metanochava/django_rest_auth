
import os
import stat
import subprocess
import json
from datetime import datetime
from django.conf import settings
from django.http import JsonResponse, HttpResponse


def home(request):
    return HttpResponse("Página inicial funcionando 🚀")


# 🔐 Token de segurança
DEPLOY_TOKEN = "12121212"
BASE_DIR = settings.BASE_DIR
PROJECT_NAME = "back"

PROJECT_DIR = f"{BASE_DIR}/{PROJECT_NAME}"
RELEASES_DIR = f"{BASE_DIR}/releases"
CURRENT_LINK = PROJECT_DIR
LOG_FILE = "/tmp/deploy.log"
STATUS_FILE = "/tmp/deploy_status.json"

# =========================
# SCRIPT DE DEPLOY (COM RELEASE)
# =========================
DEPLOY_SCRIPT = f"""#!/bin/bash
set -e

LOCK_FILE="/tmp/deploy.lock"

if [ -f "$LOCK_FILE" ]; then
    echo "🚫 Deploy já em execução"
    exit 1
fi

trap "rm -f $LOCK_FILE" EXIT
touch $LOCK_FILE

echo "🚀 Deploy iniciado..."

TIMESTAMP=$(date +%Y%m%d%H%M%S)
NEW_RELEASE="{RELEASES_DIR}/$TIMESTAMP"

echo "📁 Criando release: $NEW_RELEASE"
mkdir -p $NEW_RELEASE

echo "📥 Clonando código..."
git clone /var/www/back $NEW_RELEASE

cd $NEW_RELEASE

echo "🐍 Ativando ambiente..."
source {PROJECT_DIR}/venv/bin/activate

echo "📦 Instalando dependências..."
pip install -r requirements.txt

echo "🗄️ Migrações..."
python manage.py migrate

echo "📁 Static..."
python manage.py collectstatic --noinput

echo "🔗 Atualizando symlink..."
ln -sfn $NEW_RELEASE {CURRENT_LINK}

echo "🔄 Reiniciando Gunicorn..."
systemctl restart gunicorn_dev_back

echo "✅ Deploy concluído"
"""

# =========================
# HELPERS
# =========================
def write_status(status, message=""):
    data = {
        "status": status,
        "message": message,
        "time": datetime.now().isoformat()
    }
    with open(STATUS_FILE, "w") as f:
        json.dump(data, f)


def read_status():
    if not os.path.exists(STATUS_FILE):
        return {"status": "idle"}
    with open(STATUS_FILE) as f:
        return json.load(f)


def ensure_script(path):
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w") as f:
            f.write(DEPLOY_SCRIPT)

        os.chmod(path, os.stat(path).st_mode | stat.S_IEXEC)


# =========================
# ENDPOINT: DEPLOY
# =========================
def deploy(request):
    if request.GET.get("token") != DEPLOY_TOKEN:
        return HttpResponse("Unauthorized", status=403)

    script_path = getattr(settings, "DEPLOY_FILE_PATH", "/var/www/lib/deploy.sh")

    try:
        ensure_script(script_path)

        write_status("running", "Deploy iniciado")

        subprocess.Popen(
            [script_path],
            stdout=open(LOG_FILE, "a"),
            stderr=subprocess.STDOUT,
        )

        return JsonResponse({"message": "🚀 Deploy iniciado"})

    except Exception as e:
        write_status("error", str(e))
        return JsonResponse({"error": str(e)}, status=500)


# =========================
# ENDPOINT: STATUS
# =========================
def deploy_status(request):
    if request.GET.get("token") != DEPLOY_TOKEN:
        return HttpResponse("Unauthorized", status=403)

    return JsonResponse(read_status())


# =========================
# ENDPOINT: LOGS
# =========================
def deploy_logs(request):
    if request.GET.get("token") != DEPLOY_TOKEN:
        return HttpResponse("Unauthorized", status=403)

    if not os.path.exists(LOG_FILE):
        return HttpResponse("Sem logs ainda")

    with open(LOG_FILE) as f:
        return HttpResponse(f.read(), content_type="text/plain")


# =========================
# ENDPOINT: ROLLBACK
# =========================
def rollback(request):
    if request.GET.get("token") != DEPLOY_TOKEN:
        return HttpResponse("Unauthorized", status=403)

    releases = sorted(os.listdir(RELEASES_DIR))

    if len(releases) < 2:
        return JsonResponse({"error": "Sem versão anterior"}, status=400)

    previous = releases[-2]
    previous_path = f"{RELEASES_DIR}/{previous}"

    try:
        os.system(f"ln -sfn {previous_path} {CURRENT_LINK}")
        os.system("systemctl restart gunicorn_dev_back")

        return JsonResponse({
            "message": "Rollback realizado",
            "version": previous
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# =========================
# MULTI-TENANT (OPCIONAL)
# =========================
def deploy_tenant(request, tenant):
    if request.GET.get("token") != DEPLOY_TOKEN:
        return HttpResponse("Unauthorized", status=403)

    tenant_path = f"/var/www/{tenant}"

    if not os.path.exists(tenant_path):
        return JsonResponse({"error": "Tenant não existe"}, status=404)

    try:
        subprocess.Popen(
            ["bash", f"{tenant_path}/deploy.sh"],
            stdout=open(LOG_FILE, "a"),
            stderr=subprocess.STDOUT,
        )

        return JsonResponse({"message": f"Deploy iniciado para {tenant}"})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
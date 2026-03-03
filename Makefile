# =========================
# Makefile - MyTech / Django SaaS
# pip install bump2version
# =========================

SHELL := /bin/bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c

PY := python3
MANAGE := $(PY) src/manage.py
VENV_ACTIVATE := source venv/bin/activate
PYPROJECT := pyproject.toml

# Lê a versão do pyproject.toml (PEP621: [project].version)
define GET_VERSION
$(PY) -c "import tomli; print(tomli.load(open('$(PYPROJECT)','rb'))['project']['version'])"
endef

# =========================
# Helpers
# =========================
.PHONY: clean_pycache version env

clean_pycache:
	find . -name "__pycache__" -type d -exec rm -rf {} +

version:
	@$(call GET_VERSION)

env:
	@$(VENV_ACTIVATE); echo "✅ venv ativado"

# =========================
# Django
# =========================
.PHONY: check migrations migrate superuser supersaas run

check:
	@$(MANAGE) check

migrations:
	@$(MANAGE) makemigrations

migrate:
	@$(MANAGE) migrate

superuser:
	@$(MANAGE) createsuperuser

supersaas:
	@$(MANAGE) supersaas

run:
	@$(MANAGE) runserver 84.247.162.222:7001

# =========================
# Git - utilitários
# =========================
.PHONY: gitback gitrmc gitignoreon gitignoreoff status

status:
	git status -sb

gitback:
	git reset --soft HEAD~1

gitrmc:
	read -p "Digite o caminho do ficheiro ou pasta: " m; \
	git rm --cached "$$m"

# =========================
# Push (sem tag)
# =========================
.PHONY: push

push: clean_pycache
	bump2version patch
	git add .
	VERSION="$$( $(call GET_VERSION) )"; \
	read -p "Mensagem do commit (release: v$$VERSION - ...): " m; \
	git commit -m "release: v$$VERSION - $$m" || true; \
	git push --set-upstream origin main develop;

push: clean_pycache
	git add .
	VERSION="$$( $(call GET_VERSION) )"; \
	read -p "Mensagem do commit (release: v$$VERSION - ...): " m; \
	git commit -m "release: v$$VERSION - $$m" || true; \
	git push --set-upstream origin main;

# =========================
# Build + Upload pip (sem tag)
# =========================
.PHONY: pushpip

pushpip: push
	$(PY) -m build; \
	twine upload dist/*;

# =========================
# Release por TAG (recomendado p/ deploy automático)
# - Commit
# - Tag vX.Y.Z
# - Push branch + tag
# - Build + Upload pip
# =========================
.PHONY: upv

upv: clean_pycache
	bump2version patch; \
	git add .; \
	VERSION="$$( $(call GET_VERSION) )"; \
	read -p "Mensagem do release v$$VERSION: " m; \
	git commit -m "release: v$$VERSION - $$m" || true; \
	git tag "v$$VERSION"; \
	git push --set-upstream origin main develop; \
	git push origin "v$$VERSION"; \
	$(PY) -m build; \
	twine upload dist/*;

# =========================
# Install local editable
# =========================
.PHONY: install

install:
	pip install -e .

# =========================
# GitFlow (novo)
# =========================
.PHONY: init feature_start feature_finish release_start release_finish hotfix_start hotfix_finish

init:
	git flow init -d

feature_start:
	read -p "Nome da feature (ex: login-api): " n; \
	git flow feature start "$$n"

feature_finish:
	read -p "Nome da feature (ex: login-api): " n; \
	git flow feature finish "$$n"

release_start:
	VERSION="$$( $(call GET_VERSION) )"; \
	echo "Iniciando release v$$VERSION"; \
	git flow release start "v$$VERSION"

release_finish:
	VERSION="$$( $(call GET_VERSION) )"; \
	read -p "Mensagem do release v$$VERSION: " m; \
	git flow release finish -m "release: v$$VERSION - $$m" "v$$VERSION"; \
	git push origin main develop --tags

hotfix_start:
	read -p "Nome do hotfix (ex: fix-login): " n; \
	git flow hotfix start "$$n"

hotfix_finish:
	read -p "Nome do hotfix (ex: fix-login): " n; \
	git flow hotfix finish "$$n"; \
	git push origin main develop --tags
env:
	source venv/bin/activate; 
up:
	find . -name "__pycache__" -type d -exec rm -rf {} + ; \
	git add .; \
	VERSION=$$(python -c "import tomli; print(tomli.load(open('pyproject.toml','rb'))['project']['version'])"); \
	read -p "Mensagem do release: $$VERSION " m; \
	git commit -m "release: v$$VERSION - $$m"; \
	git push origin main; \
	python -m build; \
	twine upload dist/*; 
upgit:
	find . -name "__pycache__" -type d -exec rm -rf {} + ; \
	git add .; \
	VERSION=$$(python -c "import tomli; print(tomli.load(open('pyproject.toml','rb'))['project']['version'])"); \
	read -p "Mensagem do release: $$VERSION " m; \
	git commit -m "release: v$$VERSION - $$m"; \
	git push origin main;  
upv:
	find . -name "__pycache__" -type d -exec rm -rf {} + ; \
	git add .; \
	VERSION=$$(python -c "import tomli; print(tomli.load(open('pyproject.toml','rb'))['project']['version'])"); \
	read -p "Mensagem do release: " m; \
	git commit -m "release: v$$VERSION - $$m"; \
	git tag v$$VERSION; \
	git push origin main; \
	git push origin v$$VERSION; \
	python -m build; \
	twine upload dist/*; 
install:
	pip install -e .;

check:
	python3 src/manage.py check ;
migrations:
	python3 src/manage.py makemigrations ;
migrate:
	python3 src/manage.py migrate ;
superuser:
	python3 src/manage.py createsuperuser ;
supersaas:
	python3 src/manage.py supersaas ;
run:
	python3 src/manage.py runserver 84.247.162.222:12121 ;
gitback:
	git reset --soft HEAD~1
gitrmc:
	read -p "Digite o caminho do ficheiro ou pasta " m; \
	git rm --cached $$m

env:
	pip install -e .
up:
	git add .; \
	VERSION=$$(python -c "import tomli; print(tomli.load(open('pyproject.toml','rb'))['project']['version'])"); \
	read -p "Mensagem do release: $$VERSION " m; \
	git commit -m "release: v$$VERSION - $$m"; \
	git push origin main; \
	python -m build; \
	twine upload dist/*; 
upgit:
	git add .; \
	VERSION=$$(python -c "import tomli; print(tomli.load(open('pyproject.toml','rb'))['project']['version'])"); \
	read -p "Mensagem do release: $$VERSION " m; \
	git commit -m "release: v$$VERSION - $$m"; \
	git push origin main;  
upv:
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
run:
	python3 src/manage.py runserver 84.247.162.222:12121 ;

gitback:
	git reset --soft HEAD~1
gitrmcomited:
	git rm --cached folder_file
up:
	git add .; \
	VERSION=$$(python -c "import tomli; print(tomli.load(open('pyproject.toml','rb'))['project']['version'])"); \
	read -p "Mensagem do release: $$VERSION " m; \
	git commit -m "release: v$$VERSION - $$m"; \
	git push origin main; \
	python -m build; \
	twine upload dist/*; \
upv:
	git add .; \
	VERSION=$$(python -c "import tomli; print(tomli.load(open('pyproject.toml','rb'))['project']['version'])"); \
	read -p "Mensagem do release: " m; \
	git commit -m "release: v$$VERSION - $$m"; \
	git tag v$$VERSION; \
	git push origin main; \
	git push origin v$$VERSION; \
	python -m build; \
	twine upload dist/*; \
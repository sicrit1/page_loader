install:
	poetry install

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user dist/*.whl

lint:
	poetry run flake8 page_loader

uninstall-code:
	python3 -m pip uninstall hexlet-code

pytest:
	poetry run pytest

coverage:
	poetry run pytest --cov=page_loader

cc-coverage:
	poetry run pytest --cov=page_loader --cov-report xml

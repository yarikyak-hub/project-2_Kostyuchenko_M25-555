install:
	poetry install
project:
	poetry run project
build:
	poetry build
publish:
	poetry publish --dry-run
package-install:
	python3 -m pip install dist/*.whl
fix:
	poetry run ruff check --fix .
lint:
	poetry run ruff check .
database:
	poetry run database
pipx-install:
	pipx install dist/*.whl

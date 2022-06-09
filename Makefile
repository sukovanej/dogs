.PHONY: test

test:
	poetry run pytest tests

test-cov:
	poetry run pytest --cov dogs tests

mypy:
	poetry run mypy dogs --show-traceback

format:
	poetry run black dogs/ tests/
	poetry run isort dogs/ tests/

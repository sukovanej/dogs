.PHONY: test

test:
	poetry run pytest tests

mypy:
	poetry run mypy dogs --show-traceback

format:
	poetry run black dogs/ tests/

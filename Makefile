.PHONY: test

test:
	poetry run pytest tests

test-cov:
	poetry run pytest --cov dogs tests

mypy:
	poetry run mypy dogs

format:
	poetry run black dogs/ tests/
	poetry run isort dogs/ tests/

clean:
	find dogs -name "*.pyc" -exec rm {} \;
	find dogs -name "__pycache__" -exec rm -rf {} \;

	find tests -name "*.pyc" -exec rm {} \;
	find tests -name "__pycache__" -exec rm -rf {} \;

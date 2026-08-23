.PHONY: install dev test lint docker-build docker-run compose-up compose-down clean

install:
	uv venv .venv
	uv pip install --python .venv/bin/python -r requirements-dev.txt

dev:
	uv run --python .venv/bin/python uvicorn app.main:app --reload --port 8000

test:
	uv run --python .venv/bin/python pytest -v

lint:
	uv run --python .venv/bin/python ruff check .

docker-build:
	docker build -t practice-app .

docker-run:
	docker run --rm -p 8000:8000 --env-file .env practice-app

compose-up:
	docker compose up --build

compose-down:
	docker compose down

clean:
	rm -rf .venv .pytest_cache .ruff_cache **/__pycache__

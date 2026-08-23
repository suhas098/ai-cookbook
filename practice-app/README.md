# practice-app

A small FastAPI task API. It's deliberately simple - the point isn't the app,
it's using it as a sandbox to practice two things:

1. **DevOps mechanics**: running a service locally, containerizing it,
   wiring up CI, health/readiness checks, structured logging, config via
   environment variables.
2. **Claude Code workflows**: giving Claude a small, well-scoped codebase and
   practicing prompts like "add an endpoint," "write a test for this," "add
   a Dockerfile step," "review this diff."

## What's here

```
practice-app/
├── app/
│   ├── main.py          # FastAPI app, request logging middleware
│   ├── config.py         # env-based settings
│   ├── models.py          # Pydantic models
│   ├── store.py            # in-memory data layer
│   └── routers/
│       ├── health.py        # /health, /ready, /version
│       └── tasks.py          # /tasks CRUD
├── tests/                # pytest + FastAPI TestClient
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── requirements.txt
└── requirements-dev.txt
```

CI lives at the repo root: `.github/workflows/practice-app-ci.yml`, scoped
to run only when files under `practice-app/` change. It lints (ruff), tests
(pytest), then builds the Docker image.

## Endpoints

| Method | Path           | Purpose                          |
|--------|----------------|-----------------------------------|
| GET    | `/`            | Welcome message                  |
| GET    | `/health`      | Liveness probe                   |
| GET    | `/ready`       | Readiness probe                  |
| GET    | `/version`     | App name/version/env             |
| GET    | `/tasks`       | List tasks                       |
| POST   | `/tasks`       | Create a task                    |
| GET    | `/tasks/{id}`  | Get one task                     |
| PATCH  | `/tasks/{id}`  | Update a task (title and/or done) |
| DELETE | `/tasks/{id}`  | Delete a task                    |

Interactive docs at `/docs` once the app is running.

## Run locally

```bash
cd practice-app
cp .env.example .env
make install
make dev
# -> http://localhost:8000/docs
```

Without `make`:

```bash
uv venv .venv
uv pip install --python .venv/bin/python -r requirements-dev.txt
uv run --python .venv/bin/python uvicorn app.main:app --reload --port 8000
```

## Test

```bash
make test
```

## Run with Docker

```bash
make docker-build
make docker-run
```

Or with Compose (same result, one command):

```bash
make compose-up
```

## DevOps learning path

Roughly in order of difficulty - try these as exercises, ideally with Claude
Code driving the diff:

1. Add a new field to `Task` (e.g. `priority`) end to end: model, store,
   router, tests.
2. Add a `Dockerfile` build-time `ARG`/`ENV` for the version and stamp it
   into `/version`.
3. Add a `.dockerignore` rule you're missing, rebuild, and confirm the image
   shrinks.
4. Extend the CI workflow with a coverage report, or a matrix over two
   Python versions.
5. Swap `app/store.py` for a real database (SQLite is the smallest step) and
   update the tests to match.
6. Add basic rate limiting or an API key check as middleware.
7. Push the built image to a registry (GHCR is free with a GitHub repo) as a
   CI step gated on `main`.
8. Write a `docker-compose.yml` service for a second dependency (e.g.
   Postgres) and wire the app to it via `.env`.

## Claude Code practice ideas

- Ask Claude to add an endpoint and its tests in one pass, then review the
  diff yourself before accepting.
- Ask Claude to explain the request-logging middleware in `app/main.py` and
  suggest what a production version would add (correlation IDs, structured
  JSON logs, etc.).
- Ask Claude to run `/code-review` on a deliberately-introduced bug and see
  if it's caught.
- Ask Claude to containerize a change (e.g. add a new dependency) and update
  the Dockerfile/requirements together.
- Use `/init` in this folder to see what Claude Code generates for a
  project-specific `CLAUDE.md`, and compare it to the one already here.

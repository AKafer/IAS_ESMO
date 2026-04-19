# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

IAS_ESMO is a Django 5 async web application that proxies, caches, and presents medical examination session data from an external ESMO API (`profaudit.kvzrm.ru/api/v1/`). There are no Django ORM models — all data lives in Redis (fetched from the external API) or is generated on the fly into Excel exports.

## Commands

All Docker operations are run from the `ci/` directory.

```bash
# Start dev stack (PostgreSQL + Redis + app + Nginx)
cd ci && docker-compose up -d --build

# Start production stack (pulls pre-built images from DockerHub)
cd ci && docker-compose -f docker-compose.production.yml up -d

# Interactive management menu (start / backup / stop)
cd ci && ./run_esmo.sh
```

Local development without Docker:
```bash
poetry install
cd application
python manage.py migrate
python manage.py runserver
```

## Architecture

### Request Flow

```
Browser → Nginx → Gunicorn (async) → Django View → Service layer → EsmoApiClient → external API
                                                  ↕
                                               Redis cache
```

### Key Layers

**`application/externals/`** — External API client.
- `base.py`: `BaseApiClient` — async HTTPX sessions, configurable retry/backoff via `pyfailsafe`, SSL verification disabled.
- `esmo_api.py`: `EsmoApiClient` — JWT bearer auth (token from `TOKEN` env var), Redis caching, cursor-based pagination via `_fetch_paginated()`. Wrapped in a `LazyObjectProxy` so the singleton is constructed only on first use.

**`application/services/`** — Business logic (no I/O).
- `exams_handler.py`: Pairs medical tests of type 1 & 2 within each session, computes time intervals between them, filters by query parameters.
- `book_handler.py`: Builds Excel workbooks with `openpyxl` from the processed exam data.
- `common.py`: Cache key construction and query-param extraction helpers.

**`application/api/`** — Async Django views.
- `GET /` — Main exam table (login required).
- `GET /exams/` — JSON exam data; accepts `date`, `time`, `interval`, `div` query params.
- `GET /api/file/` — Stream Excel file download.
- `GET /divs/` — Cached division list.
- `GET /empls/` — Employees with data anomalies.

**`application/users/`** — Standard Django login/logout views.

**`application/core/`** — Context processors and template tags shared across apps.

### Caching Strategy

Cache keys follow the pattern `"exams_dct<>date=...&time=...&div=..."`. TTLs are configured in `settings.py`:
- `EXAM_TTL = 3600` (1 hour)
- `EMPL_TTL = 3600` (1 hour)

### Configuration

All secrets and environment-specific values come from `ci/.env`:

| Variable | Purpose |
|---|---|
| `TOKEN` | JWT bearer token for the external ESMO API |
| `SECRET_KEY` | Django secret key |
| `DEBUG` | Django debug mode |
| `POSTGRES_*` / `DB_*` | Database connection |
| `ADMIN_LOGIN/EMAIL/PASSWORD` | Superuser seeding |
| `CHECK` | Validation flag used in API views |

Tunable runtime knobs in `settings.py`: `ALLOWED_RETRIES`, `BACKOFF_SECONDS`, `ROWS_PER_PAGE`.

## CI/CD

Jenkins pipeline (`ci/jenkins/docker_build.jenkins`): builds Docker images → pushes to DockerHub (`akafer/esmo_app`, `akafer/esmo_nginx`) → deploys via SCP + SSH to `ub1:/root/app/IAS_ESMO_NEW/` → runs migrations and collectstatic remotely.
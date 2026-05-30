# 13 — Deployment & Docker

## Domains

| Service | URL |
|---------|-----|
| Frontend | `https://safraskin.online` |
| Backend API | `https://api.safraskin.online` |
| Database | Internal: `safraskin_database:5432` |

## Easypanel Setup

### 1. PostgreSQL (existing)

- Service name: `safraskin_database`
- Database: `safraskin`
- Internal URL: `postgres://postgres:s4eagoems3oueizu0h00@safraskin_database:5432/safraskin?sslmode=disable`

### 2. Backend Service

- **Source:** GitHub repo `/backend`
- **Dockerfile:** `backend/Dockerfile`
- **Domain:** `api.safraskin.online` → port 8000
- **Env:** See [env/backend.env.example](./env/backend.env.example)
- **Health check:** `GET /health`

### 3. Frontend Service

- **Source:** GitHub repo `/frontend`
- **Dockerfile:** `frontend/Dockerfile`
- **Domain:** `safraskin.online` + `www.safraskin.online` → port 3000
- **Build args:** `NEXT_PUBLIC_API_URL`, `NEXT_PUBLIC_SITE_URL`
- **Env:** See [env/frontend.env.example](./env/frontend.env.example)

## docker-compose.yml (Local Dev)

```yaml
# docker-compose.yml at repo root
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: safraskin
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgres://postgres:postgres@db:5432/safraskin
    depends_on:
      - db

  frontend:
    build:
      context: ./frontend
      args:
        NEXT_PUBLIC_API_URL: http://localhost:8000
        NEXT_PUBLIC_SITE_URL: http://localhost:3000
    ports:
      - "3000:3000"
    depends_on:
      - backend

volumes:
  pgdata:
```

## GitHub Push Checklist

```
/
├── .gitignore
├── README.md
├── docker-compose.yml
├── docs/
├── frontend/
│   ├── Dockerfile
│   ├── .env.example → copy from docs/env/
│   └── ...
└── backend/
    ├── Dockerfile
    ├── .env.example
    └── ...
```

## SSL

Easypanel handles Let's Encrypt for both domains.

## CORS (Backend)

```
CORS_ORIGINS=https://safraskin.online,https://www.safraskin.online
```

## CI (Optional GitHub Actions)

```yaml
# .github/workflows/ci.yml
on: [push]
jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install -r backend/requirements.txt
      - run: cd backend && python -m pytest  # if tests added
  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: cd frontend && npm ci && npm run build
```

## Migrations on Deploy

Backend container runs `alembic upgrade head` on startup before uvicorn — no manual step.

## Logs

- Backend: structured JSON logs for orders + CAPI responses
- Frontend: Next.js standard

## Backups

- Easypanel Postgres backup schedule recommended daily

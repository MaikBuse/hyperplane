# Hyperplane local development commands

set dotenv-load

compose := "docker compose -f docker-compose-local.yml"

# List available recipes
default:
    @just --list

# --- Setup ---

# First-time setup: copy .env files, generate secrets, install deps
setup:
    ./setup.sh

# --- Infrastructure ---

# Start all infrastructure (db, redis, rabbitmq, minio, api, worker)
up *args:
    {{ compose }} up -d {{ args }}

# Stop all infrastructure
down *args:
    {{ compose }} down {{ args }}

# Restart all infrastructure
restart *args:
    {{ compose }} restart {{ args }}

# Show logs (optionally for a specific service)
logs *args:
    {{ compose }} logs -f {{ args }}

# Show running containers
ps:
    {{ compose }} ps

# --- Frontend ---

# Start all frontend dev servers (web, admin, space, live)
dev:
    pnpm dev

# Build all packages
build:
    pnpm turbo run build

# --- Checks ---

# Run all frontend checks (format + lint + types)
check:
    pnpm turbo run check

# Auto-fix frontend format and lint issues
fix:
    pnpm turbo run fix

# Run all backend checks (lint + format + unit tests)
check-api:
    cd apps/api && ruff check . && ruff format --check . && pytest -m "unit"

# Lint Python code
lint-api:
    cd apps/api && ruff check .

# Format Python code
fmt-api:
    cd apps/api && ruff format .

# Run backend unit tests
test-api *args:
    cd apps/api && pytest -m "unit" {{ args }}

# Run all checks (frontend + backend)
check-all: check check-api

# --- Database ---

# Run Django migrations
migrate *args:
    {{ compose }} exec api python manage.py migrate --settings=plane.settings.local {{ args }}

# Create a new migration
makemigrations *args:
    {{ compose }} exec api python manage.py makemigrations --settings=plane.settings.local {{ args }}

# Open a Django shell inside the API container
shell:
    {{ compose }} exec api python manage.py shell --settings=plane.settings.local

# Open a psql shell
db-shell:
    {{ compose }} exec plane-db psql -U plane -d plane

# --- Auth ---

# Open dev login in browser (bypasses Zitadel)
login:
    #!/usr/bin/env bash
    url="http://localhost:8000/auth/dev-login/"
    echo "Opening $url"
    xdg-open "$url" 2>/dev/null || open "$url" 2>/dev/null || echo "Visit: $url"

# --- Cleanup ---

# Remove all containers and volumes (destructive!)
[confirm("This will delete all local data. Continue?")]
nuke:
    {{ compose }} down -v

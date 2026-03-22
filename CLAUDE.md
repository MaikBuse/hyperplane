# Hyperplane

## Definition of Done

Before considering any change complete, all of the following must pass:

### Frontend (TypeScript/React)
1. `pnpm turbo run check:format` — code is properly formatted (Oxfmt)
2. `pnpm turbo run check:lint` — no linting errors (Oxlint)
3. `pnpm turbo run check:types` — no type errors (TypeScript)

### Backend (Python/Django)
4. `cd apps/api && ruff check .` — no linting errors
5. `cd apps/api && ruff format --check .` — code is properly formatted
6. `cd apps/api && pytest -m "unit"` — all unit tests pass

### All Changes
7. Commit messages follow Conventional Commits format

## Project Structure

- **apps/web** — Main web application (React/Vite, port 3000)
- **apps/admin** — Instance admin panel (React, port 3001, path `/god-mode`)
- **apps/space** — Public project spaces (React, port 3002, path `/spaces`)
- **apps/live** — Real-time collaboration server (Node.js, port 3100)
- **apps/api** — Django REST API backend (port 8000)
- **packages/** — Shared monorepo packages (ui, types, services, editor, etc.)
- **charts/hyperplane/** — Helm chart for Kubernetes deployment

## Key Commands

### Frontend
- `pnpm turbo run check` — run all checks (format + lint + types)
- `pnpm turbo run fix` — auto-fix format and lint issues
- `pnpm turbo run build` — build all packages
- `pnpm turbo run test` — run frontend tests (vitest in apps/live)

### Backend
- `cd apps/api && ruff check .` — lint Python code
- `cd apps/api && ruff format .` — format Python code
- `cd apps/api && pytest -m "unit"` — run unit tests
- `cd apps/api && pytest -m "contract"` — run contract/API tests
- `cd apps/api && pytest` — run all tests
- `cd apps/api && python run_tests.py -u` — run unit tests via helper script
- `cd apps/api && python run_tests.py -o` — run tests with coverage

## Authentication

Hyperplane uses Zitadel as the sole identity provider via OIDC. Roles (Admin/Member/Guest) are managed in-app.
- Backend provider: `apps/api/plane/authentication/provider/oidc/zitadel.py`
- Config: `ZITADEL_ISSUER_URL`, `ZITADEL_CLIENT_ID`, `ZITADEL_CLIENT_SECRET`

## Conventions

- **Commit messages**: Conventional Commits (`feat:`, `fix:`, `docs:`, etc.)
- **JS/TS line length**: 120 characters (Oxfmt)
- **Python line length**: 120 characters (Ruff)
- **Python indent**: 4 spaces
- **JS/TS indent**: 2 spaces

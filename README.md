# FastAPI Web App

Minimal, working FastAPI backend + zero-build React front end.

## Stack
- **Backend**: FastAPI + Uvicorn (Python 3.14)
- **Front end**: React 18 (UMD via CDN) + `htm` — no npm, no build step
- **Tests**: pytest + FastAPI `TestClient`

## Layout
```
app/
  main.py            # app wiring: API routers + static mount + index route
  api/
    health.py        # GET /api/health
    items.py         # CRUD /api/items  (in-memory store)
  static/
    index.html       # React UI served at /
tests/
  test_app.py        # smoke + CRUD lifecycle tests
run.sh               # dev server launcher
requirements.txt
```

## Run
```bash
./run.sh                 # http://localhost:8000  (auto-reload on)
PORT=9000 ./run.sh       # different port
```
First time only:
```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

- UI:               http://localhost:8000/
- Swagger docs:     http://localhost:8000/docs
- Health:           http://localhost:8000/api/health

## Test
```bash
.venv/bin/pytest -q
```

## API
| Method | Path             | Description            |
|--------|------------------|------------------------|
| GET    | /api/health      | liveness               |
| GET    | /api/items       | list items             |
| GET    | /api/items/{id}  | get one                |
| POST   | /api/items       | create                 |
| PATCH  | /api/items/{id}  | update                 |
| DELETE | /api/items/{id}  | delete                 |

The `items` resource uses an in-process store so it runs with zero setup.
Swap the internals of `app/api/items.py` for a real database (SQLAlchemy,
SQLModel, etc.) without changing the HTTP contract or the front end.

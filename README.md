# Background Jobs — Stage 0

Foundation for a background job processing system.

## Project Structure

```
main.py          # FastAPI application
jobs.py          # In-memory job store
worker.py        # Placeholder worker functions
config.py        # Configuration values
requirements.txt # Python dependencies
```

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload
```

## Health Check

```bash
curl http://localhost:8000/health
```

Returns:

```json
{"status": "ok"}
```

## Stage 0 Scope

- In-memory job store (`create_job`, `get_job`, `update_job`)
- FastAPI health endpoint
- Placeholder worker and config

Not included yet: background tasks, Celery/Redis, AI calls, retries, authentication.

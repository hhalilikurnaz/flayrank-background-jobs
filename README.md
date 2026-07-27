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

## API

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/jobs` | Create a job (202 Accepted) |
| GET | `/jobs/{job_id}` | Get job status (404 if missing) |

## Stages

- **Stage 0** — Project foundation (job store, config, worker placeholders)
- **Stage 1** — Job creation and status lookup

Not included yet: background tasks, Celery/Redis, AI calls, retries, authentication.

# Background Jobs

Foundation for a background job processing system.

## Project Structure

```
main.py          # FastAPI application (API routes, starts background work)
jobs.py          # In-memory job store and state management
worker.py        # Job execution logic
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

## API

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/jobs` | Create a job and start background processing (202 Accepted) |
| GET | `/jobs/{job_id}` | Get job status (404 if missing) |

## Background Processing Flow

1. Client calls `POST /jobs`
2. API creates a job with status `queued`
3. API schedules `process_job(job_id)` via FastAPI `BackgroundTasks`
4. API returns **202 Accepted** immediately (does not wait for work to finish)
5. Worker picks up the job, sets status to `running`, simulates work with `time.sleep`
6. Worker marks the job `completed` (or `failed` on exception)
7. Client polls `GET /jobs/{job_id}` to check progress

## Job Lifecycle

```
queued → running → completed
                 ↘ failed
```

| Status | Meaning |
|--------|---------|
| `queued` | Job created, waiting to run |
| `running` | Worker is processing the job |
| `completed` | Finished successfully (`result` set) |
| `failed` | Error during processing (`error` set) |

## Stages

- **Stage 0** — Project foundation (job store, config, worker placeholders)
- **Stage 1** — Job creation and status lookup
- **Stage 2** — Background worker execution (non-blocking API)

Not included yet: Celery/Redis, retries, idempotency, AI calls, authentication.

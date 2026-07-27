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
| GET | `/jobs/{job_id}` | Get job status and metadata (404 if missing) |

## Background Processing Flow

1. Client calls `POST /jobs`
2. API creates a job with status `queued` and a `created_at` timestamp
3. API schedules `process_job(job_id)` via FastAPI `BackgroundTasks`
4. API returns **202 Accepted** immediately (does not wait for work to finish)
5. Worker sets status to `running` (`started_at` recorded)
6. Worker marks the job `completed` or `failed` (`completed_at` recorded)
7. Client polls `GET /jobs/{job_id}` to check progress and metadata

## Job Lifecycle

```
queued → running → completed
                 ↘ failed
```

### `queued`
Job accepted by API. Waiting for the worker to pick it up.
Timestamps: `created_at` set; `started_at` and `completed_at` are `null`.

### `running`
Worker is processing the task.
Timestamps: `started_at` set.

### `completed`
Work finished successfully. `result` contains the outcome.
Timestamps: `completed_at` set.

### `failed`
Worker encountered an error. `error` contains the message.
Timestamps: `completed_at` set.

## Stages

- **Stage 0** — Project foundation (job store, config, worker placeholders)
- **Stage 1** — Job creation and status lookup
- **Stage 2** — Background worker execution (non-blocking API)
- **Stage 3** — Lifecycle metadata and status reporting

Not included yet: Celery/Redis, retries, idempotency, AI calls, authentication.

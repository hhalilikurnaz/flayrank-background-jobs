# Background Jobs

Foundation for a background job processing system.

## Project Structure

```
main.py          # FastAPI application (API routes, starts background work)
jobs.py          # In-memory job store, state management, and locking
worker.py        # Job execution logic (with retries and locks)
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

### Create a job

```bash
curl -X POST http://localhost:8000/jobs
```

Force a failing job (for retry testing):

```bash
curl -X POST http://localhost:8000/jobs \
  -H "Content-Type: application/json" \
  -d '{"should_fail": true}'
```

## Background Processing Flow

1. Client calls `POST /jobs`
2. API creates a job with status `queued`, `locked: false`, and `attempts: 0`
3. API schedules `process_job(job_id)` via FastAPI `BackgroundTasks`
4. API returns **202 Accepted** immediately
5. Worker acquires the job lock, then runs attempts (up to `MAX_RETRIES`)
6. On success → `completed`; after all retries fail → `failed`
7. Worker releases the lock (always, via `try`/`finally`)
8. Client polls `GET /jobs/{job_id}` for status and metadata

## Job Lifecycle

```
queued → running → completed
                 ↘ failed
```

### `queued`
Job accepted by API. Waiting for the worker to pick it up.

### `running`
Worker is processing the task.

### `completed`
Work finished successfully. `result` contains the outcome.

### `failed`
Worker exhausted retries. `error` retains the last error message.

## Retry Lifecycle

```
running
  ↓
failure
  ↓
retry (attempts++)
  ↓
completed  OR  failed (after MAX_RETRIES)
```

- Each attempt increments `attempts` and re-enters `running`
- Maximum attempts: `MAX_RETRIES` (default **3**) from `config.py`
- Intermediate failures store the error message but keep retrying
- After the final failed attempt, status becomes `failed` and `error` is kept
- Successful jobs stop retrying immediately

## Idempotency

Jobs cannot be processed concurrently twice.

- Before execution, the worker calls `acquire_job_lock(job_id)`
- If the job is already locked, the second worker exits immediately without changing state
- Only one worker runs the job; results are not duplicated
- The lock is always released after completion or failure (`try`/`finally`)

```
worker A: acquire lock → process → release lock
worker B: acquire lock fails → exit (no state change)
```

## Configuration

| Setting | Default | Meaning |
|---------|---------|---------|
| `JOB_PROCESSING_DELAY` | `5` | Simulated work duration (seconds) |
| `MAX_RETRIES` | `3` | Maximum execution attempts per job |

## Stages

- **Stage 0** — Project foundation (job store, config, worker placeholders)
- **Stage 1** — Job creation and status lookup
- **Stage 2** — Background worker execution (non-blocking API)
- **Stage 3** — Lifecycle metadata and status reporting
- **Stage 4** — Retry handling and failure management
- **Stage 5** — Idempotency via job locking

Not included yet: Celery/Redis, database persistence, AI calls, authentication.

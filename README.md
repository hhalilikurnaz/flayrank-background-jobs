# FlyRank Background Jobs

## Case Study: Building a Reliable Background Job Processing System

## Problem

Many backend systems need to execute operations that are too slow to run inside a normal HTTP request.

Examples:

- AI model calls
- Report generation
- Large file processing
- External API integrations
- Data processing tasks

Running these operations directly inside an API request creates problems:

- Slow response times
- Request timeouts
- Poor user experience
- Difficult failure management

A more scalable approach is:

**Accept the request quickly → Process asynchronously → Report the result**

---

# Solution Overview

This project implements a background job processing pattern.

Instead of keeping the client waiting for a long-running operation:

1. Client submits a job.
2. API creates a job record.
3. API immediately returns `202 Accepted`.
4. Background worker processes the task.
5. Client checks job status separately.

The system demonstrates:

- Background execution
- Job lifecycle tracking
- Retry handling
- Failure management
- Idempotent processing

---

# Architecture

```text
Client
  |
  | POST /jobs
  ↓
FastAPI API
  |
  | Create Job
  ↓
Job Store
  |
  | Background Worker
  ↓
Processing
  |
  ↓
Completed / Failed
```

Execution flow:

1. The client sends a job request.
2. The API creates a queued job.
3. The worker executes the operation asynchronously.
4. Job state is updated during processing.
5. The client retrieves the result through the status endpoint.

---

# Engineering Decisions

## 1. Asynchronous Processing

### Problem

Long-running operations should not block HTTP requests.

### Decision

The API only accepts the task and delegates execution to a background worker.

The endpoint responds immediately:

```
POST /jobs

→ 202 Accepted
→ background processing starts
```

This keeps the API responsive.

---

## 2. Job Lifecycle Tracking

Each job maintains its execution state:

```
queued
   ↓
running
   ↓
completed
```

or:

```
queued
   ↓
running
   ↓
failed
```

Supported states:

| Status | Description |
|---|---|
| `queued` | Job accepted and waiting for processing |
| `running` | Worker is executing the task |
| `completed` | Processing finished successfully |
| `failed` | Processing failed after retries |

Jobs also track:

- `created_at`
- `started_at`
- `completed_at`
- `attempts`
- `locked`

---

# Retry and Failure Handling

Background jobs can fail because of:

- Temporary network errors
- External service failures
- Unexpected runtime errors

The worker retries failed operations automatically.

Lifecycle:

```
running
   ↓
failure
   ↓
retry attempt
   ↓
completed OR failed
```

Features:

- Configurable maximum retries
- Attempt counter tracking
- Error message preservation
- Final failure state

Configuration:

```python
MAX_RETRIES = 3
```

---

# Idempotency

A production system must assume:

> The same job can be triggered more than once.

Without protection:

```
Worker A → executes job
Worker B → executes same job again
```

This can create duplicate operations.

To prevent this, jobs use locking.

Flow:

```
Worker 1
   |
 acquire lock ✅
   |
 process job


Worker 2
   |
 acquire lock ❌
   |
 stop
```

The lock is always released after completion or failure.

---

# API Documentation

## Create Job

### POST `/jobs`

Creates a new background job.

Response:

```
202 Accepted
```

Example:

```json
{
  "id": "uuid",
  "status": "queued",
  "result": null,
  "error": null
}
```

Failure simulation for testing:

```bash
curl -X POST http://localhost:8000/jobs \
-H "Content-Type: application/json" \
-d '{"should_fail": true}'
```

---

## Check Job Status

### GET `/jobs/{job_id}`

Returns the current job state.

Response example:

```json
{
  "id": "uuid",
  "status": "completed",
  "result": "Job completed successfully",
  "error": null
}
```

Returns:

- `200` if job exists
- `404` if job is missing

---

## Health Check

### GET `/health`

Response:

```json
{
  "status": "ok"
}
```

---

# File Responsibilities

| File | Responsibility |
|---|---|
| `main.py` | API routes and starting background execution |
| `jobs.py` | Job storage, lifecycle management, locking |
| `worker.py` | Background execution, retries, failures |
| `config.py` | Worker and retry configuration |

---

# Running Locally

Create environment:

```bash
python -m venv .venv
```

Activate:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run API:

```bash
uvicorn main:app --reload
```

Open:

```
http://localhost:8000/docs
```

---

# Project Structure

```
.
├── main.py
├── jobs.py
├── worker.py
├── config.py
├── requirements.txt
└── README.md
```

---

# Configuration

| Setting | Default | Description |
|---|---|---|
| `JOB_PROCESSING_DELAY` | `5` | Simulated long-running operation duration |
| `MAX_RETRIES` | `3` | Maximum retry attempts |

---

# Future Production Improvements

This project currently uses an in-memory job store for learning and demonstration.

A production-ready version could add:

- Redis Queue / Celery
- Persistent database storage
- Distributed workers
- Job monitoring dashboard
- Alerting system
- Metrics and tracing
- Dead letter queues

The goal of this project is to demonstrate the core architecture behind reliable asynchronous processing systems.
"""In-memory job store for background job processing."""

from uuid import uuid4

_jobs: dict[str, dict] = {}


def create_job() -> dict:
    """Create a new job and store it in memory."""
    job = {
        "id": str(uuid4()),
        "status": "queued",
        "result": None,
        "error": None,
    }
    _jobs[job["id"]] = job
    return job


def get_job(job_id: str) -> dict | None:
    """Retrieve a job by ID. Returns None if not found."""
    return _jobs.get(job_id)


def update_job(job_id: str, data: dict) -> dict | None:
    """Update an existing job with the given data. Returns None if not found."""
    job = _jobs.get(job_id)
    if job is None:
        return None
    job.update(data)
    return job

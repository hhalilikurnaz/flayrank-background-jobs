"""In-memory job store for background job processing."""

from datetime import datetime, timezone
from uuid import uuid4

_jobs: dict[str, dict] = {}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def create_job() -> dict:
    """Create a new job and store it in memory."""
    job = {
        "id": str(uuid4()),
        "status": "queued",
        "result": None,
        "error": None,
        "created_at": _now_iso(),
        "started_at": None,
        "completed_at": None,
    }
    _jobs[job["id"]] = job
    return job


def get_job(job_id: str) -> dict | None:
    """Retrieve a job by ID. Returns None if not found."""
    return _jobs.get(job_id)


def update_job(job_id: str, data: dict) -> dict | None:
    """Update an existing job with the given data. Returns None if not found.

    Automatically sets started_at when status becomes running,
    and completed_at when status becomes completed or failed.
    """
    job = _jobs.get(job_id)
    if job is None:
        return None

    new_status = data.get("status")
    if new_status == "running":
        data = {**data, "started_at": _now_iso()}
    elif new_status in ("completed", "failed"):
        data = {**data, "completed_at": _now_iso()}

    job.update(data)
    return job

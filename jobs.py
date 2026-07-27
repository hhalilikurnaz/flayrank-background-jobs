"""In-memory job store for background job processing."""

import threading
from datetime import datetime, timezone
from uuid import uuid4

_jobs: dict[str, dict] = {}
_lock = threading.Lock()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def create_job(should_fail: bool = False) -> dict:
    """Create a new job and store it in memory."""
    job = {
        "id": str(uuid4()),
        "status": "queued",
        "result": None,
        "error": None,
        "created_at": _now_iso(),
        "started_at": None,
        "completed_at": None,
        "attempts": 0,
        "locked": False,
        "should_fail": should_fail,
    }
    _jobs[job["id"]] = job
    return job


def get_job(job_id: str) -> dict | None:
    """Retrieve a job by ID. Returns None if not found."""
    return _jobs.get(job_id)


def update_job(job_id: str, data: dict) -> dict | None:
    """Update an existing job with the given data. Returns None if not found.

    Automatically sets started_at on first transition to running,
    and completed_at when status becomes completed or failed.
    """
    job = _jobs.get(job_id)
    if job is None:
        return None

    new_status = data.get("status")
    if new_status == "running" and job.get("started_at") is None:
        data = {**data, "started_at": _now_iso()}
    elif new_status in ("completed", "failed"):
        data = {**data, "completed_at": _now_iso()}

    job.update(data)
    return job


def acquire_job_lock(job_id: str) -> bool:
    """Try to lock a job for exclusive processing.

    Returns False if the job does not exist or is already locked.
    """
    with _lock:
        job = _jobs.get(job_id)
        if job is None:
            return False
        if job.get("locked"):
            return False
        job["locked"] = True
        return True


def release_job_lock(job_id: str) -> None:
    """Release the processing lock on a job."""
    with _lock:
        job = _jobs.get(job_id)
        if job is None:
            return
        job["locked"] = False

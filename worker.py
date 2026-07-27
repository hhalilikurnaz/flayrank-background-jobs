"""Background worker for job execution."""

import time

import config
import jobs


def process_job(job_id: str) -> None:
    """Execute a job in the background.

    Lifecycle: queued → running → completed | failed
    """
    job = jobs.get_job(job_id)
    if job is None:
        return

    jobs.update_job(job_id, {"status": "running"})

    try:
        time.sleep(config.JOB_PROCESSING_DELAY)
        jobs.update_job(
            job_id,
            {
                "status": "completed",
                "result": "Job completed successfully",
            },
        )
    except Exception as exc:
        jobs.update_job(
            job_id,
            {
                "status": "failed",
                "error": str(exc),
            },
        )

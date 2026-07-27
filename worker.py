"""Background worker for job execution."""

import time

import config
import jobs


def process_job(job_id: str) -> None:
    """Execute a job in the background with retry handling.

    Lifecycle: queued → running → (retry on failure) → completed | failed
    """
    job = jobs.get_job(job_id)
    if job is None:
        return

    last_error: str | None = None

    for _ in range(config.MAX_RETRIES):
        job = jobs.get_job(job_id)
        if job is None:
            return

        attempts = job.get("attempts", 0) + 1
        jobs.update_job(job_id, {"attempts": attempts, "status": "running"})

        try:
            time.sleep(config.JOB_PROCESSING_DELAY)

            job = jobs.get_job(job_id)
            if job is not None and job.get("should_fail"):
                raise RuntimeError("Simulated job failure")

            jobs.update_job(
                job_id,
                {
                    "status": "completed",
                    "result": "Job completed successfully",
                    "error": None,
                },
            )
            return
        except Exception as exc:
            last_error = str(exc)
            jobs.update_job(job_id, {"error": last_error})

    jobs.update_job(
        job_id,
        {
            "status": "failed",
            "error": last_error,
        },
    )

"""FastAPI application entry point."""

from fastapi import BackgroundTasks, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

import jobs
from worker import process_job

app = FastAPI(title="Background Jobs")


class JobCreate(BaseModel):
    should_fail: bool = False


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/jobs", status_code=status.HTTP_202_ACCEPTED)
def submit_job(background_tasks: BackgroundTasks, payload: JobCreate = JobCreate()):
    job = jobs.create_job(should_fail=payload.should_fail)
    background_tasks.add_task(process_job, job["id"])
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=job)


@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    job = jobs.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return job

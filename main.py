"""FastAPI application entry point."""

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse

import jobs

app = FastAPI(title="Background Jobs")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/jobs", status_code=status.HTTP_202_ACCEPTED)
def submit_job():
    job = jobs.create_job()
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=job)


@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    job = jobs.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return job

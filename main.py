"""FastAPI application entry point."""

from fastapi import FastAPI

app = FastAPI(title="Background Jobs")


@app.get("/health")
def health():
    return {"status": "ok"}

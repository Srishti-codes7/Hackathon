from fastapi import FastAPI

from app.database import init_db

from app.routers import (
    learners,
    recommend,
    evaluate
)


app = FastAPI(
    title="Adaptive Learning Engine",
    description=(
        "Personalized learning recommendation "
        "engine for EdTech platforms."
    ),
    version="1.0.0"
)


@app.on_event("startup")
def startup():

    init_db()


@app.get("/")
def root():

    return {
        "name": "Adaptive Learning Engine",
        "status": "running"
    }


app.include_router(
    learners.router
)

app.include_router(
    recommend.router
)

app.include_router(
    evaluate.router
)

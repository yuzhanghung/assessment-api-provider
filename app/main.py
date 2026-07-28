from fastapi import FastAPI

from app.database import Base, engine
from app.routes import artifacts, assessments, webhooks

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(
    assessments.router
)

app.include_router(
    artifacts.router
)

app.include_router(
    webhooks.router
)

import asyncio
import secrets
import uuid

from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel

from app.database import SessionLocal
from app.models import Assessment, WebhookEndpoint
from app.webhook import process_assessment

app = FastAPI()

class WebhookRequest(BaseModel):
    url: str
    client_id: str

class AssessmentRequest(BaseModel):
    product_id: str
    assessment_type: str
    client_id: str

@app.post("/registerWebhook", status_code=201)
def register_webhook(request: WebhookRequest):
    db = SessionLocal()

    endpoint_id = str(uuid.uuid4())
    secret = secrets.token_urlsafe(32)

    webhook = WebhookEndpoint(
        endpoint_id=endpoint_id,
        client_id=request.client_id,
        url=request.url,
        secret=secret
    )

    db.add(webhook)
    db.commit()
    db.close()


    return {
        "endpoint_id": endpoint_id,
        "secret": secret,
        "status": "registered",
        "message": "Webhook registered successfully"
    }


@app.post("/api/assessments", status_code=201)
async def create_assessment(
    request: AssessmentRequest,
    background_tasks: BackgroundTasks

):
    db = SessionLocal()

    assessment_id = str(uuid.uuid4())

    assessment = Assessment(
        assessment_id=assessment_id,
        client_id=request.client_id,
        product_id=request.product_id,
        assessment_type=request.assessment_type,
        status="submitted"
    )

    db.add(assessment)
    db.commit()
    db.close()


    background_tasks.add_task(
        process_assessment,
        assessment_id
    )

    return {
        "status": "submitted",
        "assessment_id": assessment_id,
        "message": "Assessment submitted successfully"
    }


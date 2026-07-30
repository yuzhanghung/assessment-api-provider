import secrets
import uuid

from fastapi import APIRouter
from pydantic import BaseModel

from app.database import SessionLocal
from app.models import WebhookEndpoint


router = APIRouter(
    prefix="/api/webhooks",
    tags=["webhooks"]
)


class WebhookRequest(BaseModel):
    url: str
    client_id: str


@router.post("/register", status_code=201)
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
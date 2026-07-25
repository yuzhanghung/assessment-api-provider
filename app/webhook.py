import asyncio

import httpx
from database import SessionLocal
from models import Assessment, WebhookEndpoint

from app.security import create_signature


async def send_webhook(client_id: str, assessment_id: str, status: str):

    db = SessionLocal()

    webhook_data = db.query(WebhookEndpoint).filter(
        WebhookEndpoint.client_id == client_id
    ).first()

    
    if webhook_data is None:
        print("No webhook registered")
        db.close()
        return

    payload = {
        "assessment_id": assessment_id,
        "status": status
    }

    signature = create_signature(
        payload,
        webhook_data.secret
    )

    headers = {
        "X-Hi-Signature": signature
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            webhook_data.url,
            json=payload,
            headers=headers
        )

    print(
        "Webhook sent:",
        status,
        response.status_code
    )


async def process_assessment(id: str):

    db = SessionLocal()

    assessment = db.query(Assessment).filter(
        Assessment.assessment_id == id
    ).first()

    # submitted --> pending
    await asyncio.sleep(3)

    assessment.status = "pending"
    db.commit()

    await send_webhook(
        assessment["client_id"],
        id,
        "pending"
    )

    # pending --> running
    await asyncio.sleep(5)

    assessment.status = "running"
    db.commit()

    await send_webhook(
        assessment["client_id"],
        id,
        "running"
    )


    # running --> completed
    await asyncio.sleep(10)
    
    assessment.status = "completed"
    db.commit()

    await send_webhook(
        assessment["client_id"],
        id,
        "completed"
    )

    

    


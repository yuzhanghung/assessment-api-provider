import asyncio

import httpx

from app.database import SessionLocal
from app.models import Assessment, WebhookEndpoint
from app.security import create_signature


async def send_webhook(client_id: str, assessment_id: str, status: str):
    db = SessionLocal()

    try:
        webhook_data = db.query(WebhookEndpoint).filter(
            WebhookEndpoint.client_id == client_id
        ).first()

        if webhook_data is None:
            print("No webhook registered for client:", client_id)
            return

        payload = {
            "assessment_id": assessment_id,
            "status": status,
            "client_id": client_id
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

    finally:
        db.close()


async def process_assessment(assessment_id: str):

    print("PROCESS STARTED:", assessment_id)

    db = SessionLocal()

    try:
        assessment = db.query(Assessment).filter(
            Assessment.assessment_id == assessment_id
        ).first()

        if assessment is None:
            print("Assessment not found:", assessment_id)
            return

        print("Found assessment:", assessment_id)

        client_id = assessment.client_id


        # submitted -> pending
        await asyncio.sleep(3)

        print("Sending pending webhook")

        assessment.status = "pending"
        db.commit()

        await send_webhook(
            client_id,
            assessment_id,
            "pending"
        )


        # pending -> running
        await asyncio.sleep(5)

        print("Sending running webhook")

        assessment.status = "running"
        db.commit()

        await send_webhook(
            client_id,
            assessment_id,
            "running"
        )


        # running -> completed
        await asyncio.sleep(10)

        print("Sending completed webhook")

        assessment.status = "completed"
        db.commit()

        await send_webhook(
            client_id,
            assessment_id,
            "completed"
        )


    finally:
        db.close()
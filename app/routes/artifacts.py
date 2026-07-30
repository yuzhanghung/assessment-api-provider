import os
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Artifact, Assessment
from app.storage import s3_client

get_db_dep = Depends(get_db)

router = APIRouter(
    prefix="/api/artifacts",
    tags=["artifacts"]
)

@router.post("/presigned-url")
def create_presigned_url(
    assessment_id:str, 
    filename: str,
    db: Session = get_db_dep
):
    assessment = (
        db.query(Assessment)
        .filter(
            Assessment.assessment_id == assessment_id
        )
        .first()
    )

    if not assessment:
        raise HTTPException(
            status_code=404,
            detail="Assessment not found"
        )
    
    object_key = f"artifacts/{uuid.uuid4()}-{filename}"

    artifact = Artifact(
        assessment_id=assessment_id,
        filename=filename,
        object_key=object_key,
        status="pending_upload"
    )

    db.add(artifact)
    db.commit()
    db.refresh(artifact)

    url = s3_client.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": os.getenv("S3_BUCKET_NAME"),
            "Key": object_key
        },
        ExpiresIn=600
    )

    return {
        "artifact_id": artifact.id,
        "upload_url": url,
        "object_key": object_key,
        "expires_in": 600
    }


@router.post("/{artifact_id}/complete")
def complete_upload(
    artifact_id: str,
    db: Session = get_db_dep
):
    artifact = (
        db.query(Artifact)
        .filter(Artifact.id == artifact_id)
        .first()
    )

    if not artifact:
        raise HTTPException(
            status_code=404,
            detail="Artifact not found"
        )

    artifact.status = "uploaded"

    db.commit()
    db.refresh(artifact)

    return {
        "artifact_id": artifact.id,
        "status": artifact.status
    }


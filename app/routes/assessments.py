import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel

from app.database import get_db
from app.models import Artifact, Assessment
from app.webhook import process_assessment

router = APIRouter(
    prefix="/api/assessments",
    tags=["assessments"]
)

db_dependency = Depends(get_db)

class AssessmentRequest(BaseModel):
    product_id: str
    assessment_type: str
    client_id: str


@router.post("", status_code=201)
async def create_assessment(
    request: AssessmentRequest,
    db=db_dependency
):

    assessment_id = str(uuid.uuid4())

    assessment = Assessment(
        assessment_id=assessment_id,
        client_id=request.client_id,
        product_id=request.product_id,
        assessment_type=request.assessment_type,
        status="created"
    )

    db.add(assessment)
    db.commit()

    return {
        "assessment_id": assessment_id,
        "status": "created"
    }



@router.post("/{assessment_id}/start")
def start_assessment(
    assessment_id: str,
    background_tasks: BackgroundTasks,
    db=db_dependency
):
    assessment = (
        db.query(Assessment)
        .filter(
            Assessment.assessment_id == assessment_id
        ).first()
    )

    if not assessment:
        raise HTTPException(
            status_code=404,
            detail="Assessment not found"
        )

    artifacts = (
        db.query(Artifact)
        .filter(
            Artifact.assessment_id == assessment_id
        ).all()
    )

    if not artifacts:
        raise HTTPException(
            status_code=400,
            detail="No artifacts uploaded"
        )

    for artifact in artifacts:
        if artifact.status != "uploaded":
            raise HTTPException(
                status_code=400,
                detail="Artifact uploaded incomplete"
            )

    assessment.status = "submitted"
    db.commit()

    background_tasks.add_task(
        process_assessment,
        assessment_id
    )

    return {
        "assessment_id": assessment_id,
        "status": "submitted",
        "message": "Assessment started"
    }
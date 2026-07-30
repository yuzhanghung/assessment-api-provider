import uuid

from sqlalchemy import Column, DateTime, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class WebhookEndpoint(Base):
    __tablename__ = "webhook_endpoints"

    endpoint_id = Column(String, primary_key=True)
    client_id = Column(String, nullable=False)
    url = Column(Text, nullable=False)
    secret = Column(Text, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

class Assessment(Base):
    __tablename__ = "assessments"

    assessment_id = Column(String, primary_key=True)
    client_id = Column(String, nullable=False)
    product_id = Column(String, nullable=False)
    assessment_type = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    artifacts = relationship(
        "Artifact",
        back_populates="assessment"
    )

class Artifact(Base):
    __tablename__ = "artifacts"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    assessment_id = Column(
        String,
        ForeignKey("assessments.assessment_id"),
        nullable=False
    )

    assessment = relationship(
        "Assessment",
        back_populates="artifacts"
    )

    filename = Column(
        String,
        nullable=False
    )

    object_key = Column(
        Text,
        nullable=False
    )

    status = Column(
        String,
        nullable=False,
        default="pending_upload"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
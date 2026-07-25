from database import Base
from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.sql import func


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
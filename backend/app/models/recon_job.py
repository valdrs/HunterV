from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.database import Base


class ReconJob(Base):
    __tablename__ = "recon_jobs"

    id = Column(Integer, primary_key=True, index=True)

    target_id = Column(
        Integer,
        ForeignKey("targets.id"),
        nullable=False,
    )

    job_type = Column(
        String,
        nullable=False,
        default="subdomain",
    )

    source = Column(
        String,
        nullable=False,
        default="subfinder",
    )

    status = Column(
        String,
        nullable=False,
        default="queued",
    )

    error = Column(
        Text,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    started_at = Column(
        DateTime,
        nullable=True,
    )

    completed_at = Column(
        DateTime,
        nullable=True,
    )

    target = relationship(
        "Target",
        back_populates="recon_jobs",
    )
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.database import Base


class Target(Base):
    __tablename__ = "targets"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    base_url = Column(String, nullable=False)

    program = Column(String)

    platform = Column(String)

    status = Column(String, default="New")

    notes = Column(String)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    findings = relationship(
      "Finding",
      back_populates="target",
      cascade="all, delete-orphan",
    )

    subdomains = relationship(
    "Subdomain",
    back_populates="target",
    cascade="all, delete-orphan",
    )

    recon_jobs = relationship(
    "ReconJob",
    back_populates="target",
    cascade="all, delete-orphan",
    )

    assets = relationship(
    "Asset",
    back_populates="target",
    cascade="all, delete-orphan",
    )
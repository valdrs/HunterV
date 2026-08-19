from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    )
from sqlalchemy.orm import relationship

from app.db.database import Base


class Subdomain(Base):
    __tablename__ = "subdomains"

    __table_args__ = (
        UniqueConstraint(
            "target_id",
            "hostname",
            name="uq_subdomain_target_hostname",
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    hostname = Column(
        String,
        nullable=False
    )

    status = Column(
        String,
        default="discovered"
    )

    source = Column(
        String,
        nullable=True
    )

    target_id = Column(
        Integer,
        ForeignKey("targets.id"),
        nullable=False
    )

    target = relationship(
        "Target",
        back_populates="subdomains"
    )
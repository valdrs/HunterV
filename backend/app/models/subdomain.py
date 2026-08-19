from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    )
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

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

    first_seen = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    last_seen = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
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
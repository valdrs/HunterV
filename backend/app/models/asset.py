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


class Asset(Base):
    __tablename__ = "assets"

    __table_args__ = (
        UniqueConstraint(
            "target_id",
            "hostname",
            "port",
            "protocol",
            name="uq_asset_target_hostname_port_protocol",
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    hostname = Column(
        String,
        nullable=False,
    )

    protocol = Column(
        String,
        nullable=False,
    )

    port = Column(
        Integer,
        nullable=False,
    )

    status = Column(
        String,
        default="discovered",
        nullable=False,
    )

    source = Column(
        String,
        nullable=True,
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
        nullable=False,
    )

    subdomain_id = Column(
        Integer,
        ForeignKey("subdomains.id"),
        nullable=True,
    )

    target = relationship(
        "Target",
        back_populates="assets",
    )

    subdomain = relationship(
        "Subdomain",
        back_populates="assets",
    )
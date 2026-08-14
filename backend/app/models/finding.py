from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import relationship

from app.db.database import Base


class Finding(Base):
    __tablename__ = "findings"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    severity = Column(String, default="Info")

    description = Column(Text)

    poc = Column(Text)

    poc_type = Column(String)

    status = Column(String, default="Open")

    target_id = Column(
        Integer,
        ForeignKey("targets.id"),
        nullable=False,
    )

    target = relationship(
        "Target",
        back_populates="findings",
    )
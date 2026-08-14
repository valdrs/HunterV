from sqlalchemy.orm import Session

from app.models.finding import Finding
from app.models.target import Target
from app.schemas.finding import FindingCreate, FindingUpdate


def _get_finding(
    db: Session,
    finding_id: int
) -> Finding | None:
    return (
        db.query(Finding)
        .filter(Finding.id == finding_id)
        .first()
    )


def create_finding(
    db: Session,
    finding: FindingCreate
) -> Finding | None:

    target = (
        db.query(Target)
        .filter(Target.id == finding.target_id)
        .first()
    )

    if target is None:
        return None

    db_finding = Finding(
        title=finding.title,
        severity=finding.severity or "Info",
        description=finding.description,
        status=finding.status or "Open",
        target_id=finding.target_id,
    )

    db.add(db_finding)
    db.commit()
    db.refresh(db_finding)

    return db_finding


def get_findings(db: Session) -> list[Finding]:
    return db.query(Finding).all()


def get_finding_by_id(
    db: Session,
    finding_id: int
) -> Finding | None:

    return _get_finding(db, finding_id)


def update_finding(
    db: Session,
    finding_id: int,
    finding_data: FindingUpdate
) -> Finding | None:

    finding = _get_finding(db, finding_id)

    if finding is None:
        return None

    update_data = finding_data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(finding, key, value)

    db.commit()
    db.refresh(finding)

    return finding


def delete_finding(
    db: Session,
    finding_id: int
) -> bool:

    finding = _get_finding(db, finding_id)

    if finding is None:
        return False

    db.delete(finding)
    db.commit()

    return True
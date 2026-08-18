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
        poc=finding.poc,
        poc_type=finding.poc_type,
        status=finding.status or "Open",
        target_id=finding.target_id,
    )

    db.add(db_finding)
    db.commit()
    db.refresh(db_finding)

    return db_finding


def get_findings(
    db: Session,
    severity: str | None = None,
    status: str | None = None,
    target_id: int | None = None,
    skip: int = 0,
    limit: int = 20,
    sort: str = "id",
    order: str = "asc",
) -> list[Finding]:

    query = db.query(Finding) 

    if severity is not None:
        query = query.filter(Finding.severity == severity)

    if status is not None:
        query = query.filter(Finding.status == status)

    if target_id is not None:
        query = query.filter(Finding.target_id == target_id)

    sort_fields = {
    "id": Finding.id,
    "severity": Finding.severity,
    "status": Finding.status,
    "target_id": Finding.target_id,
    }

    column = sort_fields[sort]

    if order == "desc":
       query = query.order_by(column.desc())
    else:
       query = query.order_by(column.asc())

    query = query.offset(skip).limit(limit)

    return query.all()


def get_findings_for_target(
    db: Session,
    target_id: int,
    skip: int = 0,
    limit: int = 20,
    sort: str = "id",
    order: str = "asc",
) -> list[Finding]:

    return get_findings(
        db=db,
        target_id=target_id,
        skip=skip,
        limit=limit,
        sort=sort,
        order=order,
    )


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
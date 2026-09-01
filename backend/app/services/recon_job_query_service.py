from sqlalchemy.orm import Session

from app.models.recon_job import ReconJob


def get_recon_job_by_id(
    db: Session,
    job_id: int,
) -> ReconJob | None:
    return (
        db.query(ReconJob)
        .filter(ReconJob.id == job_id)
        .first()
    )


def get_recon_jobs(
    db: Session,
    target_id: int | None = None,
    status: str | None = None,
    skip: int = 0,
    limit: int = 50,
) -> list[ReconJob]:
    query = db.query(ReconJob)

    if target_id is not None:
        query = query.filter(ReconJob.target_id == target_id)

    if status is not None:
        query = query.filter(ReconJob.status == status)

    return (
        query
        .order_by(ReconJob.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
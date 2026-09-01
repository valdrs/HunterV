from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.recon_job import ReconJob


def create_recon_job(
    db: Session,
    target_id: int,
    job_type: str,
    source: str,
) -> ReconJob:
    job = ReconJob(
        target_id=target_id,
        job_type=job_type,
        source=source,
        status="queued",
        created_at=datetime.now(timezone.utc),
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


def get_recon_job(
    db: Session,
    job_id: int,
) -> ReconJob | None:
    return (
        db.query(ReconJob)
        .filter(ReconJob.id == job_id)
        .first()
    )

def get_active_recon_job(
    db: Session,
    target_id: int,
    job_type: str,
    source: str,
) -> ReconJob | None:
    return (
        db.query(ReconJob)
        .filter(
            ReconJob.target_id == target_id,
            ReconJob.job_type == job_type,
            ReconJob.source == source,
            ReconJob.status.in_(["queued", "running"]),
        )
        .order_by(ReconJob.id.desc())
        .first()
    )

def mark_job_started(
    db: Session,
    job_id: int,
) -> ReconJob | None:
    job = get_recon_job(db, job_id)

    if job is None:
        return None

    job.status = "running"
    job.started_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(job)

    return job


def mark_job_completed(
    db: Session,
    job_id: int,
) -> ReconJob | None:
    job = get_recon_job(db, job_id)

    if job is None:
        return None

    job.status = "completed"
    job.completed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(job)

    return job


def mark_job_failed(
    db: Session,
    job_id: int,
    error: str,
) -> ReconJob | None:
    job = get_recon_job(db, job_id)

    if job is None:
        return None

    job.status = "failed"
    job.error = error
    job.completed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(job)

    return job
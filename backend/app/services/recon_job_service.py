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


def mark_job_started(
    db: Session,
    job: ReconJob,
) -> ReconJob:
    job.status = "running"
    job.started_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(job)

    return job


def mark_job_completed(
    db: Session,
    job: ReconJob,
) -> ReconJob:
    job.status = "completed"
    job.completed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(job)

    return job


def mark_job_failed(
    db: Session,
    job: ReconJob,
    error: str,
) -> ReconJob:
    job.status = "failed"
    job.error = error
    job.completed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(job)

    return job
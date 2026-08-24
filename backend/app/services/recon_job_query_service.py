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
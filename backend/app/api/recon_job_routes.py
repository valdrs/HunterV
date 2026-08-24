from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.recon_job import ReconJobResponse
from app.services.recon_job_query_service import get_recon_job_by_id


router = APIRouter(
    prefix="/recon/jobs",
    tags=["Recon Jobs"],
)


@router.get(
    "/{job_id}",
    response_model=ReconJobResponse,
)
def read_recon_job(
    job_id: int,
    db: Session = Depends(get_db),
):
    job = get_recon_job_by_id(
        db=db,
        job_id=job_id,
    )

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Recon job not found",
        )

    return job
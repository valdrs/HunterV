from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.recon_job import ReconJobResponse, ReconJobStatus
from app.services.recon_job_query_service import (
    get_recon_job_by_id,
    get_recon_jobs,
)


router = APIRouter(
    prefix="/recon/jobs",
    tags=["Recon Jobs"],
)


@router.get(
    "/",
    response_model=list[ReconJobResponse],
)
def read_recon_jobs(
    target_id: int | None = Query(default=None),
    status: ReconJobStatus | None = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db),
):
   return get_recon_jobs(
        db=db,
        target_id=target_id,
        status=status.value if status else None,
        skip=skip,
        limit=limit,
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
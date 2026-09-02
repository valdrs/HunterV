from fastapi import (
    APIRouter, 
    BackgroundTasks, 
    Depends, 
    HTTPException, 
    Response, 
    Query,
)
from sqlalchemy.orm import Session

from app.models.target import Target

from app.services.finding_service import get_findings_for_target
from app.db.dependencies import get_db
from app.schemas.finding import FindingResponse
from app.schemas.recon_job import ReconJobResponse
from app.schemas.asset import AssetResponse
from app.schemas.target import (
    TargetCreate,
    TargetResponse,
    TargetUpdate,
)
from app.schemas.finding_query import (
    FindingSort,
    SortOrder,
)
from app.services.finding_service import (
    get_findings_for_target,
)
from app.services.target_service import (
    create_target,
    get_targets,
    get_target_by_id,
    update_target,
    delete_target,
)
from app.services.asset_service import get_assets
from app.services.recon.recon_worker import (
    execute_subdomain_recon_job,
    execute_asset_recon_job,
    execute_full_recon_job,
)
from app.services.recon_job_service import (
    ActiveReconJobError,
    create_recon_job,
    get_active_recon_job,
)

router = APIRouter(
    prefix="/targets",
    tags=["Targets"]
)


@router.post(
    "/",
    response_model=TargetResponse
)
def create_new_target(
    target: TargetCreate,
    db: Session = Depends(get_db)
):
    return create_target(db, target)

@router.get(
    "/{target_id}/findings",
    response_model=list[FindingResponse]
)
def read_target_findings(
    target_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    sort: FindingSort = FindingSort.ID,
    order: SortOrder = SortOrder.ASC,
    db: Session = Depends(get_db)
):
    target = get_target_by_id(db, target_id)

    if target is None:
        raise HTTPException(
            status_code=404,
            detail="Target not found"
        )

    return get_findings_for_target(
        db=db,
        target_id=target_id,
        skip=skip,
        limit=limit,
        sort=sort.value,
        order=order.value,
    )

@router.get(
    "/{target_id}/assets",
    response_model=list[AssetResponse],
)
def read_target_assets(
    target_id: int,
    db: Session = Depends(get_db),
):
    target = get_target_by_id(db, target_id)

    if target is None:
        raise HTTPException(
            status_code=404,
            detail="Target not found",
        )

    return get_assets(
        db=db,
        target_id=target_id,
    )

@router.get(
    "/",
    response_model=list[TargetResponse]
)
def read_targets(
    db: Session = Depends(get_db)
):
    return get_targets(db)

@router.get(
    "/{target_id}",
    response_model=TargetResponse
)
def read_target(
    target_id: int,
    db: Session = Depends(get_db)
):
    target = get_target_by_id(db, target_id)

    if target is None:
        raise HTTPException(
            status_code=404,
            detail="Target not found"
        )

    return target

@router.put(
    "/{target_id}",
    response_model=TargetResponse
)
def update_existing_target(
    target_id: int,
    target_data: TargetUpdate,
    db: Session = Depends(get_db)
):
    target = update_target(
        db,
        target_id,
        target_data
    )

    if target is None:
        raise HTTPException(
            status_code=404,
            detail="Target not found"
        )

    return target

@router.delete(
    "/{target_id}",
    status_code=204
)
def delete_existing_target(
    target_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_target(db, target_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Target not found"
        )

    return Response(status_code=204)

@router.post(
    "/{target_id}/recon/subdomains",
    response_model=ReconJobResponse,
    status_code=202,
    responses={
        404: {"description": "Target not found"},
        409: {"description": "An active recon job already exists"},
    },
)
def recon_subdomains(
    target_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    target = (
        db.query(Target)
        .filter(Target.id == target_id)
        .first()
    )

    if target is None:
        raise HTTPException(
            status_code=404,
            detail="Target not found",
        )

    active_job = get_active_recon_job(
        db=db,
        target_id=target_id,
        job_type="subdomain_recon",
        source="subfinder",
    )

    if active_job is not None:
        raise HTTPException(
            status_code=409,
            detail="A subdomain reconnaissance job is already active for this target.",
        )

    try:
        job = create_recon_job(
            db=db,
            target_id=target_id,
            job_type="subdomain_recon",
            source="subfinder",
        )
    except ActiveReconJobError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        )

    background_tasks.add_task(
        execute_subdomain_recon_job,
        job.id,
        target_id,
    )

    return job

@router.post(
    "/{target_id}/recon",
    response_model=ReconJobResponse,
    status_code=202,
    responses={
        404: {"description": "Target not found"},
        409: {"description": "An active full recon job already exists"},
    },
)
def recon_target(
    target_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    target = (
        db.query(Target)
        .filter(Target.id == target_id)
        .first()
    )

    if target is None:
        raise HTTPException(
            status_code=404,
            detail="Target not found",
        )

    active_job = get_active_recon_job(
        db=db,
        target_id=target_id,
        job_type="full_recon",
        source="hunterv",
    )

    if active_job is not None:
        raise HTTPException(
            status_code=409,
            detail="A full reconnaissance job is already active for this target.",
        )

    try:
        job = create_recon_job(
            db=db,
            target_id=target_id,
            job_type="full_recon",
            source="hunterv",
        )
    except ActiveReconJobError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        )

    background_tasks.add_task(
        execute_full_recon_job,
        job.id,
        target_id,
    )

    return job

@router.post(
    "/{target_id}/recon/assets",
    response_model=ReconJobResponse,
    status_code=202,
    responses={
        404: {"description": "Target not found"},
        409: {"description": "An active asset recon job already exists"},
    },
)
def recon_assets(
    target_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    target = (
        db.query(Target)
        .filter(Target.id == target_id)
        .first()
    )

    if target is None:
        raise HTTPException(
            status_code=404,
            detail="Target not found",
        )

    active_job = get_active_recon_job(
        db=db,
        target_id=target_id,
        job_type="asset_recon",
        source="httpx",
    )

    if active_job is not None:
        raise HTTPException(
            status_code=409,
            detail="An asset reconnaissance job is already active for this target.",
        )

    try:
        job = create_recon_job(
            db=db,
            target_id=target_id,
            job_type="asset_recon",
            source="httpx",
        )
    except ActiveReconJobError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        )

    background_tasks.add_task(
        execute_asset_recon_job,
        job.id,
        target_id,
    )

    return job
from fastapi import APIRouter, Depends, HTTPException, Response, Query
from sqlalchemy.orm import Session
from app.services.finding_service import get_findings_for_target
from app.db.dependencies import get_db
from app.schemas.finding import FindingResponse
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
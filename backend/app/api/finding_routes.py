from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.target import Target
from app.schemas.finding import (
    FindingCreate,
    FindingUpdate,
    FindingResponse,
)
from app.services.finding_service import (
    create_finding,
    get_findings,
    get_finding_by_id,
    update_finding,
    delete_finding,
)
from app.services.finding_service import (
    create_finding,
    get_findings,
    get_findings_for_target,
    get_finding_by_id,
    update_finding,
    delete_finding,
)

from app.schemas.finding_query import (
    FindingSort,
    SortOrder,
)

router = APIRouter(
    prefix="/findings",
    tags=["Findings"]
)


@router.post(
    "/",
    response_model=FindingResponse
)
def create_new_finding(
    finding: FindingCreate,
    db: Session = Depends(get_db)
):
    result = create_finding(db, finding)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Target not found"
        )

    return result


@router.get(
    "/",
    response_model=list[FindingResponse]
)
def list_findings(
    severity: str | None = None,
    status: str | None = None,
    target_id: int | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    sort: FindingSort = FindingSort.ID,
    order: SortOrder = SortOrder.ASC,
    db: Session = Depends(get_db)
):
    return get_findings(
        db,
        severity,
        status,
        target_id,
        skip,
        limit,
        sort.value,
        order.value,
    )

@router.get(
    "/target/{target_id}",
    response_model=list[FindingResponse]
)
def list_findings_for_target(
    target_id: int,
    db: Session = Depends(get_db)
):
    target = (
        db.query(Target)
        .filter(Target.id == target_id)
        .first()
    )

    if target is None:
        raise HTTPException(
            status_code=404,
            detail="Target not found"
        )

    return get_findings_for_target(
        db,
        target_id
    )

@router.get(
    "/{finding_id}",
    response_model=FindingResponse
)
def read_finding(
    finding_id: int,
    db: Session = Depends(get_db)
):
    finding = get_finding_by_id(db, finding_id)

    if finding is None:
        raise HTTPException(
            status_code=404,
            detail="Finding not found"
        )

    return finding


@router.put(
    "/{finding_id}",
    response_model=FindingResponse
)
def update_existing_finding(
    finding_id: int,
    finding_data: FindingUpdate,
    db: Session = Depends(get_db)
):
    finding = update_finding(
        db,
        finding_id,
        finding_data
    )

    if finding is None:
        raise HTTPException(
            status_code=404,
            detail="Finding not found"
        )

    return finding


@router.delete(
    "/{finding_id}"
)
def delete_existing_finding(
    finding_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_finding(
        db,
        finding_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Finding not found"
        )

    return {
        "message": "Finding deleted successfully"
    }
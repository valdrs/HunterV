from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
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
    db: Session = Depends(get_db)
):
    return get_findings(db)


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
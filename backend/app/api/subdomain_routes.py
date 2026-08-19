from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.subdomain import (
    SubdomainCreate,
    SubdomainResponse,
)

from app.services.subdomain_service import (
    create_subdomain,
    get_subdomains,
)


router = APIRouter(
    prefix="/subdomains",
    tags=["Subdomains"]
)


@router.post(
    "/",
    response_model=SubdomainResponse
)
def create_new_subdomain(
    subdomain: SubdomainCreate,
    db: Session = Depends(get_db)
):
    result = create_subdomain(
        db,
        subdomain
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Target not found"
        )

    return result


@router.get(
    "/",
    response_model=list[SubdomainResponse]
)
def list_subdomains(
    target_id: int | None = None,
    db: Session = Depends(get_db)
):
    return get_subdomains(
        db,
        target_id
    )
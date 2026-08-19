from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.subdomain import Subdomain
from app.models.target import Target
from app.schemas.subdomain import SubdomainCreate

class DuplicateSubdomainError(Exception):
    pass

def create_subdomain(
    db: Session,
    subdomain: SubdomainCreate
) -> Subdomain | None:

    target = (
        db.query(Target)
        .filter(Target.id == subdomain.target_id)
        .first()
    )

    if target is None:
        return None

    db_subdomain = Subdomain(
        hostname=subdomain.hostname,
        status=subdomain.status or "discovered",
        source=subdomain.source,
        target_id=subdomain.target_id,
    )

    db.add(db_subdomain)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise DuplicateSubdomainError

    db.refresh(db_subdomain)

    return db_subdomain

def get_subdomains(
    db: Session,
    target_id: int | None = None
) -> list[Subdomain]:

    query = db.query(Subdomain)

    if target_id is not None:
        query = query.filter(
            Subdomain.target_id == target_id
        )

    return query.all()

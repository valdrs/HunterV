from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.subdomain import Subdomain
from app.models.target import Target
from app.schemas.subdomain import SubdomainCreate


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

    existing = (
        db.query(Subdomain)
        .filter(
            Subdomain.target_id == subdomain.target_id,
            Subdomain.hostname == subdomain.hostname,
        )
        .first()
    )

    if existing:
        existing.status = subdomain.status
        existing.source = subdomain.source
        existing.last_seen = datetime.now(timezone.utc)

        db.commit()
        db.refresh(existing)

        return existing

    db_subdomain = Subdomain(
        hostname=subdomain.hostname,
        status=subdomain.status or "discovered",
        source=subdomain.source,
        target_id=subdomain.target_id,
    )

    db.add(db_subdomain)
    db.commit()
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

def upsert_subdomains(
    db: Session,
    target_id: int,
    hostnames: list[str],
    source: str,
    status: str = "discovered",
) -> tuple[list[Subdomain], int, int]:

    if not hostnames:
        return [], 0, 0

    # Remove duplicates while preserving order.
    unique_hostnames = list(dict.fromkeys(hostnames))

    existing_subdomains = (
        db.query(Subdomain)
        .filter(
            Subdomain.target_id == target_id,
            Subdomain.hostname.in_(unique_hostnames),
        )
        .all()
    )

    existing_by_hostname = {
        subdomain.hostname: subdomain
        for subdomain in existing_subdomains
    }

    now = datetime.utcnow()

    created = 0
    updated = 0
    results = []

    for hostname in unique_hostnames:

        existing = existing_by_hostname.get(hostname)

        if existing:
            existing.status = status
            existing.source = source
            existing.last_seen = now

            updated += 1
            results.append(existing)

        else:
            db_subdomain = Subdomain(
                hostname=hostname,
                status=status,
                source=source,
                target_id=target_id,
                last_seen=now,
            )

            db.add(db_subdomain)

            created += 1
            results.append(db_subdomain)

    db.commit()

    return results, created, updated
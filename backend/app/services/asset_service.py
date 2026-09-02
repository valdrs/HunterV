from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.asset import Asset


def upsert_asset(
    db: Session,
    target_id: int,
    hostname: str,
    protocol: str,
    port: int,
    source: str,
    status: str = "discovered",
    subdomain_id: int | None = None,
) -> tuple[Asset, bool]:
    """
    Create an asset if it does not exist.

    Returns:
        (asset, created)
    """

    existing = (
        db.query(Asset)
        .filter(
            Asset.target_id == target_id,
            Asset.hostname == hostname,
            Asset.protocol == protocol,
            Asset.port == port,
        )
        .first()
    )

    now = datetime.now(timezone.utc)

    if existing:
        existing.status = status
        existing.source = source
        existing.last_seen = now

        if subdomain_id is not None:
            existing.subdomain_id = subdomain_id

        db.commit()
        db.refresh(existing)

        return existing, False

    asset = Asset(
        target_id=target_id,
        subdomain_id=subdomain_id,
        hostname=hostname,
        protocol=protocol,
        port=port,
        status=status,
        source=source,
        first_seen=now,
        last_seen=now,
    )

    db.add(asset)
    db.commit()
    db.refresh(asset)

    return asset, True


def get_assets(
    db: Session,
    target_id: int | None = None,
) -> list[Asset]:

    query = db.query(Asset)

    if target_id is not None:
        query = query.filter(
            Asset.target_id == target_id
        )

    return (
        query
        .order_by(Asset.id.desc())
        .all()
    )
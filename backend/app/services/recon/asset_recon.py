from sqlalchemy.orm import Session

from app.models.target import Target
from app.models.subdomain import Subdomain
from app.services.recon.http_probe import probe_host
from app.services.asset_service import upsert_asset


HTTP_PORTS = [
    ("http", 80),
    ("https", 443),
]


def run_asset_recon(
    db: Session,
    target: Target,
) -> dict:
    """
    Probe discovered subdomains for HTTP/HTTPS services
    and persist reachable services as Assets.
    """

    subdomains = (
        db.query(Subdomain)
        .filter(
            Subdomain.target_id == target.id
        )
        .all()
    )

    discovered = 0
    created = 0
    updated = 0
    assets = []

    for subdomain in subdomains:

        for protocol, port in HTTP_PORTS:

            result = probe_host(
                hostname=subdomain.hostname,
                protocol=protocol,
                port=port,
            )

            if result is None:
                continue

            discovered += 1

            asset, was_created = upsert_asset(
                db=db,
                target_id=target.id,
                hostname=subdomain.hostname,
                protocol=protocol,
                port=port,
                source="httpx",
                status=result["status"],
                subdomain_id=subdomain.id,
            )

            if was_created:
                created += 1
            else:
                updated += 1

            assets.append(
                {
                    "id": asset.id,
                    "hostname": asset.hostname,
                    "protocol": asset.protocol,
                    "port": asset.port,
                    "status": asset.status,
                }
            )

    return {
        "target_id": target.id,
        "source": "httpx",
        "subdomains_checked": len(subdomains),
        "discovered": discovered,
        "created": created,
        "updated": updated,
        "assets": assets,
    }
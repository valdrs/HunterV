from sqlalchemy.orm import Session

from app.models.target import Target
from app.models.subdomain import Subdomain
from app.schemas.subdomain import SubdomainCreate
from app.services.recon.subfinder import (
    run_subfinder,
    SubfinderError,
)
from app.services.subdomain_service import create_subdomain


def normalize_hostname(hostname: str) -> str | None:
    """
    Normalize a hostname returned by a reconnaissance tool.
    """

    hostname = hostname.strip().lower()

    if not hostname:
        return None

    hostname = hostname.rstrip(".")

    if "://" in hostname:
        hostname = hostname.split("://", 1)[1]

    hostname = hostname.split("/", 1)[0]

    return hostname


def run_subdomain_recon(
    db: Session,
    target: Target,
) -> dict:

    discovered_hosts = run_subfinder(
        target.base_url
    )

    normalized_hosts = set()

    for hostname in discovered_hosts:
        normalized = normalize_hostname(hostname)

        if normalized:
            normalized_hosts.add(normalized)

    created = 0
    updated = 0
    persisted_hosts = []

    for hostname in sorted(normalized_hosts):

        existing = (
            db.query(Subdomain)
            .filter(
                Subdomain.target_id == target.id,
                Subdomain.hostname == hostname,
            )
            .first()
        )

        subdomain = create_subdomain(
            db,
            SubdomainCreate(
                hostname=hostname,
                target_id=target.id,
                status="discovered",
                source="subfinder",
            ),
        )

        if subdomain is None:
            continue

        if existing:
            updated += 1
        else:
            created += 1

        persisted_hosts.append(
            subdomain.hostname
        )

    return {
        "target_id": target.id,
        "source": "subfinder",
        "discovered": len(normalized_hosts),
        "created": created,
        "updated": updated,
        "subdomains": persisted_hosts,
    }
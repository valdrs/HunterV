from sqlalchemy.orm import Session
from app.models.target import Target
from app.models.subdomain import Subdomain
from app.services.recon.subfinder import run_subfinder
from app.services.subdomain_service import upsert_subdomains


def normalize_hostname(hostname: str) -> str | None:

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

    normalized_hosts = sorted(normalized_hosts)

    subdomains, created, updated = upsert_subdomains(
        db=db,
        target_id=target.id,
        hostnames=normalized_hosts,
        source="subfinder",
        status="discovered",
    )

    persisted_hosts = [
        subdomain.hostname
        for subdomain in subdomains
    ]

    return {
        "target_id": target.id,
        "source": "subfinder",
        "discovered": len(normalized_hosts),
        "created": created,
        "updated": updated,
        "subdomains": persisted_hosts,
        }
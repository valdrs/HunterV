from app.db.session import SessionLocal
from app.models.target import Target

from app.services.recon.subdomain_recon import run_subdomain_recon
from app.services.recon.asset_recon import run_asset_recon
from app.services.recon.subfinder import SubfinderError
from app.services.recon_job_service import (
    mark_job_started,
    mark_job_completed,
    mark_job_failed,
)


def execute_subdomain_recon_job(
    job_id: int,
    target_id: int,
) -> None:

    db = SessionLocal()

    try:
        target = (
            db.query(Target)
            .filter(Target.id == target_id)
            .first()
        )

        if target is None:
            mark_job_failed(
                db,
                job_id,
                "Target not found",
            )
            return

        mark_job_started(
            db,
            job_id,
        )

        run_subdomain_recon(
            db=db,
            target=target,
        )

        mark_job_completed(
            db,
            job_id,
        )

    except SubfinderError as exc:
        db.rollback()

        mark_job_failed(
            db,
            job_id,
            str(exc),
        )

    except Exception as exc:
        db.rollback()

        mark_job_failed(
            db,
            job_id,
            str(exc),
        )

    finally:
        db.close()


def execute_full_recon_job(
    job_id: int,
    target_id: int,
) -> None:

    db = SessionLocal()

    try:
        target = (
            db.query(Target)
            .filter(Target.id == target_id)
            .first()
        )

        if target is None:
            mark_job_failed(
                db,
                job_id,
                "Target not found",
            )
            return

        mark_job_started(
            db,
            job_id,
        )

        # Phase 1: Subdomain discovery
        run_subdomain_recon(
            db=db,
            target=target,
        )

        # Phase 2: Asset discovery
        from app.services.recon.asset_recon import run_asset_recon

        run_asset_recon(
            db=db,
            target=target,
        )

        mark_job_completed(
            db,
            job_id,
        )

    except SubfinderError as exc:
        db.rollback()

        mark_job_failed(
            db,
            job_id,
            str(exc),
        )

    except Exception as exc:
        db.rollback()

        mark_job_failed(
            db,
            job_id,
            str(exc),
        )

    finally:
        db.close()


def execute_asset_recon_job(
    job_id: int,
    target_id: int,
) -> None:

    db = SessionLocal()

    try:
        target = (
            db.query(Target)
            .filter(Target.id == target_id)
            .first()
        )

        if target is None:
            mark_job_failed(
                db,
                job_id,
                "Target not found",
            )
            return

        mark_job_started(
            db,
            job_id,
        )

        run_asset_recon(
            db=db,
            target=target,
        )

        mark_job_completed(
            db,
            job_id,
        )

    except Exception as exc:
        db.rollback()

        mark_job_failed(
            db,
            job_id,
            str(exc),
        )

    finally:
        db.close()
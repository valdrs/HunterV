from sqlalchemy.orm import Session

from app.models.target import Target
from app.schemas.target import TargetCreate, TargetUpdate


def _get_target(
        db: Session, 
        target_id: int
)->Target | None:
    return (
        db.query(Target)
        .filter(Target.id == target_id)
        .first()
    )


def create_target(
        db: Session, 
        target: TargetCreate
) -> Target:
    
    db_target = Target(
        name=target.name,
        base_url=target.base_url,
        program=target.program,
        platform=target.platform,
        notes=target.notes,
    )

    db.add(db_target)
    db.commit()
    db.refresh(db_target)

    return db_target

def get_targets(db: Session) -> list[Target]:
    return db.query(Target).all()

def get_target_by_id(
        db: Session, 
        target_id: int
)-> Target | None:
    return _get_target(db, target_id)

def update_target(
    db: Session,
    target_id: int,
    target_data: TargetUpdate
)-> Target | None:
    
    target = _get_target(db, target_id)

    if target is None:
        return None

    update_data = target_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(target, key, value)

    db.commit()
    db.refresh(target)

    return target

def delete_target(
        db: Session, 
        target_id: int
)-> bool:
    
    target = _get_target(db, target_id)

    if target is None:
        return False

    db.delete(target)
    db.commit()

    return True
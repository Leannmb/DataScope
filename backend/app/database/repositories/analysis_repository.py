from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import Analysis


def save_analysis(
    db: Session,
    analysis: Analysis,
) -> Analysis:
    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return analysis


def get_user_analyses(
    db: Session,
    user_id: int,
) -> list[Analysis]:
    result = db.execute(
        select(Analysis)
        .where(Analysis.user_id == user_id)
        .order_by(Analysis.created_at.desc())
    )

    return list(result.scalars().all())
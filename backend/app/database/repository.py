from sqlalchemy.orm import Session

from app.database.models import Analysis

from sqlalchemy import select

from sqlalchemy import select

def save_analysis(db: Session, analysis: Analysis) -> None:
    db.add(analysis)
    db.commit()
    db.refresh(analysis)


def get_all_analyses(db: Session) -> list[Analysis]:
    result = db.execute(
        select(Analysis).order_by(Analysis.created_at.desc())
    )
    return result.scalars().all()
from sqlalchemy.orm import Session

from app.database.models import Analysis

def save_analysis(db: Session, analysis: Analysis) -> None:
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
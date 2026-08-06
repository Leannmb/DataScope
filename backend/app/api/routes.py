import traceback
from pathlib import Path
from shutil import copyfileobj
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.database.models import Analysis, User
from app.database.repositories.analysis_repository import (
    get_user_analyses,
    save_analysis,
)
from app.schemas.analysis import (
    AnalysisHistoryResponse,
    AnalysisResponse,
)
from app.services.analyzer import analyze_csv
from app.services.auth import get_current_user

from fastapi.responses import StreamingResponse
from app.services.pdf_report import build_pdf_report

router = APIRouter()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get("/")
def read_root() -> dict[str, str]:
    return {
        "name": "DataScope API",
        "version": "0.7.0",
        "status": "running",
    }


@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}


@router.get(
    "/analyses",
    response_model=list[AnalysisHistoryResponse],
)
def get_analyses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Analysis]:
    return get_user_analyses(
        db,
        current_user.id,
    )


@router.post(
    "/analyze",
    response_model=AnalysisResponse,
)
def analyze_uploaded_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="El archivo debe tener un nombre.",
        )

    if Path(file.filename).suffix.lower() != ".csv":
        raise HTTPException(
            status_code=400,
            detail="Solo se soportan archivos CSV.",
        )

    temporary_path: Path | None = None

    try:
        with NamedTemporaryFile(
            delete=False,
            suffix=".csv",
        ) as temporary_file:
            copyfileobj(
                file.file,
                temporary_file,
            )

            temporary_path = Path(
                temporary_file.name
            )

        analysis = analyze_csv(
            str(temporary_path)
        )

        analysis["filename"] = file.filename

        analysis_record = Analysis(
            filename=analysis["filename"],
            rows=analysis["rows"],
            columns=analysis["column_names"],
            user_id=current_user.id,
        )

        save_analysis(
            db,
            analysis_record,
        )

        return analysis

    except (
        ValueError,
        UnicodeDecodeError,
    ) as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except Exception as error:
        db.rollback()

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor.",
        ) from error

    finally:
        file.file.close()

        if (
            temporary_path is not None
            and temporary_path.exists()
        ):
            temporary_path.unlink()

@router.post("/export/pdf")
def export_analysis_pdf(
    analysis: AnalysisResponse,
    current_user: User = Depends(get_current_user),
) -> StreamingResponse:
    pdf_buffer = build_pdf_report(
        analysis.model_dump()
    )

    base_filename = Path(
        analysis.filename
    ).stem

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": (
                f'attachment; filename="{base_filename}_report.pdf"'
            )
        },
    )
from pathlib import Path
from shutil import copyfileobj
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.analyzer import analyze_csv


router = APIRouter()


@router.get("/")
def read_root() -> dict[str, str]:
    return {
        "name": "DataScope API",
        "version": "0.4.0",
        "status": "running",
    }


@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}


@router.post("/analyze")
def analyze_uploaded_csv(file: UploadFile = File(...)) -> dict:
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
            copyfileobj(file.file, temporary_file)
            temporary_path = Path(temporary_file.name)

        analysis = analyze_csv(str(temporary_path))
        analysis["filename"] = file.filename

        return analysis

    except (ValueError, UnicodeDecodeError) as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor.",
        ) from error

    finally:
        file.file.close()

        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()
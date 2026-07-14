from pathlib import Path
from shutil import copyfileobj
from tempfile import NamedTemporaryFile

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from analyzer import analyze_csv

app = FastAPI(
    title="DataScope API",
    description="API para analizar conjuntos de datos.",
    version="0.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root() -> dict[str, str]:
    return {
        "name" :"DataScope API",
        "version" :"0.2.0",
        "status" :"running",
    }

@app.get("/health")
def health_check() -> dict[str, str]:
    return { "status": "healthy" }

@app.post("/analyze")
def analyze_uploaded_csv(file: UploadFile = File(...)) -> dict:
    if not file.filename:
        raise HTTPException(
            status_code=400, 
            detail="El archivo debe tener un nombre.")
    
    if Path(file.filename).suffix.lower() != ".csv":
        raise HTTPException(
            status_code=400, 
            detail="Solo se soportan archivos CSV.")
    
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

    except (ValueError, UnicodeDecodeError) as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        ) from e
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor.",
        ) from e
    
    finally:
        file.file.close()

        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink() 
import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.database.models import User
from app.database.repositories.user_repository import get_user_by_id
from app.services.security import (
    JWT_ALGORITHM,
    JWT_SECRET_KEY,
)


bearer_scheme = HTTPBearer(
    auto_error=False,
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        bearer_scheme
    ),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None:
        raise credentials_exception

    try:
        payload = jwt.decode(
            credentials.credentials,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        user = get_user_by_id(
            db,
            int(user_id),
        )

    except (jwt.PyJWTError, ValueError, TypeError) as error:
        raise credentials_exception from error

    if user is None:
        raise credentials_exception

    return user
import os
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt

from fastapi import (
    Depends,
    HTTPException,
    Request,
    status,
)

from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from sqlalchemy.orm import Session

from config import (
    JWT_ALGORITHM,
    JWT_SECRET_KEY,
)

from database.models import User
from database.session import SessionLocal


security = HTTPBearer(auto_error=False)

AUTH_COOKIE_NAME = "access_token"


def create_token(
    subject: str,
    expires_minutes: int = 60,
) -> str:
    now = datetime.now(timezone.utc)

    payload = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int(
            (
                now
                + timedelta(
                    minutes=expires_minutes
                )
            ).timestamp()
        ),
    }

    return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )


def decode_token(token: str) -> dict:
    return jwt.decode(
        token,
        JWT_SECRET_KEY,
        algorithms=[JWT_ALGORITHM],
    )


def set_auth_cookie(
    response,
    token: str,
    expires_minutes: int = 60,
) -> None:
    response.set_cookie(
        key=AUTH_COOKIE_NAME,
        value=token,

        # Prevent JavaScript from reading the token.
        httponly=True,

        # Required for cross-origin frontend/backend
        # cookie authentication.
        samesite="none",

        # SameSite=None requires Secure.
        secure=True,

        max_age=expires_minutes * 60,

        path="/",
    )


def clear_auth_cookie(response) -> None:
    response.delete_cookie(
        key=AUTH_COOKIE_NAME,
        path="/",
    )


def _extract_token(
    request: Request,
    credentials: Optional[
        HTTPAuthorizationCredentials
    ],
) -> Optional[str]:

    # Preferred method:
    # Authorization: Bearer <JWT>
    if (
        credentials
        and credentials.scheme.lower()
        == "bearer"
    ):
        return credentials.credentials

    # Fallback:
    # access_token cookie
    return request.cookies.get(
        AUTH_COOKIE_NAME
    )


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_current_user(
    request: Request,

    credentials: Optional[
        HTTPAuthorizationCredentials
    ] = Depends(security),

    db: Session = Depends(get_db),
):
    token = _extract_token(
        request,
        credentials,
    )

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required.",
        )

    try:
        payload = decode_token(token)

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
        )

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload.",
        )

    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload.",
        )

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
        )

    return user
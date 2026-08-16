from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
import bcrypt
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from core.auth import clear_auth_cookie, create_token, get_db, set_auth_cookie
from core.rate_limit import api_limiter, get_client_key, login_limiter
from database.models import User

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)



class AuthRequest(BaseModel):
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    email: EmailStr
    message: str
    access_token: str | None = None


@router.post("/register", response_model=AuthResponse)
async def register(
    request: AuthRequest,
    response: Response,
    db: Session = Depends(get_db),
    http_request: Request = None,
):
    client_key = get_client_key(http_request)
    if not api_limiter.is_allowed(client_key):
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many requests.")

    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email is already registered.")

    user = User(
        email=request.email,
        password_hash=bcrypt.hashpw(request.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_token(subject=str(user.id))
    set_auth_cookie(response, token)
    return AuthResponse(email=user.email, message="Account created successfully.", access_token=token)


@router.post("/login", response_model=AuthResponse)
async def login(
    request: AuthRequest,
    response: Response,
    db: Session = Depends(get_db),
    http_request: Request = None,
):
    client_key = get_client_key(http_request)
    if not login_limiter.is_allowed(client_key):
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many login attempts.")

    user = db.query(User).filter(User.email == request.email).first()
    if not user or not bcrypt.checkpw(request.password.encode('utf-8'), user.password_hash.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    token = create_token(subject=str(user.id))
    set_auth_cookie(response, token)
    return AuthResponse(email=user.email, message="Login successful.", access_token=token)


@router.post("/logout")
async def logout(response: Response):
    clear_auth_cookie(response)
    return {"message": "Logged out successfully."}

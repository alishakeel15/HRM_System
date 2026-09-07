from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from dependencies.db import get_db
from models.users_model import User
from schemas.users_schema import UserCreate, UserResponse, ChangePassword, ForgotPassword, ResetPassword
from errors_handling.HTTP_Exceptions import already_exists, unauthorized
from schemas.auth_schema import TokenResponse
from utils.password import verify_password, hash_password
from utils.jwt import create_access_token, create_reset_token
from dependencies.auth import get_current_user
from models.password_reset_model import PasswordResetToken
from datetime import datetime, timezone
from utils.jwt import SECRET_KEY, ALGORITHM

import jwt
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/signup", response_model=UserResponse)
def signup(
    data: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        (User.username == data.username) |
        (User.email == data.email)
    ).first()
    if existing_user:
        raise already_exists(
            "Username or email already exists"
        )
    user = User(
        username=data.username,
        email=data.email,
        password_hash=hash_password(data.password),
        is_active=data.is_active
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.username == form_data.username
    ).first()
    if not user:
        raise unauthorized("Invalid username or password")
    if not user.is_active:
        raise unauthorized("User account is inactive")
    if not verify_password(
        form_data.password,
        user.password_hash
    ):
        raise unauthorized("Invalid username or password")
    access_token = create_access_token({
        "sub": str(user.id)
    })
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.patch("/change-password")
def change_password(
    data: ChangePassword,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not verify_password(
        data.old_password,
        current_user.password_hash
    ):
        raise unauthorized("Old password is incorrect")
    current_user.password_hash = hash_password(
        data.new_password
    )
    db.commit()
    return {
        "message": "Password changed successfully"
    }

@router.post("/forgot-password")
def forgot_password(
    data: ForgotPassword,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == data.email
    ).first()
    if user:
        token, expires_at = create_reset_token(user.id)
        reset_token = PasswordResetToken(
            user_id=user.id,
            token=token,
            expires_at=expires_at.replace(tzinfo=None)
        )
        db.add(reset_token)
        db.commit()
    return {
        "message": "If this email exists, a password reset link has been sent"
    }

@router.post("/reset-password")
def reset_password(
    data: ResetPassword,
    db: Session = Depends(get_db)
):
    reset_record = db.query(PasswordResetToken).filter(
        PasswordResetToken.token == data.token,
        PasswordResetToken.used == False
    ).first()
    if not reset_record:
        raise unauthorized("Invalid or already used reset token")
    if reset_record.expires_at < datetime.now(timezone.utc).replace(
        tzinfo=None
    ):
        raise unauthorized("Reset token has expired")
    try:
        payload = jwt.decode(
            data.token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        if payload.get("type") != "password_reset":
            raise unauthorized("Invalid reset token")
    except jwt.ExpiredSignatureError:
        raise unauthorized("Reset token has expired")
    except jwt.InvalidTokenError:
        raise unauthorized("Invalid reset token")
    user = db.query(User).filter(
        User.id == reset_record.user_id
    ).first()
    if not user:
        raise unauthorized("User not found")
    user.password_hash = hash_password(
        data.new_password
    )
    reset_record.used = True
    db.commit()
    return {
        "message": "Password reset successfully"
    }
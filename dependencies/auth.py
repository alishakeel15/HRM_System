from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from dependencies.db import get_db
from models.users_model import User
from utils.jwt import SECRET_KEY, ALGORITHM
from errors_handling.HTTP_Exceptions import unauthorized, forbidden
import jwt
from datetime import datetime, timedelta, timezone
from models.revoked_tokens_model import RevokedToken
from models.permissions_model import Permission
from models.role_permissions_model import RolePermission

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise unauthorized("Invalid token")
        revoked = db.query(RevokedToken).filter(
            RevokedToken.token == token
        ).first()

        if revoked:
            raise unauthorized("Token has been revoked")
    except jwt.ExpiredSignatureError:
        raise unauthorized("Token has expired")
    except jwt.InvalidTokenError:
        raise unauthorized("Invalid token")
    user = db.query(User).filter(
        User.id == int(user_id)
    ).first()
    if not user:
        raise unauthorized("User not found")
    if not user.is_active:
        raise unauthorized("User account is inactive")
    return user

def require_role(required_role: str):
    def role_checker(
        current_user: User = Depends(get_current_user)
    ):
        if not current_user.role_id:
            raise unauthorized("User has no role assigned")
        role = current_user.role
        if role.name != required_role:
            raise unauthorized("You do not have this role")
        return current_user
    return role_checker

def require_permission(required_permission: str):
    def permission_checker(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        permission = (
            db.query(Permission)
            .join(
                RolePermission,
                RolePermission.permission_id == Permission.id
            )
            .filter(
                RolePermission.role_id == current_user.role_id,
                Permission.name == required_permission
            )
            .first()
        )
        if not permission:
            raise forbidden(
                "You do not have this permission"
            )
        return current_user
    return permission_checker

def create_reset_token(user_id: int):
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    token = jwt.encode(
        {
            "sub": str(user_id),
            "type": "password_reset",
            "exp": expire
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return token, expire
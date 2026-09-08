from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies.db import get_db
from models.users_model import User
from schemas.users_schema import UserCreate, UserUpdate, UserResponse, UserRoleUpdate
from errors_handling.HTTP_Exceptions import not_found, already_exists
from utils.password import hash_password
from dependencies.auth import require_permission, require_role
from models.roles_model import Role

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", response_model=UserResponse)
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
        current_user = Depends(
        require_permission("users.create")
        )
):
    existing_user = db.query(User).filter(
        (User.username == data.username) |
        (User.email == data.email)
    ).first()
    if existing_user:
        raise already_exists("Username or email already exists")
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

@router.get("/", response_model=list[UserResponse])
def get_users(
    username: str | None = None,
    email: str | None = None,
    db: Session = Depends(get_db),
        current_user = Depends(
        require_permission("users.read")
        )
):
    query = db.query(User)
    if username:
        query = query.filter(
            User.username.ilike(f"%{username}%")
        )
    if email:
        query = query.filter(
            User.email.ilike(f"%{email}%")
        )
    return query.all()

@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
        current_user = Depends(
        require_permission("users.read")
        )
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()
    if not user:
        raise not_found("User not found")
    return user

@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
        current_user = Depends(
        require_permission("users.update")
        )
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()
    if not user:
        raise not_found("User not found")
    update_data = data.model_dump(exclude_unset=True)
    if "username" in update_data:
        existing_username = db.query(User).filter(
            User.username == update_data["username"],
            User.id != user_id
        ).first()
        if existing_username:
            raise already_exists("Username already exists")
    if "email" in update_data:
        existing_email = db.query(User).filter(
            User.email == update_data["email"],
            User.id != user_id
        ).first()
        if existing_email:
            raise already_exists("Email already exists")
    if "password" in update_data:
        update_data["password_hash"] = hash_password(
            update_data.pop("password")
        )
    for key, value in update_data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(
        require_permission("users.delete")
    )
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()
    if not user:
        raise not_found("User not found")
    db.delete(user)
    db.commit()
    return {
        "message": "User deleted successfully"
    }

@router.patch("/{user_id}/role")
def assign_role(
    user_id: int,
    data: UserRoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin"))
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()
    if not user:
        raise not_found("User not found")
    role = db.query(Role).filter(
        Role.id == data.role_id
    ).first()
    if not role:
        raise not_found("Role not found")
    user.role_id = role.id
    db.commit()
    db.refresh(user)
    return {
        "message": "Role assigned successfully",
        "user_id": user.id,
        "role_id": role.id,
        "role": role.name
    }
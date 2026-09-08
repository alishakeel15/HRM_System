from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies.db import get_db
from models.permissions_model import Permission
from schemas.permissions_schema import (
    PermissionCreate,
    PermissionUpdate,
    PermissionResponse
)
from errors_handling.HTTP_Exceptions import not_found, already_exists
from dependencies.auth import require_permission

router = APIRouter(
    prefix="/permissions",
    tags=["Permissions"]
)

@router.post("/", response_model=PermissionResponse)
def create_permission(
    data: PermissionCreate,
    db: Session = Depends(get_db),
    permission_check: None = Depends(require_permission("permissions.create"))
):
    existing_permission = db.query(Permission).filter(
        Permission.name == data.name
    ).first()
    if existing_permission:
        raise already_exists("Permission already exists")
    permission = Permission(
        name=data.name,
        description=data.description
    )
    db.add(permission)
    db.commit()
    db.refresh(permission)
    return permission

@router.get("/", response_model=list[PermissionResponse])
def get_permissions(
    name: str | None = None,
    db: Session = Depends(get_db),
    permission_check: None = Depends(require_permission("permissions.read"))
):
    query = db.query(Permission)
    if name:
        query = query.filter(
            Permission.name.ilike(f"%{name}%")
        )
    return query.all()

@router.get("/{permission_id}", response_model=PermissionResponse)
def get_permission(
    permission_id: int,
    db: Session = Depends(get_db),
    permission_check: None = Depends(require_permission("permissions.read"))
):
    permission = db.query(Permission).filter(
        Permission.id == permission_id
    ).first()
    if not permission:
        raise not_found("Permission not found")
    return permission

@router.patch("/{permission_id}", response_model=PermissionResponse)
def update_permission(
    permission_id: int,
    data: PermissionUpdate,
    db: Session = Depends(get_db),
    permission_check: None = Depends(require_permission("permissions.update"))
):
    permission = db.query(Permission).filter(
        Permission.id == permission_id
    ).first()
    if not permission:
        raise not_found("Permission not found")
    update_data = data.model_dump(exclude_unset=True)
    if "name" in update_data:
        existing_permission = db.query(Permission).filter(
            Permission.name == update_data["name"],
            Permission.id != permission_id
        ).first()
        if existing_permission:
            raise already_exists("Permission already exists")
    for key, value in update_data.items():
        setattr(permission, key, value)
    db.commit()
    db.refresh(permission)
    return permission

@router.delete("/{permission_id}")
def delete_permission(
    permission_id: int,
    db: Session = Depends(get_db),
    permission_check: None = Depends(require_permission("permissions.delete"))
):
    permission = db.query(Permission).filter(
        Permission.id == permission_id
    ).first()
    if not permission:
        raise not_found("Permission not found")
    db.delete(permission)
    db.commit()
    return {"message": "Permission deleted successfully"}
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies.db import get_db
from models.role_permissions_model import RolePermission
from schemas.role_permissions_schema import (
    RolePermissionCreate,
    RolePermissionUpdate,
    RolePermissionResponse
)
from errors_handling.HTTP_Exceptions import not_found, already_exists

router = APIRouter(
    prefix="/role-permissions",
    tags=["Role Permissions"]
)

@router.post("/", response_model=RolePermissionResponse)
def create_role_permission(
    data: RolePermissionCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(RolePermission).filter(
        RolePermission.role_id == data.role_id,
        RolePermission.permission_id == data.permission_id
    ).first()
    if existing:
        raise already_exists("Role permission already exists")
    role_permission = RolePermission(
        role_id=data.role_id,
        permission_id=data.permission_id
    )
    db.add(role_permission)
    db.commit()
    db.refresh(role_permission)
    return role_permission

@router.get("/", response_model=list[RolePermissionResponse])
def get_role_permissions(
    role_id: int | None = None,
    permission_id: int | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(RolePermission)
    if role_id:
        query = query.filter(
            RolePermission.role_id == role_id
        )
    if permission_id:
        query = query.filter(
            RolePermission.permission_id == permission_id
        )
    return query.all()

@router.get(
    "/{role_id}/{permission_id}",
    response_model=RolePermissionResponse
)
def get_role_permission(
    role_id: int,
    permission_id: int,
    db: Session = Depends(get_db)
):
    role_permission = db.query(RolePermission).filter(
        RolePermission.role_id == role_id,
        RolePermission.permission_id == permission_id
    ).first()
    if not role_permission:
        raise not_found("Role permission not found")
    return role_permission

@router.patch(
    "/{role_id}/{permission_id}",
    response_model=RolePermissionResponse
)
def update_role_permission(
    role_id: int,
    permission_id: int,
    data: RolePermissionUpdate,
    db: Session = Depends(get_db)
):
    role_permission = db.query(RolePermission).filter(
        RolePermission.role_id == role_id,
        RolePermission.permission_id == permission_id
    ).first()
    if not role_permission:
        raise not_found("Role permission not found")
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(role_permission, key, value)
    db.commit()
    db.refresh(role_permission)
    return role_permission

@router.delete("/{role_id}/{permission_id}")
def delete_role_permission(
    role_id: int,
    permission_id: int,
    db: Session = Depends(get_db)
):
    role_permission = db.query(RolePermission).filter(
        RolePermission.role_id == role_id,
        RolePermission.permission_id == permission_id
    ).first()
    if not role_permission:
        raise not_found("Role permission not found")
    db.delete(role_permission)
    db.commit()
    return {"message": "Role permission deleted successfully"}
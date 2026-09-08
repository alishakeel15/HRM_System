from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies.db import get_db
from models.roles_model import Role
from schemas.roles_schema import RoleCreate, RoleUpdate, RoleResponse
from errors_handling.HTTP_Exceptions import not_found, already_exists
from dependencies.auth import require_permission

router = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)

@router.post("/", response_model=RoleResponse)
def create_role(
    data: RoleCreate,
    db: Session = Depends(get_db),
    permission_check: None = Depends(require_permission("roles.create"))
):
    existing_role = db.query(Role).filter(
        Role.name == data.name
    ).first()
    if existing_role:
        raise already_exists("Role already exists")
    role = Role(
        name=data.name,
        description=data.description
    )
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

@router.get("/", response_model=list[RoleResponse])
def get_roles(
    name: str | None = None,
    db: Session = Depends(get_db),
    permission_check: None = Depends(require_permission("roles.read"))
):
    query = db.query(Role)
    if name:
        query = query.filter(
            Role.name.ilike(f"%{name}%")
        )
    return query.all()

@router.get("/{role_id}", response_model=RoleResponse)
def get_role(
    role_id: int,
    db: Session = Depends(get_db),
    permission_check: None = Depends(require_permission("roles.read"))
):
    role = db.query(Role).filter(
        Role.id == role_id
    ).first()
    if not role:
        raise not_found("Role not found")
    return role

@router.patch("/{role_id}", response_model=RoleResponse)
def update_role(
    role_id: int,
    data: RoleUpdate,
    db: Session = Depends(get_db),
    permission_check: None = Depends(require_permission("roles.update"))
):
    role = db.query(Role).filter(
        Role.id == role_id
    ).first()
    if not role:
        raise not_found("Role not found")
    update_data = data.model_dump(exclude_unset=True)
    if "name" in update_data:
        existing_role = db.query(Role).filter(
            Role.name == update_data["name"],
            Role.id != role_id
        ).first()
        if existing_role:
            raise already_exists("Role already exists")
    for key, value in update_data.items():
        setattr(role, key, value)
    db.commit()
    db.refresh(role)
    return role

@router.delete("/{role_id}")
def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    permission_check: None = Depends(require_permission("roles.delete"))
):
    role = db.query(Role).filter(
        Role.id == role_id
    ).first()
    if not role:
        raise not_found("Role not found")
    db.delete(role)
    db.commit()
    return {
        "message": "Role deleted successfully"
    }
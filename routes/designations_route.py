from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies.db import get_db
from models.designations_model import Designation
from schemas.designations_schema import (
    DesignationCreate,
    DesignationUpdate,
    DesignationResponse
)
from errors_handling.HTTP_Exceptions import not_found, already_exists
from dependencies.auth import require_permission
router = APIRouter(
    prefix="/designations",
    tags=["Designations"]
)

@router.post("/", response_model=DesignationResponse)
def create_designation(
    data: DesignationCreate,
    db: Session = Depends(get_db),
    permission: None = Depends(require_permission("designations.create"))
):
    existing_designation = db.query(Designation).filter(
        Designation.name == data.name
    ).first()
    if existing_designation:
        raise already_exists("Designation already exists")
    designation = Designation(
        name=data.name,
        department_id=data.department_id
    )
    db.add(designation)
    db.commit()
    db.refresh(designation)
    return designation

@router.get("/", response_model=list[DesignationResponse])
def get_designations(
    name: str | None = None,
    department_id: int | None = None,
    db: Session = Depends(get_db),
    permission: None = Depends(require_permission("designations.read"))
):
    query = db.query(Designation)
    if name:
        query = query.filter(
            Designation.name.ilike(f"%{name}%")
        )
    if department_id:
        query = query.filter(
            Designation.department_id == department_id
        )
    return query.all()

@router.get("/{designation_id}", response_model=DesignationResponse)
def get_designation(
    designation_id: int,
    db: Session = Depends(get_db),
    permission: None = Depends(require_permission("designations.read"))
):
    designation = db.query(Designation).filter(
        Designation.id == designation_id
    ).first()
    if not designation:
        raise not_found("Designation not found")
    return designation

@router.patch("/{designation_id}", response_model=DesignationResponse)
def update_designation(
    designation_id: int,
    data: DesignationUpdate,
    db: Session = Depends(get_db),
    permission: None = Depends(require_permission("designations.update"))
):
    designation = db.query(Designation).filter(
        Designation.id == designation_id
    ).first()
    if not designation:
        raise not_found("Designation not found")
    update_data = data.model_dump(exclude_unset=True)
    if "name" in update_data:
        existing_designation = db.query(Designation).filter(
            Designation.name == update_data["name"],
            Designation.id != designation_id
        ).first()
        if existing_designation:
            raise already_exists("Designation already exists")
    for key, value in update_data.items():
        setattr(designation, key, value)
    db.commit()
    db.refresh(designation)
    return designation

@router.delete("/{designation_id}")
def delete_designation(
    designation_id: int,
    db: Session = Depends(get_db),
    permission: None = Depends(require_permission("designations.delete"))
):
    designation = db.query(Designation).filter(
        Designation.id == designation_id
    ).first()
    if not designation:
        raise not_found("Designation not found")
    db.delete(designation)
    db.commit()
    return {"message": "Designation deleted successfully"}
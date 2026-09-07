from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies.db import get_db
from models.departments_model import Department
from schemas.departments_schema import (
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentResponse
)
from errors_handling.HTTP_Exceptions import not_found, already_exists

router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)

@router.post("/", response_model=DepartmentResponse)
def create_department(
    data: DepartmentCreate,
    db: Session = Depends(get_db)
):
    existing_department = db.query(Department).filter(
        Department.name == data.name
    ).first()
    if existing_department:
        raise already_exists("Department already exists")
    department = Department(
        name=data.name,
        description=data.description
    )
    db.add(department)
    db.commit()
    db.refresh(department)
    return department

@router.get("/", response_model=list[DepartmentResponse])
def get_departments(
    name: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Department)
    if name:
        query = query.filter(
            Department.name.ilike(f"%{name}%")
        )
    return query.all()

@router.get("/{department_id}", response_model=DepartmentResponse)
def get_department(
    department_id: int,
    db: Session = Depends(get_db)
):
    department = db.query(Department).filter(
        Department.id == department_id
    ).first()
    if not department:
        raise not_found("Department not found")
    return department

@router.patch("/{department_id}", response_model=DepartmentResponse)
def update_department(
    department_id: int,
    data: DepartmentUpdate,
    db: Session = Depends(get_db)
):
    department = db.query(Department).filter(
        Department.id == department_id
    ).first()
    if not department:
        raise not_found("Department not found")
    update_data = data.model_dump(exclude_unset=True)
    if "name" in update_data:
        existing_department = db.query(Department).filter(
            Department.name == update_data["name"],
            Department.id != department_id
        ).first()
        if existing_department:
            raise already_exists("Department already exists")
    for key, value in update_data.items():
        setattr(department, key, value)
    db.commit()
    db.refresh(department)
    return department

@router.delete("/{department_id}")
def delete_department(
    department_id: int,
    db: Session = Depends(get_db)
):
    department = db.query(Department).filter(
        Department.id == department_id
    ).first()
    if not department:
        raise not_found("Department not found")
    db.delete(department)
    db.commit()
    return {
        "message": "Department deleted successfully"
    }
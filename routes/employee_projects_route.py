from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies.db import get_db
from models.employee_projects_model import EmployeeProject
from schemas.employee_projects_schema import (
    EmployeeProjectCreate,
    EmployeeProjectUpdate,
    EmployeeProjectResponse
)
from errors_handling.HTTP_Exceptions import not_found, already_exists

router = APIRouter(
    prefix="/employee-projects",
    tags=["Employee Projects"]
)

@router.post("/", response_model=EmployeeProjectResponse)
def create_employee_project(
    data: EmployeeProjectCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(EmployeeProject).filter(
        EmployeeProject.employee_id == data.employee_id,
        EmployeeProject.project_id == data.project_id
    ).first()
    if existing:
        raise already_exists("Employee is already assigned to this project")
    employee_project = EmployeeProject(
        employee_id=data.employee_id,
        project_id=data.project_id
    )
    db.add(employee_project)
    db.commit()
    db.refresh(employee_project)
    return employee_project

@router.get("/", response_model=list[EmployeeProjectResponse])
def get_employee_projects(
    employee_id: int | None = None,
    project_id: int | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(EmployeeProject)
    if employee_id:
        query = query.filter(
            EmployeeProject.employee_id == employee_id
        )
    if project_id:
        query = query.filter(
            EmployeeProject.project_id == project_id
        )
    return query.all()

@router.get(
    "/{employee_id}/{project_id}",
    response_model=EmployeeProjectResponse
)
def get_employee_project(
    employee_id: int,
    project_id: int,
    db: Session = Depends(get_db)
):
    employee_project = db.query(EmployeeProject).filter(
        EmployeeProject.employee_id == employee_id,
        EmployeeProject.project_id == project_id
    ).first()
    if not employee_project:
        raise not_found("Employee project assignment not found")
    return employee_project

@router.patch(
    "/{employee_id}/{project_id}",
    response_model=EmployeeProjectResponse
)
def update_employee_project(
    employee_id: int,
    project_id: int,
    data: EmployeeProjectUpdate,
    db: Session = Depends(get_db)
):
    employee_project = db.query(EmployeeProject).filter(
        EmployeeProject.employee_id == employee_id,
        EmployeeProject.project_id == project_id
    ).first()
    if not employee_project:
        raise not_found("Employee project assignment not found")
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(employee_project, key, value)
    db.commit()
    db.refresh(employee_project)
    return employee_project

@router.delete("/{employee_id}/{project_id}")
def delete_employee_project(
    employee_id: int,
    project_id: int,
    db: Session = Depends(get_db)
):
    employee_project = db.query(EmployeeProject).filter(
        EmployeeProject.employee_id == employee_id,
        EmployeeProject.project_id == project_id
    ).first()
    if not employee_project:
        raise not_found("Employee project assignment not found")
    db.delete(employee_project)
    db.commit()
    return {"message": "Employee removed from project successfully"}
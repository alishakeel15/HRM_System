from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies.db import get_db
from models.projects_model import Project
from schemas.projects_schema import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse
)
from errors_handling.HTTP_Exceptions import not_found, already_exists
from dependencies.auth import require_permission

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)

@router.post("/", response_model=ProjectResponse)
def create_project(
    data: ProjectCreate,
    db: Session = Depends(get_db),
    permission_check: None = Depends(require_permission("projects.create"))
):
    existing_project = db.query(Project).filter(
        Project.name == data.name
    ).first()
    if existing_project:
        raise already_exists("Project already exists")
    project = Project(
        name=data.name,
        description=data.description,
        start_date=data.start_date,
        end_date=data.end_date,
        status=data.status
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@router.get("/", response_model=list[ProjectResponse])
def get_projects(
    name: str | None = None,
    status: str | None = None,
    db: Session = Depends(get_db),
    permission_check: None = Depends(require_permission("projects.read"))
):
    query = db.query(Project)
    if name:
        query = query.filter(
            Project.name.ilike(f"%{name}%")
        )
    if status:
        query = query.filter(
            Project.status == status
        )
    return query.all()

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    permission_check: None = Depends(require_permission("projects.read"))
):
    project = db.query(Project).filter(
        Project.id == project_id
    ).first()
    if not project:
        raise not_found("Project not found")
    return project

@router.patch("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    data: ProjectUpdate,
    db: Session = Depends(get_db),
    permission_check: None = Depends(require_permission("projects.update"))
):
    project = db.query(Project).filter(
        Project.id == project_id
    ).first()
    if not project:
        raise not_found("Project not found")
    update_data = data.model_dump(exclude_unset=True)
    if "name" in update_data:
        existing_project = db.query(Project).filter(
            Project.name == update_data["name"],
            Project.id != project_id
        ).first()
        if existing_project:
            raise already_exists("Project already exists")
    for key, value in update_data.items():
        setattr(project, key, value)
    db.commit()
    db.refresh(project)
    return project

@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    permission_check: None = Depends(require_permission("projects.delete"))
):
    project = db.query(Project).filter(
        Project.id == project_id
    ).first()
    if not project:
        raise not_found("Project not found")
    db.delete(project)
    db.commit()
    return {"message": "Project deleted successfully"}
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies.db import get_db
from models.employees_model import Employee
from schemas.employees_schema import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse
)
from errors_handling.HTTP_Exceptions import not_found, already_exists
from dependencies.auth import require_permission
router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)

@router.post("/", response_model=EmployeeResponse)
def create_employee(
    user_id: int,
    data: EmployeeCreate,
    db: Session = Depends(get_db),
        current_user = Depends(
        require_permission("employees.create")
        )
):
    existing_employee = db.query(Employee).filter(
        Employee.user_id == user_id
    ).first()
    if existing_employee:
        raise already_exists("Employee already exists")
    employee = Employee(
        user_id=user_id,
        department_id=data.department_id,
        designation_id=data.designation_id,
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        phone=data.phone,
        hire_date=data.hire_date
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee

@router.get("/", response_model=list[EmployeeResponse])
def get_employees(
    first_name: str | None = None,
    department_id: int | None = None,
    designation_id: int | None = None,
    db: Session = Depends(get_db),
        current_user = Depends(
        require_permission("employees.read")
        )
):
    query = db.query(Employee)
    if first_name:
        query = query.filter(
            Employee.first_name.ilike(f"%{first_name}%")
        )
    if department_id:
        query = query.filter(
            Employee.department_id == department_id
        )
    if designation_id:
        query = query.filter(
            Employee.designation_id == designation_id
        )
    return query.all()

@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(
        require_permission("employees.read")
    )
):
    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()
    if not employee:
        raise not_found("Employee not found")
    return employee

@router.patch("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    data: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(
        require_permission("employees.update")
    )
):
    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()
    if not employee:
        raise not_found("Employee not found")
    update_data = data.model_dump(exclude_unset=True)
    if "user_id" in update_data:
        existing_employee = db.query(Employee).filter(
            Employee.user_id == update_data["user_id"],
            Employee.id != employee_id
        ).first()
        if existing_employee:
            raise already_exists("User is already assigned to an employee")
    for key, value in update_data.items():
        setattr(employee, key, value)
    db.commit()
    db.refresh(employee)
    return employee

@router.delete("/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(
        require_permission("employees.delete")
    )
):
    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()
    if not employee:
        raise not_found("Employee not found")
    db.delete(employee)
    db.commit()
    return {"message": "Employee deleted successfully"}
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies.db import get_db
from models.salaries_model import Salary
from schemas.salaries_schema import (
    SalaryCreate,
    SalaryUpdate,
    SalaryResponse
)
from errors_handling.HTTP_Exceptions import not_found

router = APIRouter(
    prefix="/salaries",
    tags=["Salaries"]
)

@router.post("/", response_model=SalaryResponse)
def create_salary(
    data: SalaryCreate,
    db: Session = Depends(get_db)
):
    salary = Salary(
        employee_id=data.employee_id,
        basic_salary=data.basic_salary,
        allowance=data.allowance,
        deduction=data.deduction,
        salary_month=data.salary_month
    )
    db.add(salary)
    db.commit()
    db.refresh(salary)
    return salary

@router.get("/", response_model=list[SalaryResponse])
def get_salaries(
    employee_id: int | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Salary)
    if employee_id:
        query = query.filter(
            Salary.employee_id == employee_id
        )
    return query.all()

@router.get("/{salary_id}", response_model=SalaryResponse)
def get_salary(
    salary_id: int,
    db: Session = Depends(get_db)
):
    salary = db.query(Salary).filter(
        Salary.id == salary_id
    ).first()
    if not salary:
        raise not_found("Salary not found")
    return salary

@router.patch("/{salary_id}", response_model=SalaryResponse)
def update_salary(
    salary_id: int,
    data: SalaryUpdate,
    db: Session = Depends(get_db)
):
    salary = db.query(Salary).filter(
        Salary.id == salary_id
    ).first()
    if not salary:
        raise not_found("Salary not found")
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(salary, key, value)
    db.commit()
    db.refresh(salary)
    return salary

@router.delete("/{salary_id}")
def delete_salary(
    salary_id: int,
    db: Session = Depends(get_db)
):
    salary = db.query(Salary).filter(
        Salary.id == salary_id
    ).first()
    if not salary:
        raise not_found("Salary not found")
    db.delete(salary)
    db.commit()
    return {"message": "Salary deleted successfully"}
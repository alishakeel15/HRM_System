from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies.db import get_db
from models.attendance_model import Attendance
from schemas.attendance_schema import (
    AttendanceCreate,
    AttendanceUpdate,
    AttendanceResponse
)
from errors_handling.HTTP_Exceptions import not_found, already_exists

router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"]
)

@router.post("/", response_model=AttendanceResponse)
def create_attendance(
    data: AttendanceCreate,
    db: Session = Depends(get_db)
):
    existing_attendance = db.query(Attendance).filter(
        Attendance.employee_id == data.employee_id,
        Attendance.attendance_date == data.attendance_date
    ).first()
    if existing_attendance:
        raise already_exists(
            "Attendance already exists for this employee on this date"
        )
    attendance = Attendance(
        employee_id=data.employee_id,
        attendance_date=data.attendance_date,
        check_in=data.check_in,
        check_out=data.check_out,
        status=data.status
    )
    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    return attendance

@router.get("/", response_model=list[AttendanceResponse])
def get_attendance(
    employee_id: int | None = None,
    status: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Attendance)
    if employee_id:
        query = query.filter(
            Attendance.employee_id == employee_id
        )
    if status:
        query = query.filter(
            Attendance.status == status
        )
    return query.all()

@router.get("/{attendance_id}", response_model=AttendanceResponse)
def get_attendance_record(
    attendance_id: int,
    db: Session = Depends(get_db)
):
    attendance = db.query(Attendance).filter(
        Attendance.id == attendance_id
    ).first()
    if not attendance:
        raise not_found("Attendance record not found")
    return attendance

@router.patch(
    "/{attendance_id}",
    response_model=AttendanceResponse
)
def update_attendance(
    attendance_id: int,
    data: AttendanceUpdate,
    db: Session = Depends(get_db)
):
    attendance = db.query(Attendance).filter(
        Attendance.id == attendance_id
    ).first()
    if not attendance:
        raise not_found("Attendance record not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(attendance, key, value)
    db.commit()
    db.refresh(attendance)
    return attendance

@router.delete("/{attendance_id}")
def delete_attendance(
    attendance_id: int,
    db: Session = Depends(get_db)
):
    attendance = db.query(Attendance).filter(
        Attendance.id == attendance_id
    ).first()
    if not attendance:
        raise not_found("Attendance record not found")
    db.delete(attendance)
    db.commit()
    return {"message": "Attendance deleted successfully"}
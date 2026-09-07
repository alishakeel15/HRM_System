from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies.db import get_db
from models.leaves_model import Leave
from schemas.leaves_schema import (
    LeaveCreate,
    LeaveUpdate,
    LeaveResponse
)
from errors_handling.HTTP_Exceptions import not_found

router = APIRouter(
    prefix="/leaves",
    tags=["Leaves"]
)

@router.post("/", response_model=LeaveResponse)
def create_leave(
    data: LeaveCreate,
    db: Session = Depends(get_db)
):
    leave = Leave(
        employee_id=data.employee_id,
        leave_type=data.leave_type,
        start_date=data.start_date,
        end_date=data.end_date,
        reason=data.reason,
        status=data.status
    )
    db.add(leave)
    db.commit()
    db.refresh(leave)
    return leave

@router.get("/", response_model=list[LeaveResponse])
def get_leaves(
    employee_id: int | None = None,
    status: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Leave)
    if employee_id:
        query = query.filter(
            Leave.employee_id == employee_id
        )
    if status:
        query = query.filter(
            Leave.status == status
        )
    return query.all()

@router.get("/{leave_id}", response_model=LeaveResponse)
def get_leave(
    leave_id: int,
    db: Session = Depends(get_db)
):
    leave = db.query(Leave).filter(
        Leave.id == leave_id
    ).first()
    if not leave:
        raise not_found("Leave not found")
    return leave

@router.patch("/{leave_id}", response_model=LeaveResponse)
def update_leave(
    leave_id: int,
    data: LeaveUpdate,
    db: Session = Depends(get_db)
):
    leave = db.query(Leave).filter(
        Leave.id == leave_id
    ).first()
    if not leave:
        raise not_found("Leave not found")
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(leave, key, value)
    db.commit()
    db.refresh(leave)
    return leave

@router.delete("/{leave_id}")
def delete_leave(
    leave_id: int,
    db: Session = Depends(get_db)
):
    leave = db.query(Leave).filter(
        Leave.id == leave_id
    ).first()
    if not leave:
        raise not_found("Leave not found")
    db.delete(leave)
    db.commit()
    return {"message": "Leave deleted successfully"}
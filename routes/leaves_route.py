from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies.auth import require_permission
from dependencies.db import get_db
from models.leaves_model import Leave
from schemas.leaves_schema import (
    LeaveCreate,
    LeaveUpdate,
    LeaveResponse
)
from errors_handling.HTTP_Exceptions import already_exists, not_found

router = APIRouter(
    prefix="/leaves",
    tags=["Leaves"]
)

@router.post("/", response_model=LeaveResponse)
def create_leave(
    data: LeaveCreate,
    db: Session = Depends(get_db),
    permission: None = Depends(require_permission("leaves.create"))
):
    leave = Leave(
        employee_id=data.employee_id,
        leave_type=data.leave_type,
        start_date=data.start_date,
        end_date=data.end_date,
        reason=data.reason,
    )
    db.add(leave)
    db.commit()
    db.refresh(leave)
    return leave

@router.get("/", response_model=list[LeaveResponse])
def get_leaves(
    employee_id: int | None = None,
    status: str | None = None,
    db: Session = Depends(get_db),
    permission: None = Depends(require_permission("leaves.read"))
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
    db: Session = Depends(get_db),
    permission: None = Depends(require_permission("leaves.read"))
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
    db: Session = Depends(get_db),
    permission: None = Depends(require_permission("leaves.update"))
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
    db: Session = Depends(get_db),
    permission: None = Depends(require_permission("leaves.delete"))
):
    leave = db.query(Leave).filter(
        Leave.id == leave_id
    ).first()
    if not leave:
        raise not_found("Leave not found")
    db.delete(leave)
    db.commit()
    return {"message": "Leave deleted successfully"}

@router.patch("/{leave_id}/approve", response_model=LeaveResponse)
def approve_leave(
    leave_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(
        require_permission("leaves.approve")
    )
):
    leave = db.query(Leave).filter(
        Leave.id == leave_id
    ).first()
    if not leave:
        raise not_found("Leave not found")
    if leave.status != "pending":
        raise already_exists("Leave has already been processed")
    leave.status = "approved"
    leave.approved_by = current_user.id
    leave.approved_at = datetime.now()
    db.commit()
    db.refresh(leave)
    return leave
@router.patch("/{leave_id}/reject", response_model=LeaveResponse)
def reject_leave(
    leave_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(
        require_permission("leaves.approve")
    )
):
    leave = db.query(Leave).filter(
        Leave.id == leave_id
    ).first()
    if not leave:
        raise not_found("Leave not found")
    if leave.status != "pending":
        raise already_exists("Leave has already been processed")
    leave.status = "rejected"
    leave.approved_by = current_user.id
    leave.approved_at = datetime.now()
    db.commit()
    db.refresh(leave)
    return leave
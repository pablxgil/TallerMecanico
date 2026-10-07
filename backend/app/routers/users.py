from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_admin
from app.models import Role, User
from app.schemas import UserResponse, UserRoleUpdateRequest

router = APIRouter(prefix="/users", tags=["Usuarios"])


@router.get("", response_model=list[UserResponse])
def list_users(_: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    return db.scalars(select(User).order_by(User.full_name)).all()


@router.patch("/{user_id}/role", response_model=UserResponse)
def update_user_role(user_id: int, payload: UserRoleUpdateRequest, current_admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="El usuario indicado no existe.")
    if user.role == Role.SISTEMA or payload.role == Role.SISTEMA:
        raise HTTPException(status_code=400, detail="El rol de sistema no puede asignarse ni modificarse manualmente.")
    if user.id == current_admin.id and payload.role != Role.ADMINISTRADOR:
        raise HTTPException(status_code=400, detail="No puedes retirar tu propio permiso de administrador.")
    user.role = payload.role
    db.commit()
    db.refresh(user)
    return user

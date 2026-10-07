from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.models import Customer, User
from app.schemas import CustomerCreate, EntityResponse
router = APIRouter(prefix="/customers", tags=["Clientes"])
def require_staff(user: User):
    if user.role.value not in {"administrador", "recepcionista", "asesor_servicio"}: raise HTTPException(status_code=403, detail="No tienes permisos para administrar clientes.")
@router.get("")
def list_customers(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    require_staff(user); return db.scalars(select(Customer).order_by(Customer.full_name)).all()
@router.post("", response_model=EntityResponse, status_code=status.HTTP_201_CREATED)
def create_customer(payload: CustomerCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    require_staff(user); customer = Customer(full_name=payload.full_name.strip(), email=str(payload.email).lower(), phone=payload.phone.strip()); db.add(customer)
    try: db.commit()
    except IntegrityError: db.rollback(); raise HTTPException(status_code=409, detail="Ya existe un cliente con ese correo.")
    db.refresh(customer); return customer

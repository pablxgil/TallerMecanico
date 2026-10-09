import hashlib, secrets
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_admin, get_current_user
from app.models import PasswordResetToken, RoleDefinition, Role, User, Workshop
from app.schemas import EntityResponse, PasswordResetConfirm, PasswordResetRequest, RoleDefinitionRequest, RoleStatusRequest, WorkshopRequest
from app.security import hash_password
from app.postal_catalog import by_address, by_postal_code
router=APIRouter(tags=["Administración"])
@router.get("/address-lookup/by-address")
def address_lookup(state: str = Query(min_length=2), municipality: str = Query(min_length=2), neighborhood: str = Query(min_length=2)):
    item=by_address(state,municipality,neighborhood)
    if not item: raise HTTPException(404,"No se encontró esa dirección en el catálogo de Tula de Allende.")
    return {**item,"neighborhood":neighborhood}
@router.get("/address-lookup/{postal_code}")
def postal_lookup(postal_code: str):
    item=by_postal_code(postal_code)
    if not item: raise HTTPException(404,"El código postal no pertenece al catálogo de Tula de Allende.")
    return item
@router.get("/roles")
def roles(_:User=Depends(get_current_admin),db:Session=Depends(get_db)): return db.scalars(select(RoleDefinition).order_by(RoleDefinition.name)).all()
@router.post("/roles",response_model=EntityResponse,status_code=201)
def create_role(p:RoleDefinitionRequest,_:User=Depends(get_current_admin),db:Session=Depends(get_db)):
    item=RoleDefinition(name=p.name.strip().lower(),description=p.description);db.add(item)
    try: db.commit()
    except IntegrityError: db.rollback();raise HTTPException(409,"El rol ya existe.")
    db.refresh(item);return item
@router.patch("/roles/{role_id}/status",response_model=EntityResponse)
def role_status(role_id:int,p:RoleStatusRequest,_:User=Depends(get_current_admin),db:Session=Depends(get_db)):
    item=db.get(RoleDefinition,role_id)
    if not item:raise HTTPException(404,"El rol no existe.")
    item.status=p.status;db.commit();return item
@router.post("/workshops",response_model=EntityResponse,status_code=201)
def workshop(p:WorkshopRequest,user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    if user.role not in {Role.ADMINISTRADOR,Role.RECEPCIONISTA,Role.ASESOR}:raise HTTPException(403,"No tienes permisos para registrar talleres.")
    item=Workshop(**p.model_dump(),rfc=p.rfc.upper()) ;db.add(item)
    try:db.commit()
    except IntegrityError:db.rollback();raise HTTPException(409,"El nombre o RFC del taller ya está registrado.")
    db.refresh(item);return item
@router.post("/auth/password-reset/request")
def reset_request(p:PasswordResetRequest,db:Session=Depends(get_db)):
    user=db.scalar(select(User).where(User.email==str(p.email).lower()))
    if not user:return {"message":"Si la cuenta existe, se enviaron instrucciones."}
    raw=secrets.token_urlsafe(32);db.add(PasswordResetToken(user_id=user.id,token_hash=hashlib.sha256(raw.encode()).hexdigest(),expires_at=datetime.now(timezone.utc)+timedelta(minutes=20)));db.commit()
    return {"message":"Código generado para desarrollo.","development_token":raw}
@router.post("/auth/password-reset/confirm")
def reset_confirm(p:PasswordResetConfirm,db:Session=Depends(get_db)):
    item=db.scalar(select(PasswordResetToken).where(PasswordResetToken.token_hash==hashlib.sha256(p.token.encode()).hexdigest(),PasswordResetToken.used_at==None))
    if not item or item.expires_at.replace(tzinfo=timezone.utc)<datetime.now(timezone.utc):raise HTTPException(400,"El código no es válido o expiró.")
    user=db.get(User,item.user_id);user.password_hash=hash_password(p.new_password);item.used_at=datetime.now(timezone.utc);db.commit();return {"message":"Contraseña actualizada."}

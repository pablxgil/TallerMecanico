from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Role, User
from app.security import decode_token

bearer = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)) -> User:
    payload = decode_token(credentials.credentials)
    user = db.get(User, int(payload["sub"])) if payload.get("sub", "").isdigit() else None
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="La sesión no corresponde a una cuenta activa.")
    return user


def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != Role.ADMINISTRADOR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permisos de administrador para esta operación.")
    return current_user


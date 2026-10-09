from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from app.core.config import get_settings
from app.database import Base, SessionLocal, engine
from app.models import Role, User
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.customers import router as customers_router
from app.routers.administration import router as administration_router
from app.security import hash_password

settings = get_settings()


def seed_admin() -> None:
    with SessionLocal() as db:
        if not db.scalar(select(User).where(User.email == settings.admin_email.lower())):
            db.add(User(full_name="Administrador del taller", email=settings.admin_email.lower(), password_hash=hash_password(settings.admin_password), role=Role.ADMINISTRADOR))
            db.commit()


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed_admin()
    yield


app = FastAPI(title="API Taller Mecánico", version="0.1.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_credentials=False, allow_methods=["*"], allow_headers=["*"])
app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(customers_router, prefix="/api/v1")
app.include_router(administration_router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "ok"}


import os
os.environ["DATABASE_URL"] = "sqlite://"
os.environ["JWT_SECRET_KEY"] = "test-secret-key"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from app.database import Base, get_db
from app.main import app

engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)


@pytest.fixture()
def client():
    if not str(engine.url).startswith("sqlite"):
        raise RuntimeError("Las pruebas solo pueden ejecutarse con una base de datos SQLite aislada.")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    from sqlalchemy.orm import sessionmaker
    TestSession = sessionmaker(bind=engine)
    def override_db():
        db = TestSession()
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


# Taller Mecánico

Sistema SPA para autenticación y gestión futura del ciclo de vida de órdenes de reparación.

## Ejecutar con Docker (recomendado)

1. Copie `.env.example` como `.env` y cambie los secretos.
2. Ejecute `docker compose up --build`.
3. Abra `http://localhost:5173`.

El primer administrador se crea con `ADMIN_EMAIL` y `ADMIN_PASSWORD` configurados en `.env` (por defecto, `admin@tallermecanico.mx`).

## Desarrollo local

Backend:

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Frontend:

```powershell
cd frontend
npm install
npm run dev
```

Configure `VITE_API_URL=http://localhost:8000/api/v1` si el backend no usa esa dirección.

## Pruebas

```powershell
cd backend
pytest
```

Las pruebas usan SQLite en memoria y cubren registro, duplicados, inicio de sesión, protección de rutas y cambio de contraseña.


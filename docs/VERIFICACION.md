# Verificación de la entrega

Fecha de verificación: 2026-10-09.

| Comprobación | Resultado | Evidencia / notas |
|---|---|---|
| Estado inicial de Git | Verificado | Había cambios locales; se inspeccionaron y conservaron. |
| `uv` | Instalado | `uv 0.13.0` en el perfil de desarrollo. |
| Lock de dependencias | Generado | `backend/uv.lock`. |
| Entorno local con uv | Bloqueado | Python de Microsoft Store 3.14.7 no permite a uv resolver su ubicación real; `.venv` quedó creado pero sin paquetes. Docker conserva Python 3.13.16. |
| Backend con uv en Docker | Pendiente de construcción completa | Se añadió configuración, pero la construcción no terminó dentro de la ventana disponible; debe repetirse con `docker compose build backend`. |
| Pruebas M01 | 5 PASSED | Ejecutadas en contenedor aislado, sin MySQL, con `DATABASE_URL=sqlite://`; 4 warnings no funcionales. |
| Build frontend | Verificado previamente | `npm run build` terminó sin errores antes de esta entrega documental; no hubo cambio posterior de frontend. |
| Rutas API de consulta postal | Verificadas previamente | Consulta directa e inversa respondieron para `42800`/`Centro`. |
| Secretos preparados para Git | Verificado | `.env`, `.venv`, `node_modules` y `dist` están ignorados por `.gitignore`. |

## Comando de prueba seguro utilizado

```powershell
docker compose run --rm --no-deps -e DATABASE_URL=sqlite:// -e JWT_SECRET_KEY=test-secret-key -v "C:\TallerMecanico\backend:/app:ro" backend pytest -q
```

El montaje fue de solo lectura y `tests/conftest.py` ahora rechaza explícitamente cualquier base que no sea SQLite antes de ejecutar `drop_all()`.

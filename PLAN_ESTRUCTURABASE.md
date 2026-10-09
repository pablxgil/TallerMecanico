# Plan y estado real — TallerMecanico

## Objetivo y alcance

La solución es una SPA para el taller mecánico. En esta entrega se conserva y verifica el núcleo M01: identidad, autenticación, roles, recuperación de contraseña, administración de roles y alta de taller. No se implementan ni amplían vehículos, órdenes, diagnósticos, inventario ni auditoría operativa.

| Fase | Módulo | Funcionalidades | Estado | Evidencia | Pendientes |
|---|---|---|---|---|---|
| Fase 1 | M01 — Identidad, usuarios y sesiones | Registro, login JWT, consulta de sesión, cambio y recuperación de contraseña | EN DESARROLLO | `backend/app/routers/auth.py`, `frontend/src/views/AuthView.vue`, `backend/tests/test_auth.py` | Pruebas actualizadas para el rol `usuario`, entrega de recuperación por correo y auditoría persistente |
| Fase 1 | M01 — Administración de usuarios y roles | Consulta de usuarios, asignación de roles, catálogo de roles con baja lógica | EN DESARROLLO | `routers/users.py`, `routers/administration.py`, `RolesView.vue` | Migración formal y pruebas de roles; reparar datos heredados con rol `CLIENTE` |
| Fase 1 | M01 — Taller | Alta, RFC, unicidad, consulta postal local Tula de Allende | EN DESARROLLO | `WorkshopView.vue`, `postal_catalog.py`, `Workshop` | Pruebas de API, almacenamiento real de fotografía y modelo de pertenencia usuario–taller |
| Fase 2 | Clientes | Alta y listado básicos existentes | EN DESARROLLO | `customers.py`, `CustomersView.vue` | Contexto obligatorio de taller, paginación, actualización, desactivación, auditoría y pruebas; no ampliar en esta entrega |
| Fase 3 | Vehículos | Registro, consulta y relación cliente–vehículo | PENDIENTE | Diseño en `docs/` | Modelo, APIs, UI, pruebas y aislamiento por taller |
| Fases posteriores | Órdenes, diagnóstico, autorización, refacciones, inventario, notificaciones, historial y auditoría | Ciclo de reparación completo | PENDIENTE | Diseño de dependencias en `docs/` | Autorización funcional, modelo y entregas por fases |

## Tecnologías y dependencias

- Vue 3, TypeScript, Vite, Vuetify 3, Vue Router y API HTTP basada actualmente en `fetch`.
- FastAPI, SQLAlchemy, Pydantic, PyMySQL, Argon2 mediante Passlib y JWT.
- MySQL 8.4 en Docker; pruebas actuales con SQLite en memoria.
- `uv` administra dependencias del backend mediante `backend/pyproject.toml` y `backend/uv.lock`.

## Dependencias entre módulos

M01 entrega identidad, roles y el futuro contexto de taller. Clientes requiere M01 y un taller activo; Vehículos requiere Clientes; Órdenes requiere Clientes y Vehículos; los módulos operativos posteriores dependen de Órdenes.

## Entregables y criterios de aceptación de esta entrega

- Documentación de arquitectura, casos de uso, modelo de datos y APIs preliminares en `docs/`.
- Dependencias del backend reproducibles con `uv`; Docker conserva Python 3.13.
- Diagramas Mermaid versionados junto a la documentación.
- Pruebas ejecutadas y resultados registrados sin declarar éxito no verificado.

## Riesgos y próximos pasos

1. Existe una discrepancia en datos heredados: MySQL contiene al menos un rol `CLIENTE` que ya no existe en el `Enum` Python; esto afecta el listado de usuarios.
2. `Base.metadata.create_all()` no sustituye migraciones versionadas. Antes de evolucionar el esquema debe incorporarse una herramienta de migraciones y una migración nueva, sin reescribir tablas aplicadas.
3. La recuperación de contraseña devuelve un token de desarrollo; se requiere un proveedor de correo y almacenamiento seguro antes de producción.
4. Definir y persistir la relación usuario–taller antes de ampliar Clientes o Vehículos.

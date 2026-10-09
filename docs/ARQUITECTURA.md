# Arquitectura y diagramas

## Decisión sobre Archify

Se investigó Archify. La herramienta identificada es un skill/renderizador de diagramas para agentes que genera artefactos HTML, no una dependencia necesaria de Vue/FastAPI ni una integración de producción del proyecto. Para no añadir una dependencia no esencial, los diagramas se mantienen como Mermaid en Markdown, revisables en Git y compatibles con GitHub. La evaluación está en [ARCHIFY_EVALUACION.md](ARCHIFY_EVALUACION.md).

## Arquitectura actual

```mermaid
flowchart LR
  U[Usuario] --> V[Vue 3 SPA\nVuetify + Vue Router]
  V -->|HTTPS/JSON\n/api/v1| F[FastAPI]
  F --> A[Autenticación JWT\nArgon2 + dependencias]
  F --> S[SQLAlchemy]
  S --> M[(MySQL 8.4)]
  T[pytest + SQLite en memoria] -.verifica.-> F
```

## Comunicación de ejecución

```mermaid
sequenceDiagram
  participant UI as Vue SPA
  participant API as FastAPI /api/v1
  participant DB as MySQL
  UI->>API: JSON + Bearer JWT
  API->>API: Pydantic y autorización
  API->>DB: SQLAlchemy / transacción
  DB-->>API: entidad o error
  API-->>UI: respuesta HTTP tipada
```

## M01 — autenticación y autorización

```mermaid
flowchart TD
  L[Login] --> V{Correo y contraseña válidos}
  V -- No --> E[401 y mensaje claro]
  V -- Sí --> H[Verificar hash Argon2]
  H --> AC{Cuenta activa}
  AC -- No --> D[403]
  AC -- Sí --> J[Emitir JWT]
  J --> R[Vue guarda sesión]
  R --> P[Ruta protegida]
  P --> G[Dependencia get_current_user]
  G --> Q{Rol autorizado}
  Q -- No --> X[403]
  Q -- Sí --> O[Operación]
```

## Diseño futuro — clientes y vehículos

```mermaid
flowchart LR
  A[Personal autenticado] --> C[Cliente dentro del taller]
  C --> V[Vehículo]
  V --> OR[Orden de reparación]
  OR --> D[Diagnóstico / autorización]
  note[Diseño propuesto: no implementado en esta entrega]
```

## Dependencias entre módulos

```mermaid
flowchart TD
  M01[M01 Identidad y contexto de taller] --> CL[Clientes]
  M01 --> TM[Administración de taller]
  CL --> VH[Vehículos]
  CL --> OR[Órdenes]
  VH --> OR
  OR --> DG[Diagnóstico y autorización]
  OR --> RF[Refacciones e inventario]
  OR --> NT[Notificaciones, historial y auditoría]
```

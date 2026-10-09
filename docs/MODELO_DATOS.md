# Modelo de datos

## Entidades existentes

| Entidad | Clave y restricciones | Uso actual |
|---|---|---|
| `users` | PK `id`, `email` único, `role` enum, `is_active` | Identidad y autorización de M01 |
| `customers` | PK `id`, `email` único | Alta/listado básico heredado; aún sin taller, baja lógica ni auditoría |
| `role_definitions` | PK `id`, `name` único, `status` booleano | Catálogo administrable de roles |
| `workshops` | PK `id`, `name` y `rfc` únicos | Alta básica de taller |
| `password_reset_tokens` | PK `id`, hash de token único, FK `user_id` | Recuperación de contraseña |

## Diagrama entidad–relación actual

```mermaid
erDiagram
  USERS ||--o{ PASSWORD_RESET_TOKENS : "solicita"
  USERS {
    int id PK
    string email UK
    string password_hash
    enum role
    boolean is_active
  }
  PASSWORD_RESET_TOKENS {
    int id PK
    int user_id FK
    string token_hash UK
    datetime expires_at
    datetime used_at
  }
  ROLE_DEFINITIONS {
    int id PK
    string name UK
    boolean status
  }
  WORKSHOPS {
    int id PK
    string name UK
    string rfc UK
  }
  CUSTOMERS {
    int id PK
    string email UK
  }
```

`role_definitions` no es todavía una FK de `users.role`: el usuario usa un enum técnico. Tampoco existe relación entre `users`, `workshops` y `customers`; por ello el aislamiento por taller no está implementado y no debe declararse terminado.

## Entidades propuestas — fases posteriores

```mermaid
erDiagram
  WORKSHOPS ||--o{ WORKSHOP_USERS : "asigna"
  USERS ||--o{ WORKSHOP_USERS : "pertenece"
  WORKSHOPS ||--o{ CUSTOMERS : "contextualiza"
  CUSTOMERS ||--o{ CUSTOMER_VEHICLES : "relaciona"
  VEHICLES ||--o{ CUSTOMER_VEHICLES : "tiene vigencia"
  WORKSHOPS {
    int id PK
  }
  WORKSHOP_USERS {
    int workshop_id FK
    int user_id FK
    string role
    boolean status
  }
  CUSTOMERS {
    int workshop_id FK
    boolean status
  }
  VEHICLES {
    int id PK
    int workshop_id FK
    string vin UK
    boolean status
  }
  CUSTOMER_VEHICLES {
    int customer_id FK
    int vehicle_id FK
    datetime valid_from
    datetime valid_to
  }
```

Este segundo diagrama es una propuesta, no una migración ni un esquema aplicado. Cualquier cambio de esquema deberá entrar mediante una nueva migración versionada; no se deben modificar tablas ya aplicadas manualmente.

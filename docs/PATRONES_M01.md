# Patrones de diseño para M01

## Decisión

Strategy y Command son apropiados, pero la lógica actual reside directamente en rutas y dependencias. Aplicarlos correctamente exige introducir una capa de servicios y pruebas dedicadas; hacerlo ahora modificaría transversalmente M01. Por ello se documenta la propuesta y se pospone su implementación hasta recibir autorización explícita.

## Strategy — política de contraseña

- **Problema:** las reglas de contraseña están repetidas en `RegisterRequest` y `PasswordChangeRequest`; futuras políticas pueden variar por configuración o entorno.
- **Objetivo:** encapsular la validación en `PasswordPolicy` y usar una estrategia `StrongPasswordPolicy` sin cambiar los contratos HTTP.
- **Componentes propuestos:** protocolo `PasswordPolicy`, estrategia actual de mayúscula/minúscula/dígito y servicio de credenciales.
- **Ubicación propuesta:** `backend/app/services/password_policy.py`, invocado por esquemas o por un servicio de autenticación.
- **Ejemplo:** producción puede exigir longitud mayor sin editar todas las rutas.

## Command — operaciones administrativas

- **Problema:** crear rol, cambiar su estado y cambiar el rol de un usuario combinan ruta, autorización y persistencia.
- **Objetivo:** representar mutaciones como comandos transaccionales y concentrar reglas de negocio.
- **Componentes propuestos:** `CreateRoleCommand`, `ChangeRoleStatusCommand`, `AssignUserRoleCommand` y un manejador/servicio que reciba la sesión.
- **Ubicación propuesta:** `backend/app/services/commands/` y pruebas unitarias independientes de FastAPI.
- **Ejemplo:** `AssignUserRoleCommand` verifica que el administrador no se retire su propio permiso y persiste el cambio.

## Criterio para implementar

La implementación se autoriza cuando se cree la capa de servicios de M01 y sus pruebas. No deben transformarse las consultas de lectura en comandos ni duplicarse los controles de autorización de FastAPI.

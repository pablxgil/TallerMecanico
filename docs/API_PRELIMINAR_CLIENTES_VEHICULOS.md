# API preliminar — clientes y vehículos

> Diseño futuro. No se implementan ni se amplían estos endpoints en esta entrega. El `workshopId` nunca debe recibirse libremente en el cuerpo o query; debe derivarse de la identidad autenticada y de las políticas del backend.

| Método | Endpoint | Propósito | Observación REST |
|---|---|---|---|
| POST | `/api/v1/customers` | Crear cliente | Contexto de taller del JWT |
| GET | `/api/v1/customers` | Buscar/listar | Paginación y filtros normalizados |
| GET | `/api/v1/customers/{customerId}` | Consultar ficha | Aislamiento por taller |
| PATCH | `/api/v1/customers/{customerId}` | Actualizar | `PUT` solo si se define reemplazo completo |
| POST | `/api/v1/customers/{customerId}/deactivate` | Desactivar | Acción explícita de baja lógica |
| POST | `/api/v1/vehicles` | Crear vehículo | Debe asociarse al contexto de taller |
| GET | `/api/v1/vehicles` | Buscar/listar | Paginación y autorización |
| GET | `/api/v1/vehicles/{vehicleId}` | Consultar vehículo | Aislamiento por taller |
| PATCH | `/api/v1/vehicles/{vehicleId}` | Actualizar | Validar placas/VIN al definir reglas |
| POST | `/api/v1/vehicles/{vehicleId}/deactivate` | Desactivar | Baja lógica |
| POST | `/api/v1/customer-vehicles` | Crear relación | Debe verificar ambos recursos en el taller |
| GET | `/api/v1/customers/{customerId}/vehicles` | Vehículos del cliente | Relación vigente/histórica definida explícitamente |
| GET | `/api/v1/vehicles/{vehicleId}/customers/current` | Cliente vigente | Útil si la relación tiene vigencia |

BR-01: cada cliente pertenece a un contexto de taller. Para modelar la relación cliente–vehículo se propone una entidad intermedia con fechas de vigencia; no se crea en esta entrega.

# Casos de uso

## UC-M01-01 — Registrar cuenta

- **Disparador:** una persona selecciona Crear cuenta.
- **Precondiciones:** API disponible; correo no registrado.
- **Entrada:** nombre, correo y contraseña.
- **Validación:** formato de correo, longitud y composición de contraseña, unicidad de correo.
- **Ejecución:** normaliza correo, genera hash Argon2 y persiste la cuenta con rol `usuario`.
- **Postcondiciones:** cuenta activa creada sin privilegios administrativos.
- **Auditoría:** pendiente; no existe tabla/evento de auditoría persistente.
- **Respuesta:** `201 UserResponse`; duplicado `409`; errores de formato `422`.
- **Excepciones:** fallo de base de datos o hash; debe responderse sin exponer secretos.
- **Pruebas:** alta válida, correo duplicado, contraseña inválida y normalización.

## UC-M01-02 — Iniciar sesión y autorizar

- **Disparador:** envío del formulario de acceso.
- **Precondiciones:** cuenta activa existente.
- **Entrada:** correo y contraseña.
- **Validación:** formato, credenciales y estado activo.
- **Ejecución:** verifica hash, emite JWT y Vue conserva sesión; rutas/API autorizan por token y rol.
- **Postcondiciones:** sesión utilizable hasta expirar.
- **Auditoría:** pendiente.
- **Respuesta:** `200 TokenResponse`; `401` credencial inválida; `403` cuenta o rol no autorizado.
- **Excepciones:** JWT inválido, expirado o usuario inexistente.
- **Pruebas:** login válido/inválido, endpoint protegido, sesión expirada y permisos por rol.

## UC-M01-03 — Cambiar o recuperar contraseña

- **Disparador:** usuario autenticado cambia clave o solicita recuperación.
- **Precondiciones:** cambio: JWT válido; recuperación: correo registrado y token temporal válido.
- **Entrada:** contraseña actual/nueva, o correo/token/nueva contraseña.
- **Validación:** política de contraseña, clave nueva distinta y vencimiento/uso único del token.
- **Ejecución:** actualiza hash Argon2 dentro de transacción; recuperación marca token como usado.
- **Postcondiciones:** solo la nueva contraseña permite acceso.
- **Auditoría:** pendiente.
- **Respuesta:** cambio `204`; recuperación `200`; errores `400/401/422` según causa.
- **Excepciones:** token vencido, cuenta inexistente sin revelarla y error de entrega de correo (no integrado).
- **Pruebas:** cambio correcto/incorrecto/reutilizado; recuperación con token válido, usado y vencido.

## UC-M01-04 — Administrar roles y taller

- **Precondiciones:** administrador para roles; administrador, recepcionista o asesor para alta de taller.
- **Entrada:** nombre/descripción/estado de rol; datos de taller y RFC.
- **Validación:** privilegio, duplicados, RFC, correo, CP y restricciones de unicidad.
- **Ejecución:** crea o desactiva lógicamente roles; registra taller en transacción.
- **Postcondiciones:** registro persistido o estado actualizado.
- **Auditoría:** pendiente.
- **Respuesta:** `201/200`; `403` por rol; `409` duplicado; `422` formato.
- **Excepciones y pruebas:** falta cubrir autorización, duplicados, RFC y baja lógica mediante pruebas automatizadas.

## UC-CV-01 — Registrar cliente (diseño futuro; no implementado en esta entrega)

- **Precondiciones:** usuario autenticado/autorizado y taller activo derivado de identidad.
- **Entrada:** nombre completo y al menos un medio de contacto según configuración.
- **Validación:** normalización, formato, posibles duplicados y prohibición de recibir libremente `workshopId`.
- **Ejecución:** abrir alta → capturar → normalizar → buscar coincidencias → confirmar → persistir → auditar.
- **Postcondiciones:** cliente activo aislado al taller.
- **Auditoría:** evento de alta con actor y taller.
- **Respuesta:** `201` o conflicto/validación claros.
- **Excepciones:** duplicado probable, taller inactivo, acceso denegado, error transaccional.
- **Pruebas:** positivos, duplicados, límites, formatos, autorización y aislamiento entre talleres.

## UC-CV-02 — Consultar, actualizar y desactivar cliente (diseño futuro)

- **Flujo principal:** ingresar criterios normalizados → búsqueda paginada → coincidencias → ficha; actualizar/desactivar tras confirmar permiso.
- **Criterios:** nombre, teléfono, correo, identificador y combinaciones permitidas.
- **Precondiciones/validación:** actor autorizado, taller derivado de JWT, registro del mismo taller y estado permitido.
- **Ejecución/postcondición:** consulta no muta; actualización conserva integridad; desactivación cambia estado sin borrar.
- **Auditoría/respuesta/excepciones/pruebas:** registrar actor/antes-después; responder `200/204/404/403/409`; probar aislamiento, paginación, límites y bajas lógicas.

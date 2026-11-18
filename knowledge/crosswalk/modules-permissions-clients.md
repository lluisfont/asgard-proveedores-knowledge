# Modulos, permisos y clientes

AS-IS estatico del commit `a8ce2c23dead8552d2c4699e4a9b9134f7a18707`, rama `master`. Los candidatos requieren verificar configuracion y despliegue.

[Actores y permisos](../general/actors-and-permissions.md) desarrolla los tipos de proveedor y el contexto de sesion observado. Las 7 marcas heuristicas de permiso del extractor proceden de licencias/codigo de dependencias y no se usan como prueba de permisos de negocio. Las fuentes relevantes revisadas son:

| Referencia | Fuente fijada | Control observado y limite |
| --- | --- | --- |
| AUTH-M-01 | `M:index_archivos/permisos.php:L1-L27` | Guardia compartida de sesion; terminacion de rechazo condicionada por runtime, ver SEC-005 |
| AUTH-M-02 | `M:index_archivos/MenuClass.php:L25-L40` | Permisos de menu por usuario y modulo; no acredita autorizacion de cada handler |
| AUTH-M-03 | `M:src/core/users/application/Find/UserFind.php:L16-L61` | Tipo de proveedor y contexto de empresa; no equivale a una matriz de permisos |
| AUTH-M-04 | `M:index_archivos/tracking/guardia_imagen.php:L1-L5` | Sesion y validacion parcial de ruta; propiedad del recurso pendiente |

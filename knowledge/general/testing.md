# Pruebas y regresion

## Ampliación iterativa del 18-11-2026

Se añaden pruebas de contrato del exportador (3/3), firma de aridad con cuerpo centinela (3/3), inyección de fallos transaccionales (34/34, incluidos 15 controles negativos), contratos y representaciones tipadas en PHP/Node, y tres controles negativos de SQL AST. Un resultado reproducido puede demostrar un defecto; no equivale a aprobar el comportamiento. Los [resultados y límites](../reviews/iterative-20261118/README.md) incluyen el censo estático de 279 PHP, 460 declaraciones y 542 llamadas resueltas, más los cierres independientes. No se ejecutó SQL, bootstrap ni tráfico de aplicación.

El Knowledge Pack diferencia verificaciones ejecutadas y escenarios que
requieren un entorno controlado de aplicacion. Las comprobaciones estaticas
no equivalen a una prueba funcional de produccion.

## Ejecutado

| Comprobacion | Resultado y evidencia |
| --- | --- |
| Inventario de master y comparacion con master_peru | Archivos y commits en `source-audits/master/2026-11-18/inventory.csv` y `branch-comparison.json` |
| Sintaxis PHP | 279 archivos, 3 fallos bajo PHP 8.4.25 con short_open_tag activado; `php-lint.json` |
| Extraccion AST Graphify | 545 archivos seleccionados, 2,173 nodos y 2,711 aristas; 319 archivos sin simbolos mas alla del nodo de archivo |
| Baseline Brownfield | 1,091 evidencias; baseline provisional, esquema SQL de master no disponible |
| Catalogo PHP/AJAX | 241 candidatos expuestos y 20 candidatos de consumo; requiere validar rutas efectivas |
| Guardas de descarga | Casos aislados de sesion y rutas en `guard-probes.json`; no se ejecutan handlers ni consultas |
| Metodos y guardas de seguridad | 12/12 casos independientes reproducibles en `security-probes.json`, con efectos externos sustituidos en memoria |
| Instalacion y cobertura | Checkout aislado: mismo commit con esquema pendiente; cambio funcional sin commit detectado y rechazado |
| Integridad del paquete | Hashes de artefactos exportados, formato de glosario, referencias de evidencia y documentos |

## Escenarios de caracterizacion propuestos

Estos escenarios son planes, no resultados ya obtenidos. Se apoyan en las
ubicaciones detalladas en [procesos](workflows.md), [reglas](business-rules.md)
y [seguridad](security-audit.md).

| ID | Proceso | Datos y comprobaciones |
| --- | --- | --- |
| QA-01 | Acceso | Credenciales correctas/incorrectas, usuario inactivo, caducidad, CSRF ausente y reutilizado; comprobar sesion y destino real |
| QA-02 | Segundo factor | Codigo correcto, incorrecto, expirado, reenvio y manipulacion de identificadores; comprobar identidad y contexto efectivos |
| QA-03 | Cambio y recuperacion de clave | Identidad propia y ajena, clave anterior y token de recuperacion; verificar rechazos y almacenamiento sin registrar secretos |
| QA-04 | Cotizacion y embarque | Crear y editar con campos obligatorios, tramos vacios y datos de otra cuenta; comprobar persistencia y visibilidad |
| QA-05 | Asignacion y seguimiento de viaje | Asignar operador, unidad y transportista; verificar estados, historial, ubicaciones y visibilidad por proveedor |
| QA-06 | Archivos | Sesion ausente, propietario ajeno, ruta relativa, ruta rechazada, extension/contenido/tamano invalidos; comprobar controles del handler completo |
| QA-07 | Cargas masivas | Plantilla valida, cabeceras incompletas, filas invalidas, duplicados y errores parciales; documentar atomicidad real |
| QA-08 | Reportes y exportaciones | Mismos filtros y datos bajo roles distintos; comprobar limites de cuenta, formatos, zona horaria y contenido sensible |
| QA-09 | Integraciones | Servicio disponible, timeout, error y respuesta invalida; registrar efectos parciales y reintentos reales |
| QA-10 | Variante Bolivia | Rutas y cotizaciones nacionales, etiquetas de pais y zona horaria sobre master |
| QA-11 | Variante Peru | Pedidos, preembarques, concesionarios y flujos exclusivos sobre master_peru |
| QA-12 | Compatibilidad PHP | Ejecutar flujos representativos en la version real del despliegue y en la version objetivo antes de migrar |

## Datos de prueba

Usar una base aislada y cuentas de cada tipo de proveedor y cliente. No asumir
que el dump historico de Peru representa el esquema ni la poblacion de master.
Los casos de mutacion deben ejecutarse con un procedimiento de restauracion
acordado y registros de resultado observados. La auditoria actual no envio
peticiones contra servicios externos ni modifico bases de datos.

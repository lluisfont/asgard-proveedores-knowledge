# SEC-015 — El exportador acepta operaciones SQL completas del cliente

Prioridad P1; defecto de contrato confirmado en fuente, impacto en producción condicionado y sin verificar. No canónico; recomendación TO-BE pendiente de revisión.

El formulario activo transmite la consulta completa en un campo oculto, en vez de un identificador de informe con filtros. El exportador divide `POST query` por `xxx`, entrega cada segmento auxiliar a `mysqli_query` y finalmente ejecuta el segmento inicial. El servidor no impone en esos bloques un catálogo de consultas ni que las operaciones sean solo de lectura.

Evidencia: `M:index_archivos/reportes/reportecontrolol.php:L111-L118`; `M:index_archivos/reporteexcel/reporteexcel.php:L11-L25,L52-L58`. Fuente master `a8ce2c23dead8552d2c4699e4a9b9134f7a18707`.

La [prueba aislada](../../../source-audits/master/2026-11-18/iterative/report-contract-probes.json) reproduce tres contratos con sustitutos en memoria: selección simple y uno o varios segmentos auxiliares antes de la selección. No contacta una base de datos ni ejecuta el bootstrap o una petición HTTP. Los nombres sintéticos no corresponden a tablas de la aplicación. [Script reproducible](../../../scripts/audit/report_contract_probes.py).

Se requiere un exportador accesible con bootstrap y conexión operativos, además de los controles de acceso aplicables. Los permisos del usuario SQL limitan el impacto; no se comprobaron privilegios, filas afectadas ni accesibilidad anónima. La guardia compartida conserva las limitaciones de runtime descritas en SEC-005. Tampoco se presupone soporte de múltiples sentencias dentro de una llamada SQL: cada segmento ya se despacha mediante una llamada separada.

**Diferencia respecto a SEC-006:** aquel hallazgo trata valores interpolados dentro de consultas construidas por el servidor. Aquí el cliente elige la operación completa y su secuencia; parametrizar únicamente filtros no resuelve esa frontera de confianza. Los procesos anteriores mencionaban el transporte de SQL, pero no registraban este defecto con sus precondiciones y prueba.

Recomendación: seleccionar en el servidor una consulta autorizada mediante un identificador de informe, enlazar valores tipados y aplicar los filtros de cuenta/ámbito en el servidor. Evitar cualquier entrada que elija SQL completo. Verificar permisos de solo lectura donde proceda y realizar pruebas de autorización en un entorno de aplicación controlado.

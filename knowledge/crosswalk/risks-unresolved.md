# Riesgos y decisiones pendientes

El baseline es `INCOMPLETE_BASELINE`, sin confirmacion humana ni commit Git auditado. La API nativa es `partial`; el catalogo aumentado es estatico. La comparacion del inventario auditado con el checkout actual devuelve:

| Resultado SHA256 | Archivos |
| --- | --- |
| different | 48 |
| missing | 5 |
| same | 1452 |

Fuente: `knowledge/snapshots/current/audited-source-comparison.json`. Esta comparacion no incluye archivos adicionales ni demuestra cobertura del dump SQL actual.

| Familia de senales API | Filas candidatas |
| --- | --- |
| NO_CSRF | 74 |
| NO_LOCAL_AUTH | 70 |
| CALLER_REFERENCED | 56 |
| IDOR_CANDIDATE | 51 |
| SENSITIVE_TABLE_ACCESS | 50 |
| UPLOAD_IMPORT | 50 |
| FK_GAP_TABLE_ACCESS | 49 |
| LEGACY_MYSQL_API | 43 |
| SQL_TAINT | 16 |
| DB_WRITE | 7 |
| DANGEROUS_SINK | 3 |
| PATH_TRAVERSAL_CANDIDATE | 2 |
| PASSWORD_CHANGE_NO_LOCAL_AUTH | 2 |

Fuente: `source-audits/api/api-deep-iterative/endpoint_deep_risks.csv`. La falta de una senal local de auth o CSRF no demuestra ausencia de un control compartido. SQL taint, IDOR, uploads y rutas de archivo requieren validacion contextual.

Las semanticas de negocio, las relaciones inferidas, los borradores de release y los defectos funcionales siguen pendientes. Las auditorias de la herramienta Graphify estan en `source-audits/related-graphify-audits/` y no deben mezclarse con Proveedores.

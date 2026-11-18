# Mapa de evidencias actual

AS-IS estatico del commit `a8ce2c23dead8552d2c4699e4a9b9134f7a18707`, rama `master`. Los candidatos requieren verificar configuracion y despliegue.

| Area | Evidencia actual |
| --- | --- |
| Procedencia | [Alcance](audit-scope.md), [manifiesto](manifest.json), [hashes actuales](current-artifacts.json) |
| Conceptos y reglas | [Glosario](glossary/business-glossary.md), [reglas](general/business-rules.md), [procesos](general/workflows.md) |
| Variantes | [Bolivia](variants/bolivia.md), [Peru](variants/peru.md), [comparacion](variants/comparison.md) |
| Fuente versionada | [Inventario](../source-audits/master/2026-11-18/inventory.csv), [diferencias](../source-audits/master/2026-11-18/branch-comparison.csv) |
| Graphify | [Grafo comprimido](../source-audits/master/2026-11-18/graphify/graph.json.gz), [metricas](../source-audits/master/2026-11-18/graphify/summary.json) |
| Brownfield | [Evidencias](../source-audits/master/2026-11-18/brownfield/evidence/summary.json), [mapa tecnico](../source-audits/master/2026-11-18/brownfield/process_maps/PROCESS_MAP.md) |
| Datos | [Modelo](general/data-model.md), [candidatos SQL](general/table-reference.md), [referencias con linea](../source-audits/master/2026-11-18/sql-references.csv) |
| API | [Referencia](general/api-reference.md), [campos](../source-audits/master/2026-11-18/request-fields.csv), [catalogo](../source-audits/master/2026-11-18/brownfield/custom/http_endpoint_catalog.csv) |
| Seguridad | [Revision](general/security-audit.md), [hallazgos](general/security-findings.json) |
| Ampliación iterativa | [Delta aceptado](reviews/iterative-20261118/accepted-deltas.json), [versiones](reviews/iterative-20261118/iterations.json), [defectos operativos](general/operational-findings.json) |
| Verificaciones | [Validacion del paquete](snapshots/current/knowledge-validation.json), [lint](../source-audits/master/2026-11-18/php-lint.json), [guardas](../source-audits/master/2026-11-18/guard-probes.json) |
| Limites | [Cobertura documental](documentation-coverage.md), [pendientes](general/open-questions.md) |
| Historia Peru | [Mapa original](history/evidence-map-20261001.md), [transferencia](transfer-scope.md) |

El DDL de Peru se conserva como historial, no como esquema de master. Los archivos no verificados en ejecucion, las inferencias y los controles de despliegue pendientes mantienen su estado explicito. Los hashes validan transporte, no correccion funcional.

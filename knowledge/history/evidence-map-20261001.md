# Mapa de conocimiento disponible

Las rutas corresponden al paquete exportado. Los archivos de texto de mas de
1 MB terminan en `.gz`; su contenido se conserva completo y se puede restaurar
con `scripts/transfer/restore_artifacts.py`.

| Pregunta | Evidencia inicial |
| --- | --- |
| Que se audito y con que limites | `transfer-scope.md`, `manifest.json`, `transfer-artifacts.json` |
| Arquitectura y dependencias | `../source-audits/graphify/GRAPH_REPORT.md`, `../source-audits/graphify/graph.json.gz`, `../source-audits/graphify/graph.html` |
| Evidencia estatica y trazabilidad | `../source-audits/brownfield/reports/evidence/` |
| Modelo fisico de datos | `../source-audits/brownfield/reports/data_dictionary/` |
| Terminos y significados candidatos | `../source-audits/brownfield/reports/business_glossary/`, `../source-audits/brownfield/reports/data_dictionary/semantic_data_dictionary.json.gz` |
| Flujos, componentes y escrituras | `../source-audits/brownfield/reports/process_maps/`, `../source-audits/brownfield/reports/semantic_flow_analysis/` |
| Endpoints PHP/AJAX | `../source-audits/api/asgard-api-audit-augmented/api-catalog.augmented.json` |
| OpenAPI provisional | `../source-audits/api/asgard-api-audit-augmented/openapi.augmented.yaml` |
| Consumo de servicios externos | `../source-audits/api/asgard-api-audit-augmented/consumed_api_augmented.csv` |
| Riesgos por endpoint | `../source-audits/api/api-deep-iterative/endpoint_deep_risks.csv` |
| Riesgos por consumidor | `../source-audits/api/api-deep-iterative/consumer_deep_risks.csv` |
| SQL, uploads y sinks peligrosos | `../source-audits/brownfield/reports/custom/DEEP_SECURITY_FINDINGS.md` |
| Integridad y sensibilidad de datos | `../source-audits/brownfield/reports/custom/DATA_MODEL_INTEGRITY_FINDINGS.md` |
| Versiones iterativas de Proveedores | `../source-audits/brownfield/reports/iterative/` |
| Plantillas y borradores de ingenieria, negocio y OpenSpec | `../source-audits/brownfield/reports/release/` |
| Cobertura real del baseline | `../source-audits/brownfield/reports/completeness/ANALYSIS_COMPLETENESS_REPORT.md` |
| Cambios frente al checkout actual | `snapshots/current/audited-source-comparison.json` |
| Checkpoints historicos recuperables | `../source-audits/history/` |
| Auditorias relacionadas de Graphify | `../source-audits/related-graphify-audits/` |

## Magnitudes historicas

Fuente: informes y artefactos de Proveedores fechados 2026-09-15.

| Area | Magnitud | Interpretacion |
| --- | ---: | --- |
| Graphify | 48,495 nodos; 116,642 aristas | Incluye dependencias externas |
| Brownfield | 1,505 archivos; 4,471 evidencias | Alcance reducido, mayoritariamente SQL |
| Datos | 1,055 tablas; 10,111 columnas | Estructura extraida del dump historico |
| Datos | 66 relaciones; 1,365 indices; 819 constraints | Declaraciones fisicas; no equivalen a todas las relaciones de negocio |
| Objetos SQL | 54 procedures; 42 functions | Logica que debe considerarse en cambios |
| Procesos | 66 componentes; 530 nodos; 4,178 aristas | Mapa tecnico candidato |
| API aumentada | 246 candidatos expuestos; 23 candidatos de consumo | Analisis estatico; no inventario de rutas confirmado en ejecucion |
| API profunda | 194 filas de riesgo endpoint; 22 de consumidor | Familias de senales que requieren revision |

Los identificadores de evidencia y ubicaciones de fuente tienen prioridad sobre
las descripciones inferidas. Para requisitos nuevos, registrar el comportamiento
demostrado, la decision pendiente y el impacto tecnico por separado.

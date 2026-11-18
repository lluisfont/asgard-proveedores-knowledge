# Cobertura de la documentacion

Esta matriz documenta el alcance real de los entregables. La existencia de un
documento no acredita validacion de negocio, despliegue ni cierre de riesgos.

| Area | Entregable actual | Estado y limites |
| --- | --- | --- |
| Procedencia y fuentes | audit-scope.md, manifest.json, inventario y comparacion de blobs | Commits fijados; checkout y diferencias trazables |
| Arquitectura y stack | general/architecture.md, general/operations.md, grafo AST | Documentado desde codigo; runtime real pendiente |
| Capacidades y dominios | product/business-domains.md, general/workflows.md | Procesos reconstruidos; validacion de negocio pendiente |
| Actores y autorizacion | general/actors-and-permissions.md | Tipos y guardas observados; matriz efectiva por tenant pendiente |
| Reglas de negocio | general/business-rules.md | Reglas con evidencia; separar inferencias y comportamiento requerido |
| Diccionario de negocio | glossary/business-glossary.md, JSON y CSV | Conceptos revisados contra codigo, sin aprobacion de negocio |
| Candidatos previos | glossary/historical-candidates-disposition.csv | Todos los 891 candidatos historicos tienen disposicion individual |
| Datos | general/data-model.md, general/table-reference.md | Referencias SQL; DDL de master ausente |
| SQL local candidato | general/local-schema-candidate.md, source-audits/local-schema-candidate/ | Estructura local extraida; pais y correspondencia con master sin acreditar |
| API y contratos | general/api-reference.md, catalogos CSV/JSON/OpenAPI provisional | Candidatos estaticos; nativo ASGARD bloqueado; HTTP real pendiente |
| Integraciones | general/integrations.md | Call sites y simbolos de configuracion; servicios y submodulos no verificados |
| Flujos y manual | general/workflows.md, general/user-manual.md | Pantallas y secuencias respaldadas por codigo; prueba de usuario pendiente |
| Variantes pais | variants/bolivia.md, variants/peru.md, variants/comparison.md | Diferencias de fuente observadas; configuracion efectiva pendiente |
| Seguridad | general/security-audit.md, general/security-findings.json | Hallazgos revisados y precondiciones; riesgos abiertos |
| Operacion y configuracion | general/operations.md | Receta versionada; operaciones reales y recuperacion no suministradas |
| QA y pruebas | general/testing.md, php-lint.json, guard-probes.json | Chequeos ejecutados separados de escenarios propuestos |
| Requisitos y cambios | general/requirements-guide.md, openspec/ | Guia AS-IS e impacto; no especificacion TO-BE aprobada |
| Trazabilidad y verificacion | current-artifacts.json, export-manifest.json, knowledge-validation.json | Integridad, evidencia y enlaces; no certificacion de aplicacion |
| Historia | history/manifest-20261001.json, transfer-artifacts.json, source-audits/history/ | Preservada con alcance Peru y hashes originales |

Los faltantes accionables se registran en `general/open-questions.md`. En
particular, no se reconstruyen tipos SQL, relaciones fisicas, aprobaciones
de roles ni procedimientos operativos a partir de nombres de tablas o
plantillas historicas. Estas dimensiones permanecen pendientes de evidencia.

# Indice del conocimiento de Proveedores

Fuente principal: master `a8ce2c23dead8552d2c4699e4a9b9134f7a18707`.
Comparacion: master_peru `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62`.
Los conceptos comunes requieren evidencia en ambas variantes; identidad de
ficheros no demuestra identidad de configuracion, datos o despliegue.

| Area | Documento principal |
| --- | --- |
| Alcance y evidencia | [Auditoria actual](audit-scope.md), [mapa de evidencia](evidence-map.md), [manifiesto](manifest.json) |
| Diccionario de negocio | [Glosario](glossary/business-glossary.md), [JSON](glossary/business-glossary.json), [CSV](glossary/business-glossary.csv), [revision](glossary/review-register.md) |
| Candidatos historicos | [Disposicion de los 891 terminos del extractor](glossary/historical-candidates-disposition.csv) |
| Dominios y capacidades | [Modulos](product/business-domains.md), [procesos](general/workflows.md) |
| Actores, permisos y cuentas | [Actores](general/actors-and-permissions.md), [crosswalk](crosswalk/modules-permissions-clients.md) |
| Reglas y requisitos | [Reglas](general/business-rules.md), [guia de requisitos](general/requirements-guide.md) |
| Manual de usuario | [Manual reconstruido](general/user-manual.md) |
| Arquitectura | [Componentes y dependencias](general/architecture.md) |
| Datos | [Modelo y limites](general/data-model.md), [referencias de tablas](general/table-reference.md) |
| SQL local sin autoridad confirmada | [Diccionario estructural candidato](general/local-schema-candidate.md) |
| API | [Referencia](general/api-reference.md), [pantallas, endpoints y tablas](crosswalk/screens-endpoints-tables.md) |
| Integraciones | [Servicios y contratos](general/integrations.md) |
| Bolivia | [Particularidades de master](variants/bolivia.md) |
| Peru | [Particularidades de master_peru](variants/peru.md) |
| Comparacion | [Matriz funcional y tecnica](variants/comparison.md), [indice de variantes](variants/README.md) |
| Obligaciones por rama | [EDP, fechas, eventos y lugares](reviews/iterative-20261118/branch-obligations.md), [registro JSON](reviews/iterative-20261118/branch-obligations.json) |
| Seguridad | [Auditoria revisada](general/security-audit.md), [hallazgos JSON](general/security-findings.json) |
| Revisión iterativa | [Cambios frente a la auditoría anterior](reviews/iterative-20261118/README.md), [defectos operativos](general/operational-findings.md), [registro de pasadas](reviews/iterative-20261118/iterations.json) |
| Operacion | [Configuracion y despliegue](general/operations.md) |
| Pruebas | [Resultados y escenarios](general/testing.md) |
| Cobertura y pendientes | [Matriz documental](documentation-coverage.md), [preguntas abiertas](general/open-questions.md) |
| Trabajo de ingenieria | [Contexto OpenSpec](openspec/context.md), [reglas de impacto](openspec/impact-rules.md) |
| Reproducir el trabajo | [Receta del perfil fijado](operations/reproduce-audit.md), [informe actual](../source-audits/master/2026-11-18/AUDIT_REPORT.md) |
| Historia | [Transferencia original](transfer-scope.md), [manifiesto original](history/manifest-20261001.json) |

El paquete permite consulta tecnica y funcional sin codigo fuente. Los enlaces
a GitHub conservan los commits de origen y requieren acceso al repositorio
privado. El estado global PARTIAL expresa dimensiones pendientes, no ausencia
de documentacion ni finalizacion ficticia de la validacion de negocio.

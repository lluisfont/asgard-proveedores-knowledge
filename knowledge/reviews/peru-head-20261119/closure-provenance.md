# Revisión de procedencia Perú HEAD

Fecha: **19-11-2026, Europe/Madrid**. HEAD `2a179e2e6472d5705d031665ecbc90c3d806edec`; P95 `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62`; M histórico `a8ce2c23dead8552d2c4699e4a9b9134f7a18707`; KB baseline `0c4bb99f076d6a8c18ae98375d6e154da6319922`.

**Estado: completado. Pase de cierre sin delta material dentro del alcance publicado.**

La técnica es trazabilidad inversa con mutaciones de metadatos: afirmación publicada → ID aceptado → origen TEMP → evidencia/contexto → pins y pruebas delegadas. Distingue clasificación, procedencia temporal y límites de inferencia; no repite solamente la igualdad de blobs ni el análisis AST del agente SQL.

Las tres mejoras PH-IMP-006/007/008 están integradas en los seis archivos asignados. El mapa aceptado conserva cuatro hallazgos y ocho mejoras; solo PH-001 tiene efecto cambiado por HEAD. El cierre sobre la publicación padre no aportó deltas materiales nuevos. `new_findings=[]` e `improvements=[]` describen este pase completado y permiten la convergencia del alcance revisado, no una convergencia global.

## Snapshot padre verificado

- `knowledge/reviews/peru-head-20261119/README.md`
- `knowledge/variants/peru-head-20261119.md`
- `knowledge/reviews/peru-head-20261119/accepted-deltas.json`

Los tres archivos quedaron fijados por SHA256 en `closure-provenance.json`. Los doce IDs publicados se rastrearon hasta sus registros de informe o carry-forward, conservando clasificación, origen, pins y evidencia.

## Comprobaciones completadas

| ID | Resultado |
| --- | --- |
| OWN-01_HISTORICAL_BODY_AND_PREFIXES | preserved |
| OWN-02_GLOSSARY_81_UNCHANGED | 80 P carried; 1 M only; no new concept or M-to-P mapping |
| OWN-03_API5_HEAD_REQUESTS | five requests with HEAD ranges and explicit exclusions |
| OWN-04_CF_ACCEPTANCE_MAP | TEMP-CF001/002/003 -> PH-IMP-006/007/008; improvements only |
| CP-01_ACCEPTED_12_SOURCE_ORIGINS | Human-accepted mapping: four new findings, eight documentary improvements; report nine origins plus CF three origins. |
| CP-02_ONE_CHANGED_THREE_INHERITED | PH-001 changed_role_effect; PH-002 inherited_P95_new_owner_boundary_consequence; PH-003/004 inherited_P95; no automatic four-regression claim. |
| CP-03_DELEGATED_TEST_LINKS | All accepted report test IDs exist in report-probes.json with pass status. Read only; not rerun and not treated as new dynamic proof. |
| CP-04_POSITIVE_SOURCE_PROVENANCE | 12/12 source-level controls pass. |
| CP-05_PROVENANCE_METADATA_MUTATIONS | 10/10 deliberate mutations rejected against accepted source-level provenance contracts. |
| CP-06_INTEGRATED_OVERLAY_MUTATIONS | 5/5 metadata mutations of actual integrated glossary overlay rejected; positive 81-entry overlay passes. |
| CP-07_SEMANTIC_LIMITS_REVERSE_OBLIGATIONS | Source obligations and non-entailments recorded for all 12 accepted items. Parent publication cannot yet be checked for preserving them. |
| CP-08_SQL_CLOSURE_DIFFERENT_TECHNIQUE | Delegated closure-sql is available and reports no deltas; its AST/metamorphic checks are not recounted as this provenance pass. |
| CP-09_PARENT_SNAPSHOT | README, página Perú HEAD y registro aceptado fijados por SHA256. |
| CP-10_PARENT_REVERSE_TRACE | 12/12 IDs publicados trazados al origen revisado con pins y evidencia sin cambios. |
| CP-11_PARENT_MUTATIONS | 6/6 mutaciones deliberadas rechazadas: clasificación, origen, pin, rango, conteo y frontera canónica. |

## Desafíos de metadatos

| Control | Resultado |
| --- | --- |
| MUT-01_IMPROVEMENT_AS_DEFECT | Rechazado; detecta classification |
| MUT-02_CROSSED_REPORT_ORIGIN | Rechazado; detecta origin_id |
| MUT-03_INHERITED_AS_HEAD_REGRESSION | Rechazado; detecta origin_change_vs_P95 |
| MUT-04_UNVERIFIED_AS_PRODUCTION | Rechazado; detecta runtime |
| MUT-05_CANONICAL_PROMOTION | Rechazado; detecta canonical |
| MUT-06_SHIFTED_REQUEST_RANGE | Rechazado; detecta origin_evidence_keys |
| MUT-07_REMOVED_DEPENDENCY_EVIDENCE | Rechazado; detecta origin_evidence_keys |
| MUT-08_KB_PIN_AS_SOURCE_PIN | Rechazado; detecta origin_evidence_keys |
| MUT-09_UNBACKED_STATEMENT | Rechazado; detecta origin_statement_sha256 |
| MUT-10_EXCLUDED_CALLBACK_SCOPE | Rechazado; detecta scope |
| MUT-11_INVENT_M_TO_P_CONCEPT | Rechazado; detecta peru_mapping:parte-recepcion |
| MUT-12_DROP_CHANGED_JS_DEPENDENCY | Rechazado; detecta changed_dependency:viaje-desde-vin |
| MUT-13_ADD_CONCEPT_82 | Rechazado; detecta concept_count, unknown_concept |
| MUT-14_REPLACE_ORIGINAL_SCOPE_EVIDENCE | Rechazado; detecta original_evidence:cliente-logistico |
| MUT-15_SHIFT_HEAD_RANGE | Rechazado; detecta range_mapping:cliente-logistico |

Los diez desafíos de origen se aplicaron al contrato de procedencia de los registros fuente aceptados; cinco desafíos adicionales se aplicaron al overlay real de 81 conceptos ya integrado. No se presentan como mutaciones sobre el snapshot principal, que aún no existe.

## Obligaciones que debe preservar la publicación

| ID | Soporte necesario | Límite de inferencia |
| --- | --- | --- |
| PH-001 | Acceso efectivo del tipo7 y colision de dominios son precondiciones; el cast no resuelve identidad. Solo este efecto se atribuye al cambio HEAD. | No demuestra acceso real de tipo7 ni politica aprobada de concesionario. |
| PH-002 | La construccion de fechas puede alterar el predicado; la cadena a data.php y las condiciones de parser/runtime/conexion deben permanecer. | Heredado P95; no explotacion SQL, lectura real ni anonymous bypass demostrado. |
| PH-003 | La cabecera acotada no acota todas las relaciones globales por chasis; multiplicidad/borrados condicionan el efecto. | No sustituye necesariamente p por otra cabecera ni generaliza el defecto a todas las CTE. |
| PH-004 | Maximos independientes pueden combinar atributos de distintas relaciones cuando hay multiplicidad. | No ocurre necesariamente con una sola relacion; ID maximo no demuestra orden temporal o estado correcto. |
| PH-IMP-001 | Proveedor de cabecera y concesionario seleccionan poblaciones diferentes. | No equivalencia de identificadores ni autorizacion completa acreditada. |
| PH-IMP-002 | Filtros por fila/tipo actuan antes del pivote y pueden retirar una columna de otro inventario. | No trasladar VAR-001 JS ni declarar requisito de conservar todas las columnas. |
| PH-IMP-003 | Realizado se apoya en presencia de registros; no completitud de secciones demostrada. | No declarar esa etiqueta incumplimiento de un contrato de negocio inexistente. |
| PH-IMP-004 | Constructor, includes, auxiliares y ejecutor tienen contratos y fallos distintos. | Ausencia en arbol no acredita fallo de despliegue; sin divulgacion en navegador ni continuacion universal. |
| PH-IMP-005 | query.php construye y data.php ejecuta en el contexto del caller. | No ejecucion autonoma demostrada, sin prueba HTTP ni parser SQL. |
| PH-IMP-006 | Cinco cabeceras/parametros de solicitudes conservan rangos, aunque el blob JS cambie. | Sin callbacks, respuesta, navegacion, salidas o recarga; no cinco APIs nuevas verificadas. |
| PH-IMP-007 | La evidencia local y el destino de dependencia directa tienen estados distintos. | No promover identidad local a equivalencia funcional compuesta ni a revision semantica global. |
| PH-IMP-008 | Evidencia P95 se arrastra como P95->HEAD; M conserva su procedencia. | 81 conceptos intactos, parte-recepcion solo M, seis mejoras historicas solo M; sin mapping inventado. |

## Resultado del cierre

La publicación conserva las obligaciones anteriores. Seis mutaciones del registro padre fueron rechazadas y no apareció un delta material adicional. Este pase es el segundo cierre consecutivo sin delta después del cierre SQL, por lo que el ledger puede declarar convergencia del alcance revisado. No se declara convergencia global ni se amplía la evidencia a runtime, datos o negocio.

## Límites

- Parent README, current Peru HEAD page and accepted-deltas registry are fixed in the JSON snapshot; a later edit requires a new closure run.
- Completed source-level/own-overlay checks are distinguished from pending publication checks; no completed global pass or consecutive-zero count claimed.
- No application, network, database, PHP/JS execution, browser/navigation/output/reload review or native auditor workaround.
- Two report PHP bodies remain delegated; only source sidecars, provenance, proof references and existing delegated closure inspected.
- Canonical glossary retains 81 definitions and original M/P95 evidence; no M-to-P mapping invented.
- Master remote a44 outside scope; source/manifest/index/general/finding registry/commits/push untouched by this task.

La evidencia y los resultados detallados están en [closure-provenance.json](closure-provenance.json); la aceptación CF y sus destinos, en [carryforward-integration.json](carryforward-integration.json).

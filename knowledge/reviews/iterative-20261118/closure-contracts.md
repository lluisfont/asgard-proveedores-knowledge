# Cierre acotado de contratos

**Nuevos hallazgos: 0. Mejoras materiales: 0.** Revisión posterior a la aceptación de OPS009. El principal cuenta el streak y genera ledger/fingerprints; no se declara convergencia global.

Fuente M `a8ce2c23dead8552d2c4699e4a9b9134f7a18707`; contraste P `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62`.

Técnica alternativa: cruce directo de predicados y callers con las afirmaciones documentadas, tablas por tipo/prioridad/población y contraejemplos. No se ejecutó vm ni nuevos probes de aplicación.

## Cruce de contratos HTTP

| Entrada | Método fuente | Interpretación documentada | Resultado |
| --- | --- | --- | --- |
| buscar-chasis: URL + type + data | POST | POST | consistent |
| resumen-inventario: URL + type + data | POST | POST | consistent |
| items.php hidden url_pedidos input | No es llamada | configuration_only_rejected_as_call | consistent |
| items include → ver_detalle_posiciones_pedido → settings | GET | GET | consistent |

Se sigue configuración → inclusión de script → función → objeto de petición. La fila PUT/root se conserva únicamente entre los 20 candidatos raw. Cambiar el pin, eliminar el candidato o duplicarlo hace fallar el overlay en vez de aplicarlo sin revisión.

## Decisión de estado por tipo

La tabla deriva de los predicados del pin y de la comparación PHP8.4.25 ya observada. Las condiciones de botón son independientes del rótulo; no se extrapola a PHP5.4 ni al tipo del driver desplegado.

| Tipo | Valor | Rótulo | Condición Interrumpir |
| --- | --- | --- | --- |
| NULL | null | Asignado | True |
| int | 0 | Asignado | False |
| string | "0" | Rechazado | False |
| int | 1 | Aceptado | True |
| string | "1" | Aceptado | True |
| int | 2 | Interrumpido | False |
| string | "2" | Interrumpido | False |
| int | 3 | Completado | False |
| string | "3" | Completado | False |
| int | 4 | Borrador | False |
| string | "4" | Borrador | False |

Fuente: `M/P:index_archivos/tracking/listaviajes.php:L203-L236`; botones M L273-L291 y P L275-L292; creación en ambos `TrackingNewClass.php:L1099-L1107`. JSON/Markdown/CSV conservan 81 entradas y solo cambia `/entries/69`.

## Decisión de inventario Perú

Se fijan daños/faltantes/contaminación en cero numérico y se cruzan tipos de pendiente/reportado. Son casos simbólicos, no respuestas observadas de la API. VAR001 ya cubre la inconsistencia entre coerción del agregado y comparación estricta; las prioridades no se convierten en un hallazgo separado.

| Pendiente tipo/valor | Reportado tipo/valor | Filtro Pendiente | Filtro Reportado | Sin observaciones | Completado | Botón |
| --- | --- | --- | --- | --- | --- | --- |
| number/1 | number/0 | True | False | False | False | Pendiente |
| number/1 | number/1 | True | True | False | False | Reportado |
| number/1 | string/"1" | True | False | False | False | Pendiente |
| string/"1" | number/0 | False | False | True | False | Detalle |
| string/"1" | number/1 | False | True | False | False | Reportado |
| string/"1" | string/"1" | False | False | True | False | none |
| number/0 | number/0 | False | False | True | True | Detalle |
| number/0 | number/1 | False | True | False | True | Reportado |
| number/0 | string/"1" | False | False | True | True | none |
| string/"0" | number/0 | False | False | True | True | Detalle |
| string/"0" | number/1 | False | True | False | True | Reportado |
| string/"0" | string/"1" | False | False | True | True | none |
| null/null | number/0 | False | False | True | True | Detalle |
| null/null | number/1 | False | True | False | True | Reportado |
| null/null | string/"1" | False | False | True | True | none |
| absent/null | number/0 | False | False | True | True | Detalle |
| absent/null | number/1 | False | True | False | True | Reportado |
| absent/null | string/"1" | False | False | True | True | none |

Fuente: `P:index_archivos/embarques/componentes/inventario-local/tabla-vehiculos.js:L75-L87,L129-L207`; `index.js:L8-L16,L147-L149`. Se contrasta con `knowledge/variants/peru.md#var-001`, que distingue tipos, población recibida y contexto nacional.

## Controles negativos y conocidos

- **NEG-CALL-BASE** (IMP-C1): URL_API in hidden input does not constitute a PUT request. Resultado: rejected_as_call.
- **NEG-RAW-OVERLAY** (IMP-C1): Rejected PUT remains in the clearly labeled raw table; it must not re-enter the reviewed contracts. Resultado: 20_raw_rows_preserved_3_reviewed_contracts.
- **NEG-ZERO** (IMP-C2): NULL and int0 share a display label under observed PHP8.4 behavior; string0 follows case0. Equal label is not equality of values or button conditions. Resultado: not_generalized_to_PHP54_or_DB_driver.
- **NEG-PENDING-STRING** (VAR001): {"pending_type": "string", "pending_value": "1", "reported_type": "number", "reported_value": 0, "damage_flags": "all_numeric_zero", "pending_filter": false, "reported_filter": false, "sin_observaciones_filter": true, "completed": false, "button": "Detalle", "known_id": "VAR001"} Resultado: known_type_inconsistency_not_new.
- **NEG-FLAG-PRIORITY** (VAR001): reportado=1 and pendiente=1 activate both filters, while the button chooses Reportado first. The documentation does not claim exclusive flags. Resultado: no_new_documentation_contradiction.
- **NEG-FILTER-AGGREGATE** (VAR001): A filtered visible subset of one of two received vehicles does not reduce the badge denominator2; the document now names the received population. Resultado: consistent.
- **NEG-COUNTRY** (VAR001): P-only counter predicates are not promoted to M or to all inventory namespaces. Resultado: scope_preserved.
- **NEG-ARITY** (OPS009): {"known_id": "OPS009", "caller_arguments": 1, "required_arguments": 2, "verdict": "known_mismatch_not_new", "evidence": [{"path": "index_archivos/embarques/embarquesController.php", "line_start": 20, "line_end": 20, "commit": "a8ce2c23dead8552d2c4699e4a9b9134f7a18707"}, {"path": "index_archivos/embarques/EmbarqueClass.php", "line_start": 129, "line_end": 129, "commit": "a8ce2c23dead8552d2c4699e4a9b9134f7a18707"}]} Resultado: known_accepted_not_new.
- **NEG-OVERLAY-DRIFT** (IMP-C1): ["missing_raw_candidate", "ambiguous_raw_candidate", "different_source_pin"] Resultado: all_rejected_by_generator.

OPS008/TEMP-C4 queda referenciado al agente de transacciones. OPS009 es el desajuste ya aceptado entre `embarquesController.php:L20` (un argumento) y `EmbarqueClass.php:L129` (dos obligatorios); no se vuelve a contar. SEC015, OPS001–007, IMP-AST001 e IMPT008–010 son conocidos, sin reapertura dentro de este cierre.

## Límites

- Cierre acotado a contratos HTTP IMP-C1, estado de viaje IMP-C2, inventario P VAR001 y deduplicación de OPS008/OPS009/SEC015; no es censo exhaustivo de contratos.
- No browser ni revisión de navegación; no aplicación, red, BD, submódulos o servicios ejecutados. La tabla de decisión no vuelve a ejecutar vm/probes.
- Las reglas de comparación PHP de la tabla se acotan al PHP8.4.25 ya observado; no validan PHP5.4, tipos devueltos por un driver o transiciones de negocio.
- Las combinaciones de flags son contraejemplos sintéticos derivados de predicados; no se afirma que la API real produzca esos valores.
- El SQL local conserva autoridad no verificada. El censo SQLglot, SEC015 y los riesgos de transacciones se deduplican, no se reabren aquí.
- El proceso principal genera ledger y fingerprints y decide el streak. No se declara convergencia global ni cierre de todos los riesgos de producción.

Registro de integración: [contract-integration.json](contract-integration.json). Tablas y evidencia estructurada: [closure-contracts.json](closure-contracts.json).

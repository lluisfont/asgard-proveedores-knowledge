# Obligaciones de reparación y contraejemplos de éxito

**PASADA 8 POSITIVA CON DOS DELTAS, aceptada por el usuario. Se revisaron 15 contratos (9 OPS + 6 mejoras) y se integraron RPR-IMP-001/002 como dos mejoras TO-BE adicionales. No se añaden hallazgos OPS ni se declara convergencia global.**

Esta revisión empieza después de aceptar CLR-IMP-001..003 como pasada 6 positiva. La nota IMP-SCOPE001 del principal mantiene vigente el alcance: M es el commit auditado y P es una comparación histórica, no el último Perú observado. No se revisa el nuevo head ni se cambian refs.

Fuente M: `a8ce2c23dead8552d2c4699e4a9b9134f7a18707`. P histórica: `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62`. Observación de actualidad: [remote-refs-observation.json](../../../source-audits/master/2026-11-18/iterative/remote-refs-observation.json).

## Técnica nueva

Se contrasta cada reparación propuesta con una obligación de postcondición y un caso de entrada o sentencia exitosa. Se distingue el arreglo débil, que puede rechazar o deformar ese éxito, de una condición candidata que conserva el caso. No se repiten probes de fallos ni se usa el hash como evidencia funcional.

Los modelos representan contratos TO-BE hipotéticos. No implementan cambios de aplicación y no aprueban políticas de idempotencia, tipos, moneda o fechas. El código Python reproducible y los 15 checks `status=completed` figuran en [closure-repair-obligations.json](closure-repair-obligations.json). Solo se leen fuentes fijadas por Git como anclaje; no se ejecuta PHP ni SQL.

```powershell
python -X utf8 -B -c "import json; from pathlib import Path; d=json.loads(Path('knowledge/reviews/iterative-20261118/closure-repair-obligations.json').read_text(encoding='utf-8')); exec(compile(d['reproduction_code'], '<repair-obligations-review>', 'exec'))"
```

## Obligaciones contrastadas

| ID | Contraejemplo de éxito frente a un arreglo débil | Decisión |
|---|---|---|
| OPS-001 | Capturar el último ID después de otro trabajo exitoso puede obtener102, no el ID propio101. | Mantener captura inmediata en la misma conexión; obligación conocida reforzada. |
| OPS-002 | Cambiar sobrescritura por AND con semilla false rechaza una lista no vacía con todos sus pasos exitosos. | Definir identidad de reducción y política de vacío; detalle del arreglo ya propuesto. |
| OPS-003 | Pasar un quinto argumento vacío evita aridad pero puede perder la descripción requerida. | Validar y transportar la descripción; no basta con hacer invocable la firma. |
| OPS-004 | Marcar lote completo después de un grupo exitoso incluye grupos no confirmados. | Vincular marcado a grupos confirmados y al commit; obligación conocida. |
| OPS-005 | Un mapa por tipo de evento conserva una sola de dos ocurrencias válidas con IDs registrados100/101. | Conservar instancias si se permiten repeticiones; política ya requerida. |
| OPS-006 | Pertenencia estricta al entero26 deja de reconocer el ID decimal string'26'. | Nueva propuesta RPR-IMP-002. |
| OPS-007 | La igualdad binaria exacta de0.1+0.2 frente a0.3 rechaza una suma monetaria coherente. | Precisión/escala acordada ya exigida; no se inventa otra mejora. |
| OPS-008 | Comprobar el actual retornoNULL rechaza también todas las consultas exitosas del hijo. | Cubierto por CLR-IMP-003 aceptada, sin recuento nuevo. |
| OPS-009 | Añadir un defaultNULL satisface aridad pero no selecciona el alcance3 solicitado. | Pasar alcance validado, ya propuesto; AJAX completo se conserva. |
| IMP-T008 | AND de booleans sin distinguir ausencia opcional rechaza una ruta no solicitada. | El contrato debe separar requerido, opcional y SKIPPED; ya documentado. |
| IMP-T009 | Cero cambios en una fila existente ya satisfecha puede ser un no-op permitido. | Nueva propuesta RPR-IMP-001. |
| IMP-T010 | Regex de formato acepta31/02; sustituir vacío permitido por1900 cambia significado. | Calendario, formato y ausencia separados, ya propuesto. |
| CLR-IMP-001 | DELETE exitoso con cero filas y aridad posterior no prueba pérdida de carga. | Precisión aceptada reforzada. |
| CLR-IMP-002 | [26,26] tiene primera coincidencia0 aunque exista otra posterior. | Presencia por resultado de búsqueda, no truthiness del índice; precisión aceptada. |
| CLR-IMP-003 | El hijo sin return produceNULL aun cuando los statements tuvieron éxito. | Definir resultado antes de comprobarlo; precisión aceptada. |

Los controles negativos de cada check están en el JSON: filas únicas, ausencia opcional válida, enteros/strings válidos y sufijos inválidos, cero monetario legítimo, no-op prohibido con resultado distinto y listado AJAX con argumentos completos. No se considera validada una reparación universal porque satisfaga un testigo.

## Dos mejoras TO-BE adicionales notificadas

### RPR-IMP-001 · El retorno de actualización debe separar filas coincidentes, cambios y una operación sin cambios permitida

**Relacionados:** IMP-T009, CLR-IMP-001. **P2. Mejora aceptada e integrada en pasada 8; no nuevo OPS.**

**Condición:** La política TO-BE admite repetir una operación ya satisfecha o guardar valores idénticos. La configuración del cliente SQL puede informar cambios o coincidencias; esa configuración no se ha comprobado.

**Contraejemplo:** El modelo de una sentencia exitosa con fila existente y valores ya iguales produce cero cambios. Un arreglo que traduce affected_rows==0 a inexistencia o error rechaza ese éxito permitido. La condición no debe confundirse con una fila que no coincide o no está autorizada.

**Obligación propuesta — TO-BE:** Definir resultados distintos para CHANGED, NOOP_CONFIRMED si la política lo permite, NOT_FOUND y rechazo de transición. Fijar qué cuenta el cliente SQL; combinar predicado autorizado y estado observado para distinguirlos. Si la política no permite no-op, devolver ese resultado específico sin inferir inexistencia.

**Novedad de esta pasada:** La mejora aceptada CLR-IMP-001 limitaba la afirmación de pérdida tras DELETE; esta pasada contrasta una reparación basada en conteos con una actualización/no-op exitosa y exige un contrato de retorno más preciso.

**Deduplicación:** Mejora de reparación/contrato dentro de IDs existentes; no otro defecto OPS ni una política de idempotencia declarada AS-IS.

**Evidencia:** `M:index_archivos/tracking/HerramientasClass.php:L29-L47`; `M:index_archivos/tracking/TrackingNewClass.php:L1509-L1521`; `M:index_archivos/tracking/ListaViajesClass.php:L30-L36`.

### RPR-IMP-002 · La reparación de pertenencia debe conservar IDs numéricos válidos recibidos como string

**Relacionados:** OPS-006, CLR-IMP-002. **P2. Mejora aceptada e integrada en pasada 8; no nuevo OPS.**

**Condición:** La representación válida del ID de evento es int26 o string decimal'26'. El tipo concreto devuelto en el despliegue no se ha verificado; la fuente no normaliza antes de la búsqueda.

**Contraejemplo:** Cambiar el if de array_search por pertenencia estricta al entero26 no reconoce '26', aunque representa el mismo ID y la búsqueda previa no estricta lo reconoce. Es una regresión de un caso exitoso de lectura, independiente de la posición o repetición.

**Obligación propuesta — TO-BE:** Comparar el resultado de búsqueda con false estrictamente sin cambiar la igualdad de valores, o validar y normalizar de forma explícita el tipo de ID antes de pertenencia estricta. Conservar int26 y '26'; no convertir indiscriminadamente entradas no numéricas como'26x'.

**Novedad de esta pasada:** Los probes y la pasada anterior usaban IDs enteros. El contraejemplo exitoso de representación string prueba una obligación de reparación no cubierta por corregir solo índice0 o repeticiones.

**Deduplicación:** Precisión de TO-BE de OPS-006/CLR-IMP-002, no nuevo hallazgo OPS ni confirmación de tipos o eventos reales.

**Evidencia:** `M:index_archivos/tracking/ListaViajesClass.php:L166-L174`; `M:index_archivos/tracking/ListaViajesClass.php:L387-L409`.

## Límites y estado de la integración

- Review bounded to9OPS+6accepted improvements; two further TO-BE proposals, no new OPS IDs or global convergence.
- Candidate repairs are logical models, not implemented PHP/SQL changes or approved requirements.
- No runtime, query fault injection, MySQL, DB/network, sessions or browser/navigation outputs executed or reviewed.
- No universally valid no-op policy, affected-row client flags, actual event-ID representation, timezone or monetary scale inferred.
- Counterexamples with successful inputs show insufficiency of a weak repair; satisfying the listed witness is not a proof for all inputs.
- Original PHP8 signature probes remain prior evidence; PHP5.4 not executed.
- PinP95fe9a4is historical, not latestPeru; observed2a179e2is not audited. No refs changed.
- IMP-SCOPE001 belongs to principal; not duplicated as an operational improvement. Ledger not compiled here.

El registro mantiene 9 OPS y 8 mejoras aceptadas, incluidas CLR-IMP-001..003 y RPR-IMP-001/002. Se conserva este cierre como positivo con dos deltas, sin convertirlas en nuevos OPS. La pasada 6 sigue marcada con delta; la nota de actualidad del principal no amplía la auditoría a otro Perú.

No se compiló ledger, no se editaron otros archivos del main, no hubo commits/push ni acceso a BD/red o persistencia de sesión. Tampoco se revisaron salidas de navegador/navegación.

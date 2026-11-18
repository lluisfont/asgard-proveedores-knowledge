# Revisión acotada de transacciones posterior a OPS-009

**PASADA CON DELTA. Pasada 6 positiva aceptada por el usuario: CLR-IMP-001..003 integradas como tres mejoras materiales adicionales. Revisados OPS-001..009; sin nueva entrada OPS ni convergencia global.**

Fuente M: `a8ce2c23dead8552d2c4699e4a9b9134f7a18707`; comparación de referencia P: `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62`. Los nueve IDs y sus evidencias están en [el registro operativo](../../general/operational-findings.json).

Esta es una pasada nueva de contratos de retorno y selección. No se repiten los 34 probes de inyección de fallos ni se presenta el censo token-only del principal como trabajo de esta pasada. El censo y el probe de firma sustentan la integración previa de OPS-009.

## Técnica y ejecución

- Dependencias estáticas de asignación y postcondiciones de retorno, sin ejecutar métodos PHP.
- Predicados relacionales con filas sintéticas y operaciones asumidas exitosas; se compara identidad o conjunto seleccionado con el contrato propuesto.
- Propiedades bajo permutaciones y conservación de pendientes en modelos de arrays; tuplas monetarias con Decimal exacto.
- Firma/argumentos y orden DELETE→llamada; control específico del AJAX con argumentos completos.

Se leyeron nueve archivos de código fijados por Git y se contrastaron contra el checkout. El modelo Python está incrustado en [closure-transactions.json](closure-transactions.json), campo `reproduction_code`, junto con hashes, resultados y límites. No se ejecutó PHP, SQL, el controlador, servicios, navegador o persistencia de sesión.

```powershell
python -X utf8 -B -c "import json; from pathlib import Path; d=json.loads(Path('knowledge/reviews/iterative-20261118/closure-transactions.json').read_text(encoding='utf-8')); exec(compile(d['reproduction_code'], '<bounded-transaction-review>', 'exec'))"
```

## Comprobaciones y controles negativos

| ID | Revisión nueva y dominio | Resultado | Control que limita la afirmación |
|---|---|---|---|
| OPS-001 | 16 fixtures; identidad por predicado embarque/autor | 2 eligen el ID de otra operación; 1 pertenece a la misma categoría. Añadir categoría no basta. | Otro embarque/autor queda excluido; fila única selecciona ID propio. |
| OPS-002 | Dos asignaciones de statusSave; dependencia de retorno | Retorna el subItems de la última localización cuyo INSERT tuvo éxito, no un AND de todos los pasos. | Vacío retorna false; todo éxito puede retornar true; excepciones fuera de esta fórmula. |
| OPS-003 | Firma 5 / llamada 4 y dominancia del DELETE | La llamada inválida viene después del DELETE aceptado; un efecto de cero filas no acredita pérdida. | El alta pasa descripción; DELETE false no alcanza la llamada; cero filas limita el impacto, no corrige aridad. |
| OPS-004 | 8 filas de lote/cuenta/grupo; snapshot con grupo1 confirmado | El UPDATE alcanza grupos1 y2 aunque solo1 esté confirmado. | Otros lotes/cuentas excluidos; lote de un grupo coincide; éxito final de todos puede dejar estado final correcto. |
| OPS-005 | 726 configuraciones de catálogo/historial | 450 violan conservación de pendientes del modelo. | 24/24 prefijos únicos exactos cumplen; catálogo vacío conserva historial. |
| OPS-006 | 90 historiales con26, longitudes1..4 | 40 no activan guardia;25 contienen repeticiones posteriores. | Primera coincidencia después de0 activa la guardia; catálogo vacío retorna antes. |
| OPS-007 | 27 tuplas exactas, conceptos de0/0,10/1,25 | 22 sumas no quedan vinculadas al total de cabecera por la fuente. | 5 tuplas coherentes; cero con detalles cero no constituye error por sí mismo. |
| OPS-008 | Totalidad de retorno; dos pedidos del mismo embarque | Helper retorna NULL también con éxito; LIMIT1 admite ambas identidades si no existen constraints externos. | Un único pedido activo puede funcionar; input vacío no llama al helper; ordenar no demuestra actividad/unicidad. |
| OPS-009 | Binding de parámetros en tres llamadas | mostrartabla pasa1 y requiere2; el campo t de la petición no añade el argumento formal ausente. | AJAX pasa5/2 y satisface la firma. Sin evaluación de reachability JS ni cuerpo SQL. |

Los números son cobertura del dominio finito y contraejemplos del modelo, no tasas de fallos de producción ni una ejecución de MySQL. La fórmula de OPS-002 se deriva estáticamente: no se vuelve a programar una secuencia de retornos false.

## Precisiones materiales notificadas

### CLR-IMP-001 · El éxito del DELETE no demuestra filas borradas ni pérdida de carga

**IDs relacionados:** OPS-003.

El retorno comprobado es éxito de sentencia, sin consulta de filas afectadas. El contraejemplo con DELETE aceptado y0filas alcanza la llamada4/5 igualmente, pero no borra carga previa. La condición de pérdida requiere filas coincidentes y efecto confirmado.

**Aporte de esta técnica:** La pasada anterior comparó DELETEtrue/false; esta pasada distingue efecto0/positivo con sentencia exitosa, sin inyectar fallos.

**Cambio de documentación/TO-BE:** Añadir precondición explícita de carga existente/coincidente y separar error de aridad de pérdida persistente. No interpretar la excepción como comprobación de borrado.

**Deduplicación:** Precisión del impacto de OPS-003; no otro hallazgo de aridad ni nueva entrada OPS.

**Evidencia:** `M:index_archivos/tracking/TrackingNewClass.php:L1581-L1589`; `M:index_archivos/tracking/TrackingNewClass.php:L1517-L1521`.

### CLR-IMP-002 · La primera coincidencia26 en índice0 oculta también repeticiones posteriores

**IDs relacionados:** OPS-006.

Sobre90historiales con26 de longitud1..4,40no activan la guardia;25de ellos tienen otro26posterior. array_search devuelve la primera coincidencia, no basta con que exista26fuera del índice0.

**Aporte de esta técnica:** La prueba diferencial anterior usó[26] frente a[3,26]. El nuevo dominio enumera repeticiones y descubre la clase[26,26] y sus extensiones.

**Cambio de documentación/TO-BE:** Ampliar caracterización para la primera coincidencia y repeticiones; evitar una especificación de presencia basada en una posición no inicial aislada.

**Deduplicación:** Misma causa de OPS-006. Distinta de la mezcla de pendientes OPS-005; no se infiere significado de negocio de26.

**Evidencia:** `M:index_archivos/tracking/ListaViajesClass.php:L166-L174`; `P:index_archivos/tracking/ListaViajesClass.php:L166-L174`.

### CLR-IMP-003 · Comprobar un retorno booleano inexistente también rechazaría adiciones exitosas

**IDs relacionados:** OPS-008.

crearPedidosDetalle llega al final sin return aun con todas las sentencias exitosas: devuelveNULL implícito. Una corrección ingenua if(!crearPedidosDetalle(...)) detectaría también los éxitos como error. Seleccionar un pedido activo/único es una obligación separada; ordenar LIMIT1por sí solo no la cumple.

**Aporte de esta técnica:** Se sustituye la agenda previa de fallos por prueba de totalidad del retorno y selección relacional con operaciones exitosas. Hace explícito un criterio de corrección que no estaba en la caracterización de fallos.

**Cambio de documentación/TO-BE:** Definir antes un resultado explícito de detalle/conciliación y consumirlo en padre/controlador; no añadir solo un if sobre el actual retornoNULL.

**Deduplicación:** Profundiza el TO-BE de OPS-008; ausencia de resultado y selección ya pertenecen a esa entrada. No se añade OPS-010.

**Evidencia:** `M:index_archivos/embarques/CotizacionClass.php:L1195-L1206`; `M:index_archivos/embarques/CotizacionClass.php:L1342-L1367`; `M:index_archivos/embarques/editarController.php:L56-L70`; `P:index_archivos/embarques/CotizacionClass.php:L1397-L1422`.

## Deduplicación y decisión acotada

- **OPS-001 / OPS-007**: Identidad elegida por SELECT frente a suma cabecera/detalle; no son SQLi ni el falso éxito genérico RN-40.
- **OPS-002 / OPS-003**: Retorno del acumulador frente a firma inválida posterior a DELETE; RN-21/23 genéricos no los sustituyen.
- **OPS-004**: Conjunto de filas marcadas antes de completar todos los grupos; distinto del agregador RN-33 que ignora códigos.
- **OPS-005 / OPS-006**: Conservación de pendientes frente a guardia por primera coincidencia; causas y controles independientes.
- **OPS-008**: Edición de pedido existente separada de alta RN-14/15; no se infiere autorización real ni se separa cada retorno ignorado en un hallazgo.
- **OPS-009 / OPS-003 / RN-34**: Tres sitios de aridad: uno nuevo aceptado por principal, otroOPSexistente y otrobaseline. No tres nuevos hallazgos del censo.

No se ha añadido un mecanismo independiente fuera de OPS-001..009 en este alcance. Se incorporan las tres precisiones anteriores a los IDs existentes. Esta decisión procede de las obligaciones y contraejemplos nuevos descritos; no de repetir checks para imponer un cero. No certifica ausencia de otros defectos.

## Límites

- Acotado a los nueveIDsaceptados; no cierre global ni aprobación canónica, dominio/release o ausencia global de defectos.
- Los modelos usan dominios explícitos; no ejecutan código PHP, motorSQL, concurrencia, BD, red ni sesión.
- La derivación def-use describe rutas con retornos ordinarios; excepciones, triggers, constraints y autocommit reales desconocidos.
- PHP8/PHP5.4: el comportamiento8es evidencia previa del principal/sidecar; no se repitió runtime ni se probó5.4.
- Modelo LIMIT1describe resultados permitidos por el predicado, no el orden realmente devuelto ni datos existentes.
- Modelos numéricos exactos no deciden política de signos, FX, escala o redondeo de negocio.
- API/IDsde eventos sintéticos;26no se etiqueta como cierre de negocio.
- Salidas de navegador/navegación bloqueadas: no revisadas; candidatoJSdeOPS009sin evaluación de reachability.

Sin cambios de código, otros documentos, scripts, manifiestos o registro SEC; sin commits o push. La secuencia queda registrada en [transaction-integration.json](transaction-integration.json). El fingerprint final del registro se guarda allí y en el JSON de esta revisión.

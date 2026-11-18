# Delta de transacciones e invariantes — 18-11-2026

**Revisión lateral no canónica; requiere consolidación independiente. No se declara convergencia.**

Fuente M: `a8ce2c23dead8552d2c4699e4a9b9134f7a18707`, checkout `C:/repos/proveedores-github-review-20261118`. Comparación selectiva P: `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` (`origin/master_peru`, sin fetch). Knowledge de partida: `3822900b6d54d99ccf854bec43005a208e2a9694`.

Resultado: **7 hallazgos nuevos** (dos P1 y cinco P2), **3 precisiones documentales** y **4 duplicados/hipótesis rechazadas**. Son defectos de fuente con impacto condicionado al entorno de cada entrada, sin validación en producción.

Se leyeron AGENTS y Brownfield/ASGARD, los 14 hallazgos SEC, workflows, business-rules y manual. Los dominios se revisaron por separado. Los IDs TEMP-T* identifican propuestas para revisión; no equivalen a IDs canónicos de seguridad ni a requisitos de negocio validados.

## Técnicas realmente intentadas

- Lectura UI/endpoint/helper/SQL/consumidor y comparación selectiva con git show de origin/master_peru.
- Inyección programada de false por etapa en métodos extraídos sin cambiar sus cuerpos.
- Intercalado sintético del maestro102 al SELECT de máximo ID, tras INSERT propio101; no concurrencia real.
- Permutación del lugar del fallo de localización/subítems para revisar el acumulador de éxito.
- Prueba diferencial de aridad tras DELETE=true/false; captura de Throwable solo en el harness externo.
- Extracción de crearViaje para inspeccionar alcance de UPDATE de lote antes de ejecutar otro grupo.
- Contraejemplos de eventos fuera de orden/repetidos, índice0 frente a1 y catálogo vacío.
- Total maestro999 frente a detalle10+20; formatos/calendario; revisión del SQL de estado y origen de timestamps.

Prueba reproducible: [script](../../../scripts/audit/transaction_probes.py) y [resultado JSON](../../../source-audits/master/2026-11-18/iterative/transaction-probes.json). **34/34 casos reproducidos y 15 controles negativos**, PHP `8.4.25`. «Reproducido» significa comportamiento observado, incluso cuando viola un invariante; no es aprobación funcional.

```powershell
python -B scripts/audit/transaction_probes.py --source C:/repos/proveedores-github-review-20261118 --output source-audits/master/2026-11-18/iterative/transaction-probes.json
```

Los cuerpos se extraen por tokens en memoria con huellas SHA-256 normalizadas LF y se envuelven como métodos públicos estáticos. Los colaboradores no seleccionados son dobles explícitos. PHP usa `-n`, sin mysqli/pdo_mysql/curl y con operaciones de red/archivo/sesión deshabilitadas. No se ejecutan includes, bootstrap, handlers, SQL, uploads o notificaciones reales. La sesión es un array sintético en memoria.

No se emuló MySQL: las agendas de resultados y el maestro concurrente102 prueban control de flujo/SQL generado. No se prueban constraints, cascadas, autocommit, triggers, conexiones efectivas o concurrencia real. Los false inyectados no equivalen a excepciones mysqli; PHP5.4 declarado en Docker no se ejecutó.

## Controles negativos y rechazos

| Grupo | Resultado observado |
|---|---|
| Costos | `cost-ok`: ruta coherente; `cost-empty`: warning sin queries; `cost-master-fail`: error, no success indiscriminado. |
| Localizaciones | `location-all-ok`: true; `location-last-items-fail`, `location-all-locations-fail` y `location-empty`: false. Acotan fallos que sí se detectan. |
| Viaje | `save-order-fail`:100 y DELETE cabecera; `edit-load-delete-fail`:100 sin ArgumentCountError. |
| Importación | `bulk-header-fails`:100 antes del UPDATE de procesamiento. |
| Eventos | `events-aligned`: prefijo correcto; `events-terminal-second`: encuentra26 fuera de índice0; `events-empty-remote`: conserva detalle. La etiqueta terminal del probe no confirma significado de26. |
| Fecha/estado | Fecha DD/MM correcta se transforma; SQL de interrupción false devuelve error. |

El caso `state-zero-affected` solo agenda query=true con condición sintética de cero filas; no ejecuta una transición SQL. Se rechazó inferir hijos huérfanos, duplicados EDP o estados de rutinas sin DDL/cuerpo SQL. Fechas empatadas carecen de desempate explícito, pero no se observó orden real de BD. No se cuentan nuevos SQLi, CSRF, bypass de autorización ni políticas sobre importes negativos.

## Deltas y deduplicación

| ID | Clase | Prioridad | Título |
|---|---|---|---|
| TEMP-T001 | new_finding | P1 | El guardado de costos puede insertar detalles o borrar el maestro de otra petición |
| TEMP-T002 | new_finding | P2 | El resultado de localizaciones oculta fallos según su posición |
| TEMP-T003 | new_finding | P1 | La edición borra la carga y llama a su reemplazo con un argumento ausente |
| TEMP-T004 | new_finding | P2 | Crear un viaje marca como procesados todos los grupos del lote |
| TEMP-T005 | new_finding | P2 | La mezcla por posición puede duplicar u omitir eventos pendientes |
| TEMP-T006 | new_finding | P2 | La excepción del evento 26 falla si aparece en la primera posición |
| TEMP-T007 | new_finding | P2 | El servidor acepta un total de costos distinto de la suma de conceptos |
| TEMP-T008 | improvement | P2 | Precisar qué escrituras del viaje se comprueban y cuáles pueden fallar sin error |
| TEMP-T009 | improvement | P2 | Distinguir fecha de modificación, interrupción y transición válida de estado |
| TEMP-T010 | improvement | P2 | La conversión de fechas no valida el calendario ni acepta ISO |
| TEMP-T011 | duplicate_or_rejected | P2 | La sustitución de costos carece de reversión y puede anunciar éxito tras fallar el detalle |
| TEMP-T012 | duplicate_or_rejected | P2 | La limpieza del viaje solo borra cabecera y la edición conserva pasos previos |
| TEMP-T013 | duplicate_or_rejected | P2 | El agregador de importación anuncia éxito sin revisar cada creación |
| TEMP-T014 | duplicate_or_rejected | P2 | No se demuestra la atomicidad ni el estado resultante de rutinas SQL ausentes |

### TEMP-T001 · El guardado de costos puede insertar detalles o borrar el maestro de otra petición

**new_finding · P1 · Costos: selección de maestro posterior al INSERT**

**AS-IS / impacto condicionado:** A selecciona el máximo id por embarque/created_by sin usar su ID de inserción ni filtrar categoría. Puede insertar sus conceptos en B y, si falla el detalle, emitir DELETE del maestro B. A puede quedar sin detalle. No exige SQLi ni otro tenant.

**Condiciones:** Dos peticiones del mismo proveedor crean costos del mismo embarque; pueden usar categorías distintas. B confirma su maestro entre el INSERT y el SELECT de A; ausencia de aislamiento/bloqueo externo que lo impida. El borrado requiere que el INSERT de detalle devuelva false sin lanzar excepción.

**Evidencia:** `M:index_archivos/embarques/CostosClass.php:L576-L592`; `M:index_archivos/embarques/CostosClass.php:L382-L390`; `M:index_archivos/embarques/CostosClass.php:L399-L415`; `P:index_archivos/embarques/CostosClass.php:L578-L594`.

**Validación:** El doble asigna INSERT propio101 y agenda el maestro concurrente102 al SELECT posterior. Se emitió detalle costos_id102 y, con detalle=false, DELETE id102, conservando success. El control secuencial usa101. Intercalado programado, sin hilos ni SQL real. Casos: `cost-ok`, `cost-race`, `cost-race-detail-fail`.

**Deduplicación:** RN-40/F-08/U09 ya advierten falta de atomicidad y falso éxito. No describen seleccionar ni borrar el maestro de otra petición. SEC-006 trata interpolación SQL, no esta carrera con valores normales.

**Destino sugerido, sin editar:** `knowledge/general/business-rules.md#RN-40`, `knowledge/general/workflows.md#F-08`.

**Perú:** P conserva SELECT último id y DELETE de ese id en578-594; la conversión mysql/mysqli no lo corrige.

**TO-BE, no aplicado:** Capturar inmediatamente el ID propio en la conexión del INSERT; sustituir costos y detalles en una transacción y notificar después de confirmar.

### TEMP-T002 · El resultado de localizaciones oculta fallos según su posición

**new_finding · P2 · Tracking: alta y edición de orígenes/destinos**

**AS-IS / impacto condicionado:** statusSave solo se actualiza tras insertar una localización. Un fallo temprano de subítems se sobreescribe con un éxito posterior; un fallo tardío del INSERT de localización conserva el true anterior. saveLocation retorna true y su llamador puede responder éxito sin todos los destinos/cargas.

**Condiciones:** Dos o más localizaciones. Una consulta devuelve false y el flujo continúa; si mysqli lanza una excepción el efecto puede diferir. Otra localización logra insertar sus subítems; los demás pasos pueden completarse.

**Evidencia:** `M:index_archivos/tracking/TrackingNewClass.php:L1192-L1239`; `M:index_archivos/tracking/TrackingNewClass.php:L1315-L1333`; `M:index_archivos/tracking/TrackingNewClass.php:L204-L214`; `M:index_archivos/tracking/TrackingNewClass.php:L1592-L1600`; `P:index_archivos/tracking/TrackingNewClass.php:L1227-L1239`.

**Validación:** Tres agendas mixtas retornan true pese a una consulta false. Último subítem fallido, todas las localizaciones fallidas y array vacío retornan false. Se extrajeron saveLocation/subItems/castDate sin cambiar cuerpos; queries/resultados están en el artifact. Casos: `location-first-location-fails`, `location-last-location-fails`, `location-first-items-fail`, `location-last-items-fail`, `location-all-locations-fail`, `location-all-ok`, `location-empty`.

**Deduplicación:** RN-21/F-04 mencionan fallos comprobados de pasos principales y RN-23 edición parcial. Falta el mecanismo que convierte fallos principales en éxito y su dependencia del orden; no se vuelve a contar el catch incompleto.

**Destino sugerido, sin editar:** `knowledge/general/business-rules.md#RN-21`, `knowledge/general/business-rules.md#RN-23`, `knowledge/general/workflows.md#F-04`.

**Perú:** La acumulación statusSave se conserva en P:1227-1239.

**TO-BE, no aplicado:** Abortar ante cada fallo y evitar que un resultado posterior sobrescriba el error; definir la transacción de la unidad lógica.

### TEMP-T003 · La edición borra la carga y llama a su reemplazo con un argumento ausente

**new_finding · P1 · TrackingNewClass::edit → editLoad → saveLoad**

**AS-IS / impacto condicionado:** saveLoad requiere descripcionMercancia como quinto argumento, pero editLoad pasa cuatro después de borrar. En PHP probado se lanza ArgumentCountError antes del INSERT; catch(Exception) de edit no lo captura. No retorna su code100 ni repone la carga. La respuesta HTTP final depende del servidor; no se necesita un fallo SQL.

**Condiciones:** La edición alcanza editLoad y DELETE devuelve true; pasos previos no abortan. PHP local8.4.25 reproduce ArgumentCountError; no se ejecutó PHP5.4 declarado en Docker. Pérdida persistente condicionada a DELETE confirmado/autocommit y ausencia de reversión externa.

**Evidencia:** `M:index_archivos/tracking/TrackingNewClass.php:L257-L285`; `M:index_archivos/tracking/TrackingNewClass.php:L1581-L1589`; `M:index_archivos/tracking/TrackingNewClass.php:L1166-L1189`; `M:index_archivos/tracking/ajaxAsignacion/editar_asignacion.php:L68-L76`; `M:Dockerfile:L1-L6`; `P:index_archivos/tracking/TrackingNewClass.php:L1581-L1589`; `P:index_archivos/tracking/TrackingNewClass.php:L1166-L1168`.

**Validación:** edit extraído con DELETE=true alcanzó ArgumentCountError tras una sola consulta DELETE, sin INSERT ni respuesta del método. DELETE=false evita la llamada inválida y devuelve100. Pasos previos simulados con éxito; sin borrado real ni ejecución de PHP5.4. Casos: `edit-load`, `edit-load-delete-fail`.

**Deduplicación:** RN-23/F-04 solo advierten actualizaciones parciales. RN-34 describe otra aridad distinta (crearViaje desde embarquesController), que no cubre este DELETE. Nueva causa concreta, con runtime condicionado.

**Destino sugerido, sin editar:** `knowledge/general/business-rules.md#RN-23`, `knowledge/general/workflows.md#F-04`, `knowledge/general/user-manual.md#U05`.

**Perú:** P conserva firma de cinco argumentos y llamada de cuatro en1166 y1581-1589.

**TO-BE, no aplicado:** Pasar la descripción requerida y validar el objeto antes de borrar; reemplazar carga dentro de transacción y revisar Throwable al modernizar PHP.

### TEMP-T004 · Crear un viaje marca como procesados todos los grupos del lote

**new_finding · P2 · Carga masiva: estado por grupo**

**AS-IS / impacto condicionado:** El UPDATE filtra lote/cuenta, no numero_viaje: el primer grupo intenta marcar estado1 también en filas sin viaje creado. Tras fallo posterior, la señal de procesado queda adelantada; la limpieza inicial de otra carga solo elimina estado nulo/0 y excluye esas filas. No se afirma que un nuevo fichero no pueda reinsertarlas ni que no exista reintento manual.

**Condiciones:** Lote con dos o más numero_viaje de una cuenta. Primer crearViaje alcanza UPDATE y se confirma; otro grupo aún no se intenta o falla después. Ausencia de corrección externa de ese marcado.

**Evidencia:** `M:index_archivos/tracking/controllers/CargaMasiva.php:L361-L367`; `M:index_archivos/tracking/controllers/CargaMasiva.php:L574-L588`; `M:index_archivos/tracking/ajax/uploadExcelCargaMasiva.php:L208-L226`; `M:index_archivos/tracking/controllers/CargaMasiva.php:L23-L29`; `P:index_archivos/tracking/controllers/CargaMasiva.php:L590-L597`.

**Validación:** crearViaje extraído para grupo1 emite UPDATE lote88/cuenta22 sin numero_viaje antes de devolver200. Fixture declara grupos1/2; grupo2 no se ejecuta. Fallo temprano de cabecera devuelve100 sin UPDATE. No se emularon filas persistentes ni lote completo. Casos: `bulk-first-group`, `bulk-header-fails`.

**Deduplicación:** RN-33/F-05 ya documentan agregador que ignora códigos. Esta transición sigue siendo incorrecta aunque el agregador detecte el fallo: grupos futuros ya fueron marcados. RN-31 no describe ese adelanto.

**Destino sugerido, sin editar:** `knowledge/general/business-rules.md#RN-31`, `knowledge/general/business-rules.md#RN-33`, `knowledge/general/workflows.md#F-05`.

**Perú:** P aplica el mismo UPDATE de lote completo en590-591.

**TO-BE, no aplicado:** Marcar solo el grupo confirmado y asociarle el ID creado; separar progreso por viaje/lote y definir reintento idempotente.

### TEMP-T005 · La mezcla por posición puede duplicar u omitir eventos pendientes

**new_finding · P2 · Detalle: orden temporal frente a catálogo remoto**

**AS-IS / impacto condicionado:** Se sobrescriben posiciones del catálogo con filas ordenadas por fecharegistro sin reconciliar IDs. Remotos[3,5,7] y detalle[5] producen[5,5,7]: desaparece pendiente3 y se duplica5. Detalle[3,3] produce[3,3,7], omitiendo5. El defecto demostrado es de representación, no modificación del historial SQL.

**Condiciones:** API devuelve lista no vacía. Detalle local no es un prefijo único del catálogo: evento adelantado, repetido o registrado fuera de orden. Las filas alcanzan el ensamblador; no se presuponen restricciones de unicidad desconocidas.

**Evidencia:** `M:index_archivos/tracking/ListaViajesClass.php:L157-L190`; `M:index_archivos/tracking/ListaViajesClass.php:L387-L409`; `M:index_archivos/tracking/viajedetalle.php:L89-L90`; `P:index_archivos/tracking/ListaViajesClass.php:L157-L190`.

**Validación:** eventosViaje extraído con dobles locales de eventos/getEventName reproduce ambos contraejemplos. Prefijo[3] produce[3,5,7]; API vacía conserva[5]. ORDER BY fecharegistro no tiene desempate explícito, pero no se observó orden real de BD. Casos: `events-aligned`, `events-out-of-order`, `events-duplicate-detail`, `events-empty-remote`.

**Deduplicación:** RN-29/F-04 recogen consulta remota y conservación si vacía, no el requisito implícito de prefijo. No duplica advertencias de efectos parciales ni subidas de SEC-010.

**Destino sugerido, sin editar:** `knowledge/general/business-rules.md#RN-29`, `knowledge/general/workflows.md#F-04`.

**Perú:** P conserva el ensamblado posicional en157-190.

**TO-BE, no aplicado:** Reconciliar por identidad y definir representación de repeticiones/omitidos y orden temporal, sin reemplazar catálogo por índices de historial.

### TEMP-T006 · La excepción del evento 26 falla si aparece en la primera posición

**new_finding · P2 · Detalle: presencia de evento mediante array_search**

**AS-IS / impacto condicionado:** array_search devuelve0 y el if lo interpreta como false. El mismo26 detiene el ensamblado en índice1, pero en índice0 se añaden hitos del catálogo. Remotos[3,5,7] con detalle[26] producen[26,5,7]; detalle[3,26] se conserva. No se atribuye nombre o significado de cierre al evento26.

**Condiciones:** Catálogo remoto no vacío y detalle con id26 en índice0. Significado empresarial de26 requiere confirmación; solo se acredita la excepción de presencia implementada.

**Evidencia:** `M:index_archivos/tracking/ListaViajesClass.php:L159-L174`; `P:index_archivos/tracking/ListaViajesClass.php:L166-L174`.

**Validación:** Prueba diferencial reproduce índice0 frente a1; API vacía sale antes de la condición. La palabra terminal en el ID técnico del probe es una etiqueta del harness, no un significado de negocio confirmado. Casos: `events-terminal-first`, `events-terminal-second`, `events-empty-remote`.

**Deduplicación:** Independiente de TEMP-T005: la búsqueda booleana falla sin historial desordenado ni duplicado; arreglar el merge no necesariamente corrige esta salida temprana. RN-29 no describe la excepción26.

**Destino sugerido, sin editar:** `knowledge/general/business-rules.md#RN-29`.

**Perú:** El mismo if aparece en P:166-168.

**TO-BE, no aplicado:** Comparar array_search contra false estrictamente o usar comprobación de pertenencia; confirmar el contrato de26 antes de documentarlo como cierre.

### TEMP-T007 · El servidor acepta un total de costos distinto de la suma de conceptos

**new_finding · P2 · Costos: invariante monetario maestro/detalle**

**AS-IS / impacto condicionado:** El navegador suma importes, pero el servidor inserta totalCategory como total_costos y cada amount por separado sin recalcular/comparar. Total999 y conceptos10+20 generan esas tres cantidades y success. getCostos devuelve total almacenado y detalle, que pueden discrepar si la BD confirma. No se infiere impacto contable ni regla de signos.

**Condiciones:** Petición de costos con conceptos numéricos y totalCategory alterado u obsoleto. INSERTs aceptados y ausencia de trigger/constraint que recalcule o rechace la discrepancia.

**Evidencia:** `M:index_archivos/embarques/ajax/guardar-costos.php:L1-L8`; `M:index_archivos/embarques/CostosClass.php:L355-L390`; `M:index_archivos/embarques/CostosClass.php:L576-L588`; `M:index_archivos/embarques/CostosClass.php:L399-L414`; `M:index_archivos/embarques/componentes/costos/card-component.js:L106-L113`; `P:index_archivos/embarques/CostosClass.php:L578-L590`.

**Validación:** El doble captura999 en INSERT maestro y10/20 en detalle con success; aserciones comprueban las tres cantidades. Control coherente usa30; conceptos vacíos se rechazan sin queries. No acredita persistencia frente a constraints desconocidos. Casos: `cost-ok`, `cost-mismatch`, `cost-empty`.

**Deduplicación:** RN-40/F-08 describen controles de navegador y sustitución, no este contraejemplo monetario. SEC-006 trata manipulación de sintaxis; aquí solo hay números simples. No se cuenta como otro SQLi.

**Destino sugerido, sin editar:** `knowledge/general/business-rules.md#RN-40`, `knowledge/general/workflows.md#F-08`.

**Perú:** P también confía en totalCategory/amount (578-590 y384-392).

**TO-BE, no aplicado:** Validar cantidades/moneda y calcular total en servidor con precisión monetaria definida; persistir maestro/detalle como una unidad.

### TEMP-T008 · Precisar qué escrituras del viaje se comprueban y cuáles pueden fallar sin error

**improvement · P2 · Documentación de multiescrituras**

**AS-IS / impacto condicionado:** save ignora resultados de rutas, relevo y registro de ubicaciones; EDP tampoco propaga el resultado. Puede devolver200 con esas operaciones fallidas. saveRoutes también devuelvefalse sin aduana, que puede ser ausencia opcional válida. No toda devolución false equivale a fallo empresarial.

**Condiciones:** Pasos comprobados exitosos. Rutas/relevo/catálogo de ubicaciones retornan false sin lanzar; integraciones no abortan.

**Evidencia:** `M:index_archivos/tracking/TrackingNewClass.php:L184-L234`; `M:index_archivos/tracking/TrackingNewClass.php:L1336-L1344`; `M:index_archivos/tracking/TrackingNewClass.php:L274-L285`; `M:index_archivos/tracking/TrackingNewClass.php:L1635-L1648`.

**Validación:** save extraído devuelve200 con false en rutas/relevo/ubicaciones. Control: saveOrder=false produce100 y DELETE cabecera. No se invocaron integraciones. Casos: `save-optional-fail`, `save-order-fail`.

**Deduplicación:** Precisión de RN-21/RN-22/F-04; no se cuenta otra advertencia genérica de parcialidad ni se convierte ausencia opcional en defecto.

**Destino sugerido, sin editar:** `knowledge/general/business-rules.md#RN-21`, `knowledge/general/business-rules.md#RN-22`, `knowledge/general/workflows.md#F-04`.

**Perú:** Comparación acotada; no se atribuye regresión de país.

**TO-BE, no aplicado:** Enumerar resultados comprobados/ignorados y acordar qué datos son obligatorios antes de endurecer errores.

### TEMP-T009 · Distinguir fecha de modificación, interrupción y transición válida de estado

**improvement · P2 · Semántica de estados y timestamps**

**AS-IS / impacto condicionado:** fecha_estado es alias de updated_at, no una fecha dedicada de transición. editInfo lo actualiza aunque no cambie estado; interrupción escribe fecha_interrupcion/estado2 sin asignar updated_at. El WHERE solo exige ID, sin estado previo, borrado lógico o comprobación de filas afectadas. Los filtros de UI no acreditan una máquina de estados del servidor. No se declara transición empresarial prohibida sin política validada.

**Condiciones:** Ruta de interrupción alcanza helper con sesión/conexión válidas. Efecto persistente y actualización automática de updated_at dependen de DDL/triggers desconocidos.

**Evidencia:** `M:index_archivos/tracking/ListaViajesClass.php:L30-L36`; `M:index_archivos/tracking/TrackingNewClass.php:L1509-L1521`; `M:index_archivos/tracking/HerramientasClass.php:L29-L47`; `M:index_archivos/tracking/listaviajes.php:L238-L238`; `M:index_archivos/tracking/listaviajes.php:L279-L284`; `M:index_archivos/tracking/ajax/discontinued-trip.php:L1-L10`.

**Validación:** Helper extraído emite WHERE id701 sin predicado de estado; true responde success y false error. Cero filas afectadas es solo fixture con query=true: el método no consulta conteo. No se ejecutó transición real ni reloj SQL. Casos: `state-ok`, `state-sql-fail`, `state-zero-affected`.

**Deduplicación:** RN-25..RN-27 ya describen etiquetas, botones y UPDATE por ID. Añadir origen exacto de fechas y alcance de garantías; no abrir nuevo bypass ni afirmar visualización de estado0 sin distinguir int/string.

**Destino sugerido, sin editar:** `knowledge/general/business-rules.md#RN-25`, `knowledge/general/business-rules.md#RN-27`, `knowledge/general/workflows.md#F-04`.

**Perú:** No se atribuye regresión de timestamps sin DDL de ambas variantes.

**TO-BE, no aplicado:** Documentar campos por fuente y confirmar política de transiciones; exigirla atómicamente y comprobar filas afectadas cuando proceda.

### TEMP-T010 · La conversión de fechas no valida el calendario ni acepta ISO

**improvement · P2 · Semántica de entrada de localizaciones**

**AS-IS / impacto condicionado:** castDate permuta tres segmentos separados por /:31/02/2026 sale2026-02-31 sin validar. ISO2026-11-18 se sustituye por1900-01-01; vacío usa el mismo centinela. No se debe describir como validación completa ni afirmar que una fecha imposible se persistirá.

**Condiciones:** Entrada alcanza castDate; contrato real de formato/ausencia requiere confirmación. Aceptación SQL depende de tipos, versión y sql_mode desconocidos.

**Evidencia:** `M:index_archivos/tracking/TrackingNewClass.php:L1198-L1200`; `M:index_archivos/tracking/TrackingNewClass.php:L1214-L1217`; `M:index_archivos/tracking/TrackingNewClass.php:L1304-L1312`.

**Validación:** Control DD/MM correcto ->2026-11-18; ISO ->1900-01-01; fecha imposible ->2026-02-31; vacío ->1900-01-01. Método extraído sin SQL. Casos: `date-18/11/2026`, `date-2026-11-18`, `date-31/02/2026`, `date-empty`.

**Deduplicación:** F-04 no promete validación completa; RN-30/RN-31 ya documentan fechas de Excel sustituidas. Precisión de otra ruta, sin duplicar esa anomalía ni inventar política calendárica.

**Destino sugerido, sin editar:** `knowledge/general/workflows.md#F-04`, `knowledge/general/business-rules.md#RN-21`.

**Perú:** Solo M se ejecutó en el probe; no se reclama exclusividad de país.

**TO-BE, no aplicado:** Acordar formato/ausencia, validar calendario y responder error o NULL explícito según el contrato.

### TEMP-T011 · La sustitución de costos carece de reversión y puede anunciar éxito tras fallar el detalle

**duplicate_or_rejected · P2 · Deduplicación: sustitución de costos**

**AS-IS / impacto condicionado:** Se emiten marcas de borrado antes del reemplazo. Maestro=false devuelve error sin restauración; detalle=false intenta DELETE del nuevo maestro y retorna success; las marcas false tampoco se verifican.

**Condiciones:** Marcas deleted_at previas aceptadas y fallo de maestro/detalle posterior. Persistencia condicionada a autocommit y ausencia de transacción externa.

**Evidencia:** `M:index_archivos/embarques/CostosClass.php:L355-L378`; `M:index_archivos/embarques/CostosClass.php:L443-L450`; `M:index_archivos/embarques/CostosClass.php:L576-L594`.

**Validación:** Inyección por etapa reproduce queries y respuestas; no se probó rollback real. Casos: `cost-master-fail`, `cost-detail-fail`, `cost-delete-fail`, `cost-empty`.

**Deduplicación:** Duplicado explícito RN-40/F-08/U09. Se adjunta caracterización, no nuevo hallazgo. TEMP-T001 sí añade seleccionar/borrar un ID de otra petición.

**Destino sugerido, sin editar:** `knowledge/general/business-rules.md#RN-40`, `knowledge/general/workflows.md#F-08`, `knowledge/general/user-manual.md#U09`.

**Perú:** No se reclama novedad frente a P.

**TO-BE, no aplicado:** Vincular pruebas a advertencia existente, sin abrir otra entrada genérica.

### TEMP-T012 · La limpieza del viaje solo borra cabecera y la edición conserva pasos previos

**duplicate_or_rejected · P2 · Deduplicación: catch de multiescrituras**

**AS-IS / impacto condicionado:** Alta emite DELETE de cabecera; catch de edición no limpia. No prueba hijos huérfanos: el resultado depende de constraints/cascadas desconocidas.

**Condiciones:** Exception capturada tras escrituras previas. DDL/cascadas/triggers no disponibles.

**Evidencia:** `M:index_archivos/tracking/TrackingNewClass.php:L230-L235`; `M:index_archivos/tracking/TrackingNewClass.php:L281-L285`; `P:index_archivos/tracking/TrackingNewClass.php:L230-L234`.

**Validación:** Fallo de orden produce DELETE cabecera y100. Consulta acredita alcance explícito, no efectos de cascadas. Casos: `save-order-fail`, `edit-load-delete-fail`.

**Deduplicación:** RN-21/RN-23/F-04 ya dicen esto y no prometen rollback. Se rechaza duplicarlo o afirmar orfandad física. TEMP-T002 y TEMP-T003 son causas nuevas diferentes.

**Destino sugerido, sin editar:** `knowledge/general/business-rules.md#RN-21`, `knowledge/general/business-rules.md#RN-23`, `knowledge/general/workflows.md#F-04`.

**Perú:** P conserva DELETE de cabecera en230-234.

**TO-BE, no aplicado:** Mantener advertencia y obtener DDL para evaluar integridad física.

### TEMP-T013 · El agregador de importación anuncia éxito sin revisar cada creación

**duplicate_or_rejected · P2 · Deduplicación: carga masiva parcial**

**AS-IS / impacto condicionado:** Agregador toma newId sin comprobar code y asigna status200. Es distinto del marcado prematuro de lote en TEMP-T004.

**Condiciones:** Un grupo devuelve100 y el agregador continúa.

**Evidencia:** `M:index_archivos/tracking/ajax/uploadExcelCargaMasiva.php:L219-L238`; `M:index_archivos/tracking/controllers/CargaMasiva.php:L574-L588`.

**Validación:** Traza estática completa del bloque. No se ejecutó endpoint, lector Excel ni upload; probe de crearViaje no se presenta como prueba del agregador.

**Deduplicación:** RN-33/F-05/U06 ya expresan la anomalía. No se vuelve a contar por ausencia de transacción global ni por reintento potencialmente duplicado.

**Destino sugerido, sin editar:** `knowledge/general/business-rules.md#RN-33`, `knowledge/general/workflows.md#F-05`, `knowledge/general/user-manual.md#U06`.

**Perú:** No se reclama regresión de P.

**TO-BE, no aplicado:** Vincular corrección a la regla existente; conservar marcado por grupo como delta distinta.

### TEMP-T014 · No se demuestra la atomicidad ni el estado resultante de rutinas SQL ausentes

**duplicate_or_rejected · P2 · Control negativo estático: duplicado, borrado y unicidad**

**AS-IS / impacto condicionado:** CALL no revela qué hijos se copian, estado inicial o rollback interno. SELECT/INSERT de EDP no demuestra duplicados persistidos si hay un índice único desconocido.

**Condiciones:** No hay definición verificada de tck_duplicar_viaje/sp_delete_trip, índices o triggers.

**Evidencia:** `M:index_archivos/tracking/TrackingNewClass.php:L947-L964`; `M:index_archivos/tracking/HerramientasClass.php:L5-L20`; `M:index_archivos/tracking/TrackingNewClass.php:L1635-L1648`.

**Validación:** Solo envoltorios inspeccionados. No se ejecutaron procedimientos ni se modeló su interior. PrioridadP2 identifica la revisión pendiente, no un defecto probado.

**Deduplicación:** RN-28/límites ya advierten ausencia de cuerpos; RN-22 describe comprobación EDP. Se rechaza elevar esas pistas a defectos verificados.

**Destino sugerido, sin editar:** `knowledge/general/business-rules.md#RN-22`, `knowledge/general/business-rules.md#RN-28`, `knowledge/general/business-rules.md#Límites-de-validez`.

**Perú:** No se atribuyen diferencias de rutinas entre países sin definiciones.

**TO-BE, no aplicado:** Obtener DDL/cuerpos y probarlos en entorno aislado autorizado antes de afirmar estados o atomicidad.

## Integridad y límites

Validación de artefactos: 14 IDs únicos, 57 rangos de evidencia comprobados en Git (17 pares commit/archivo), fuentes M iguales al checkout, IDs de probes/controles y enlaces Markdown resueltos, script Python compilable sin emitir bytecode. Diff de aplicación y de registro/documentación general vacío al verificar.

Solo se escriben este MD, su JSON paralelo, `scripts/audit/transaction_probes.py` y el JSON de probes indicado. No se modifica aplicación, registro principal, docs generales o manifest; no se ejecutaron rutas reales, BD/red, persistencia de sesión, commits o push. Otros sidecars pueden pertenecer al trabajo paralelo; no se modifican ni se atribuyen.

Incidencias del harness: dos erratas de ensamblado PHP se corrigieron durante el desarrollo (carácter sobrante del parser y paréntesis del doble). Las ejecuciones finales reproducen34/34. El generador en línea de sidecars excedió la longitud de comando de Windows y fue rechazado antes de ejecutarse; se sustituyó por escritura mediante apply_patch. Ninguna de estas incidencias se atribuye a la aplicación.

❓ Pendientes: runtime desplegado y manejo de errores, DDL/índices/triggers, persistencia real, política de estados, contrato del evento26 y escenarios con datos autorizados. Este sidecar no certifica un dominio completo, una release o la seguridad de un despliegue.

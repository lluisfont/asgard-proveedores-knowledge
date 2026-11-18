# Hallazgos operativos — revisión de fuente del 18-11-2026

**9 hallazgos operativos (2 P1, 7 P2) y 8 mejoras integrados por instrucción del usuario. Sin aprobación canónica ni convergencia global.**

Código M: `a8ce2c23dead8552d2c4699e4a9b9134f7a18707`; referencia P: `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62`. Fuente: `C:/repos/proveedores-github-review-20261118`. Baseline documental K: `3822900b6d54d99ccf854bec43005a208e2a9694` en `C:/repos/asgard-proveedores-knowledge`.

**Actualidad de la referencia:** P95fe9a4 es el pin histórico de comparación, no el último Perú. El principal observó2a179e2e6472d5705d031665ecbc90c3d806edec en [remote-refs-observation.json](../../source-audits/master/2026-11-18/iterative/remote-refs-observation.json); ese head no está auditado. IMP-SCOPE001 pertenece al principal y no se duplica como mejora operacional. No se cambian refs.

Los pins de código figuran como evidencia de fuente. Las afirmaciones heredadas de documentación se conservan en una sección separada y no se convierten en evidencia del programa. Todos los impactos desplegados permanecen condicionados; las reglas propuestas son TO-BE, no comportamiento actual ni política aprobada.

| ID | Origen | Prioridad | Hallazgo |
|---|---|---|---|
| OPS-001 | TEMP-T001 | P1 | El guardado de costos puede insertar detalles o borrar el maestro de otra petición |
| OPS-002 | TEMP-T002 | P2 | El resultado de localizaciones oculta fallos según su posición |
| OPS-003 | TEMP-T003 | P1 | La edición borra la carga y llama a su reemplazo con un argumento ausente |
| OPS-004 | TEMP-T004 | P2 | Crear un viaje marca como procesados todos los grupos del lote |
| OPS-005 | TEMP-T005 | P2 | La mezcla por posición puede duplicar u omitir eventos pendientes |
| OPS-006 | TEMP-T006 | P2 | La excepción del evento 26 falla si aparece en la primera posición |
| OPS-007 | TEMP-T007 | P2 | El servidor acepta un total de costos distinto de la suma de conceptos |
| OPS-008 | TEMP-C4 | P2 | La edición amplía chasis de un pedido existente sin verificar su selección y puede confirmar una actualización incompleta |
| OPS-009 | principal/static-arity-review | P2 | La acción mostrartabla llama al listado de embarques sin el argumento logistica obligatorio |

## Evidencia y reglas propuestas

### OPS-001 · El guardado de costos puede insertar detalles o borrar el maestro de otra petición

**Costos: selección de maestro posterior al INSERT · P1 · KNOWN_DEFECT**

**AS-IS:** A selecciona el máximo id por embarque/created_by sin usar su ID de inserción ni filtrar categoría. Puede insertar sus conceptos en B y, si falla el detalle, emitir DELETE del maestro B. A puede quedar sin detalle. No exige SQLi ni otro tenant.

**Condiciones:** Dos peticiones del mismo proveedor crean costos del mismo embarque; pueden usar categorías distintas. B confirma su maestro entre el INSERT y el SELECT de A; ausencia de aislamiento/bloqueo externo que lo impida. El borrado requiere que el INSERT de detalle devuelva false sin lanzar excepción.

**Evidencia de código:** `M:index_archivos/embarques/CostosClass.php:L576-L592`; `M:index_archivos/embarques/CostosClass.php:L382-L390`; `M:index_archivos/embarques/CostosClass.php:L399-L415`; `P:index_archivos/embarques/CostosClass.php:L578-L594`.

**Validación y alcance:** El doble asigna INSERT propio101 y agenda el maestro concurrente102 al SELECT posterior. Se emitió detalle costos_id102 y, con detalle=false, DELETE id102, conservando success. El control secuencial usa101. Intercalado programado, sin hilos ni SQL real. La integración revisa evidencia previa; no repite la ejecución de los probes.

**Deduplicación:** RN-40/F-08/U09 ya advierten falta de atomicidad y falso éxito. No describen seleccionar ni borrar el maestro de otra petición. SEC-006 trata interpolación SQL, no esta carrera con valores normales.

**Baseline documental relacionado:** BL-01, BL-10.

**Regla de uso propuesta — TO-BE, no aprobada:** Capturar inmediatamente el ID propio en la conexión del INSERT; sustituir costos y detalles en una transacción y notificar después de confirmar.

**Límites:** Evidencia de fuente y pruebas aisladas; sin SQL real, despliegue o persistencia confirmados. Retornos false inyectados solo modelan configuración que no lanza excepción; autocommit, constraints y triggers desconocidos.

**Perú:** P conserva SELECT último id y DELETE de ese id en578-594; la conversión mysql/mysqli no lo corrige.

### OPS-002 · El resultado de localizaciones oculta fallos según su posición

**Tracking: alta y edición de orígenes/destinos · P2 · KNOWN_DEFECT**

**AS-IS:** statusSave solo se actualiza tras insertar una localización. Un fallo temprano de subítems se sobreescribe con un éxito posterior; un fallo tardío del INSERT de localización conserva el true anterior. saveLocation retorna true y su llamador puede responder éxito sin todos los destinos/cargas.

**Condiciones:** Dos o más localizaciones. Una consulta devuelve false y el flujo continúa; si mysqli lanza una excepción el efecto puede diferir. Otra localización logra insertar sus subítems; los demás pasos pueden completarse.

**Evidencia de código:** `M:index_archivos/tracking/TrackingNewClass.php:L1192-L1239`; `M:index_archivos/tracking/TrackingNewClass.php:L1315-L1333`; `M:index_archivos/tracking/TrackingNewClass.php:L204-L214`; `M:index_archivos/tracking/TrackingNewClass.php:L1592-L1600`; `P:index_archivos/tracking/TrackingNewClass.php:L1227-L1239`.

**Validación y alcance:** Tres agendas mixtas retornan true pese a una consulta false. Último subítem fallido, todas las localizaciones fallidas y array vacío retornan false. Se extrajeron saveLocation/subItems/castDate sin cambiar cuerpos; queries/resultados están en el artifact. La integración revisa evidencia previa; no repite la ejecución de los probes.

**Deduplicación:** RN-21/F-04 mencionan fallos comprobados de pasos principales y RN-23 edición parcial. Falta el mecanismo que convierte fallos principales en éxito y su dependencia del orden; no se vuelve a contar el catch incompleto.

**Baseline documental relacionado:** BL-02, BL-08.

**Regla de uso propuesta — TO-BE, no aprobada:** Abortar ante cada fallo y evitar que un resultado posterior sobrescriba el error; definir la transacción de la unidad lógica.

**Límites:** Evidencia de fuente y pruebas aisladas; sin SQL real, despliegue o persistencia confirmados. Retornos false inyectados solo modelan configuración que no lanza excepción; autocommit, constraints y triggers desconocidos.

**Perú:** La acumulación statusSave se conserva en P:1227-1239.

### OPS-003 · La edición borra la carga y llama a su reemplazo con un argumento ausente

**TrackingNewClass::edit → editLoad → saveLoad · P1 · KNOWN_DEFECT**

**AS-IS:** saveLoad requiere descripcionMercancia como quinto argumento, pero editLoad pasa cuatro después de borrar. En PHP probado se lanza ArgumentCountError antes del INSERT; catch(Exception) de edit no lo captura. No retorna su code100 ni repone la carga. La respuesta HTTP final depende del servidor; no se necesita un fallo SQL.

**Condiciones:** La edición alcanza editLoad y DELETE devuelve true; pasos previos no abortan. PHP local8.4.25 reproduce ArgumentCountError; no se ejecutó PHP5.4 declarado en Docker. Pérdida persistente condicionada a DELETE confirmado/autocommit y ausencia de reversión externa. Para afirmar eliminación de carga previa, deben existir filas que coincidan con los filtros del DELETE y su borrado debe confirmarse; query=true con0filas no acredita pérdida.

**Evidencia de código:** `M:index_archivos/tracking/TrackingNewClass.php:L257-L285`; `M:index_archivos/tracking/TrackingNewClass.php:L1581-L1589`; `M:index_archivos/tracking/TrackingNewClass.php:L1166-L1189`; `M:index_archivos/tracking/ajaxAsignacion/editar_asignacion.php:L68-L76`; `M:Dockerfile:L1-L6`; `P:index_archivos/tracking/TrackingNewClass.php:L1581-L1589`; `P:index_archivos/tracking/TrackingNewClass.php:L1166-L1168`.

**Validación y alcance:** edit extraído con DELETE=true alcanzó ArgumentCountError tras una sola consulta DELETE, sin INSERT ni respuesta del método. DELETE=false evita la llamada inválida y devuelve100. Pasos previos simulados con éxito; sin borrado real ni ejecución de PHP5.4. La integración revisa evidencia previa; no repite la ejecución de los probes.

**Deduplicación:** RN-23/F-04 solo advierten actualizaciones parciales. RN-34 describe otra aridad distinta (crearViaje desde embarquesController), que no cubre este DELETE. Nueva causa concreta, con runtime condicionado.

**Baseline documental relacionado:** BL-02, BL-08.

**Regla de uso propuesta — TO-BE, no aprobada:** Pasar la descripción requerida y validar el objeto antes de borrar; reemplazar carga dentro de transacción y revisar Throwable al modernizar PHP.

**Límites:** Evidencia de fuente y pruebas aisladas; sin SQL real, despliegue o persistencia confirmados. Retornos false inyectados solo modelan configuración que no lanza excepción; autocommit, constraints y triggers desconocidos.

**Perú:** P conserva firma de cinco argumentos y llamada de cuatro en1166 y1581-1589.

### OPS-004 · Crear un viaje marca como procesados todos los grupos del lote

**Carga masiva: estado por grupo · P2 · KNOWN_DEFECT**

**AS-IS:** El UPDATE filtra lote/cuenta, no numero_viaje: el primer grupo intenta marcar estado1 también en filas sin viaje creado. Tras fallo posterior, la señal de procesado queda adelantada; la limpieza inicial de otra carga solo elimina estado nulo/0 y excluye esas filas. No se afirma que un nuevo fichero no pueda reinsertarlas ni que no exista reintento manual.

**Condiciones:** Lote con dos o más numero_viaje de una cuenta. Primer crearViaje alcanza UPDATE y se confirma; otro grupo aún no se intenta o falla después. Ausencia de corrección externa de ese marcado.

**Evidencia de código:** `M:index_archivos/tracking/controllers/CargaMasiva.php:L361-L367`; `M:index_archivos/tracking/controllers/CargaMasiva.php:L574-L588`; `M:index_archivos/tracking/ajax/uploadExcelCargaMasiva.php:L208-L226`; `M:index_archivos/tracking/controllers/CargaMasiva.php:L23-L29`; `P:index_archivos/tracking/controllers/CargaMasiva.php:L590-L597`.

**Validación y alcance:** crearViaje extraído para grupo1 emite UPDATE lote88/cuenta22 sin numero_viaje antes de devolver200. Fixture declara grupos1/2; grupo2 no se ejecuta. Fallo temprano de cabecera devuelve100 sin UPDATE. No se emularon filas persistentes ni lote completo. La integración revisa evidencia previa; no repite la ejecución de los probes.

**Deduplicación:** RN-33/F-05 ya documentan agregador que ignora códigos. Esta transición sigue siendo incorrecta aunque el agregador detecte el fallo: grupos futuros ya fueron marcados. RN-31 no describe ese adelanto.

**Baseline documental relacionado:** BL-03, BL-09.

**Regla de uso propuesta — TO-BE, no aprobada:** Marcar solo el grupo confirmado y asociarle el ID creado; separar progreso por viaje/lote y definir reintento idempotente.

**Límites:** Evidencia de fuente y pruebas aisladas; sin SQL real, despliegue o persistencia confirmados. Retornos false inyectados solo modelan configuración que no lanza excepción; autocommit, constraints y triggers desconocidos.

**Perú:** P aplica el mismo UPDATE de lote completo en590-591.

### OPS-005 · La mezcla por posición puede duplicar u omitir eventos pendientes

**Detalle: orden temporal frente a catálogo remoto · P2 · KNOWN_DEFECT**

**AS-IS:** Se sobrescriben posiciones del catálogo con filas ordenadas por fecharegistro sin reconciliar IDs. Remotos[3,5,7] y detalle[5] producen[5,5,7]: desaparece pendiente3 y se duplica5. Detalle[3,3] produce[3,3,7], omitiendo5. El defecto demostrado es de representación, no modificación del historial SQL.

**Condiciones:** API devuelve lista no vacía. Detalle local no es un prefijo único del catálogo: evento adelantado, repetido o registrado fuera de orden. Las filas alcanzan el ensamblador; no se presuponen restricciones de unicidad desconocidas.

**Evidencia de código:** `M:index_archivos/tracking/ListaViajesClass.php:L157-L190`; `M:index_archivos/tracking/ListaViajesClass.php:L387-L409`; `M:index_archivos/tracking/viajedetalle.php:L89-L90`; `P:index_archivos/tracking/ListaViajesClass.php:L157-L190`.

**Validación y alcance:** eventosViaje extraído con dobles locales de eventos/getEventName reproduce ambos contraejemplos. Prefijo[3] produce[3,5,7]; API vacía conserva[5]. ORDER BY fecharegistro no tiene desempate explícito, pero no se observó orden real de BD. La integración revisa evidencia previa; no repite la ejecución de los probes.

**Deduplicación:** RN-29/F-04 recogen consulta remota y conservación si vacía, no el requisito implícito de prefijo. No duplica advertencias de efectos parciales ni subidas de SEC-010.

**Baseline documental relacionado:** BL-04.

**Regla de uso propuesta — TO-BE, no aprobada:** Reconciliar por identidad y definir representación de repeticiones/omitidos y orden temporal, sin reemplazar catálogo por índices de historial.

**Límites:** Evidencia de fuente y pruebas aisladas; sin SQL real, despliegue o persistencia confirmados. Retornos false inyectados solo modelan configuración que no lanza excepción; autocommit, constraints y triggers desconocidos.

**Perú:** P conserva el ensamblado posicional en157-190.

### OPS-006 · La excepción del evento 26 falla si aparece en la primera posición

**Detalle: presencia de evento mediante array_search · P2 · KNOWN_DEFECT**

**AS-IS:** array_search devuelve0 y el if lo interpreta como false. El mismo26 detiene el ensamblado en índice1, pero en índice0 se añaden hitos del catálogo. Remotos[3,5,7] con detalle[26] producen[26,5,7]; detalle[3,26] se conserva. No se atribuye nombre o significado de cierre al evento26. Si el primer26está en índice0, la guardia falla aunque existan otros26en posiciones posteriores: array_search conserva la primera coincidencia.

**Condiciones:** Catálogo remoto no vacío y detalle con id26 en índice0. Significado empresarial de26 requiere confirmación; solo se acredita la excepción de presencia implementada.

**Evidencia de código:** `M:index_archivos/tracking/ListaViajesClass.php:L159-L174`; `P:index_archivos/tracking/ListaViajesClass.php:L166-L174`.

**Validación y alcance:** Prueba diferencial reproduce índice0 frente a1; API vacía sale antes de la condición. La palabra terminal en el ID técnico del probe es una etiqueta del harness, no un significado de negocio confirmado. La integración revisa evidencia previa; no repite la ejecución de los probes.

**Deduplicación:** Independiente de TEMP-T005: la búsqueda booleana falla sin historial desordenado ni duplicado; arreglar el merge no necesariamente corrige esta salida temprana. RN-29 no describe la excepción26.

**Baseline documental relacionado:** BL-04.

**Regla de uso propuesta — TO-BE, no aprobada:** Comparar array_search contra false estrictamente o usar comprobación de pertenencia; confirmar el contrato de26 antes de documentarlo como cierre.

**Límites:** Evidencia de fuente y pruebas aisladas; sin SQL real, despliegue o persistencia confirmados. Retornos false inyectados solo modelan configuración que no lanza excepción; autocommit, constraints y triggers desconocidos.

**Perú:** El mismo if aparece en P:166-168.

### OPS-007 · El servidor acepta un total de costos distinto de la suma de conceptos

**Costos: invariante monetario maestro/detalle · P2 · KNOWN_DEFECT**

**AS-IS:** El navegador suma importes, pero el servidor inserta totalCategory como total_costos y cada amount por separado sin recalcular/comparar. Total999 y conceptos10+20 generan esas tres cantidades y success. getCostos devuelve total almacenado y detalle, que pueden discrepar si la BD confirma. No se infiere impacto contable ni regla de signos.

**Condiciones:** Petición de costos con conceptos numéricos y totalCategory alterado u obsoleto. INSERTs aceptados y ausencia de trigger/constraint que recalcule o rechace la discrepancia.

**Evidencia de código:** `M:index_archivos/embarques/ajax/guardar-costos.php:L1-L8`; `M:index_archivos/embarques/CostosClass.php:L355-L390`; `M:index_archivos/embarques/CostosClass.php:L576-L588`; `M:index_archivos/embarques/CostosClass.php:L399-L414`; `M:index_archivos/embarques/componentes/costos/card-component.js:L106-L113`; `P:index_archivos/embarques/CostosClass.php:L578-L590`.

**Validación y alcance:** El doble captura999 en INSERT maestro y10/20 en detalle con success; aserciones comprueban las tres cantidades. Control coherente usa30; conceptos vacíos se rechazan sin queries. No acredita persistencia frente a constraints desconocidos. La integración revisa evidencia previa; no repite la ejecución de los probes.

**Deduplicación:** RN-40/F-08 describen controles de navegador y sustitución, no este contraejemplo monetario. SEC-006 trata manipulación de sintaxis; aquí solo hay números simples. No se cuenta como otro SQLi.

**Baseline documental relacionado:** BL-01, BL-10.

**Regla de uso propuesta — TO-BE, no aprobada:** Validar cantidades/moneda y calcular total en servidor con precisión monetaria definida; persistir maestro/detalle como una unidad.

**Límites:** Evidencia de fuente y pruebas aisladas; sin SQL real, despliegue o persistencia confirmados. Retornos false inyectados solo modelan configuración que no lanza excepción; autocommit, constraints y triggers desconocidos.

**Perú:** P también confía en totalCategory/amount (578-590 y384-392).

### OPS-008 · La edición amplía chasis de un pedido existente sin verificar su selección y puede confirmar una actualización incompleta

**editarController → editarCotizacionCliente → getPedidos → crearPedidosDetalle; separado del alta · P2 · KNOWN_DEFECT**

**AS-IS:** En alta, guardarCotizacionCliente llama a crearPedidosEmbarqueLocal solo para cliente417/alcance3 y crea cabecera de pedido. En edición, editarController acepta nuevoschasis y editarCotizacionCliente llama getPedidos/crearPedidosDetalle si es truthy, sin repetir en esa cadena la condición cliente417/local del formulario. getPedidos usa embarque_id LIMIT1 sin ORDER BY ni deleted_at; no selecciona explícitamente un pedido válido único ni crea uno si falta. crearPedidosDetalle no devuelve un resultado, ignora retornos de INSERT y UPDATE de descripción, y el padre retorna code200 si el UPDATE de cabecera fue true. code200 no acredita chasis añadidos; editarController recoge $result y redirige sin comprobarlo. La redirección tampoco acredita éxito. No se declara acceso entre tenants, ni que la política UI sea por sí misma la política de servidor aprobada.

**Condiciones:** La petición de edición supera bootstrap y controles externos; el UPDATE de cabecera se ejecuta con éxito y pasos previos no abortan. `nuevoschasis` tiene valor truthy en PHP (no equivale exactamente a cualquier string no vacío: '0' es falsy). Para completar detalles hace falta un pedido existente seleccionado; la ausencia de pedido no desencadena creación de cabecera. El falso éxito ante fallos SQL requiere que estos retornen false y las llamadas posteriores continúen; si lanzan excepción, el desenlace puede diferir. Persistencia y política válida de cliente/alcance requieren DDL/configuración/validación empresarial no disponibles.

**Evidencia de código:** `M:index_archivos/embarques/editar.php:L110-L122`; `M:index_archivos/embarques/componentes/embarques_mercancia.php:L4-L23`; `M:index_archivos/embarques/editarController.php:L25-L33`; `M:index_archivos/embarques/editarController.php:L54-L56`; `M:index_archivos/embarques/CotizacionClass.php:L1195-L1206`; `M:index_archivos/embarques/CotizacionClass.php:L1342-L1367`; `P:index_archivos/embarques/editarController.php:L27-L38`; `P:index_archivos/embarques/editarController.php:L59-L63`; `P:index_archivos/embarques/CotizacionClass.php:L1209-L1223`; `P:index_archivos/embarques/CotizacionClass.php:L1397-L1422`; `M:index_archivos/embarques/CotizacionClass.php:L680-L694`; `M:index_archivos/embarques/CotizacionClass.php:L1288-L1309`; `M:index_archivos/embarques/editarController.php:L56-L70`.

**Validación y alcance:** Cliente999/alcance1 con nuevoschasis sí alcanza INSERT de detalle en ambas ramas; vacío no lo alcanza. Pedido ausente e INSERT simulado false: devuelve code200 y alcanza UPDATE de descripción. Los probes heredados neutralizan magnitudes/tramos y sustituyen SQL; no prueban escrituras reales ni acceso de la ruta. Revisión actual confirmó directamente la diferencia entre alta/edición, retorno implícito del helper y consumo de $result.

**Deduplicación:** Distinto de RN-14 (alta y escrituras hijas), RN-15 (personalización del alta), RN-34/OPS-003 (aridad de otros métodos) y SEC-006 (interpolación). Integra la selección de pedido y la señal de éxito de esta edición en una sola entrada OPS-008; no abre un hallazgo por cada fallo subordinado.

**Baseline documental relacionado:** BL-05, BL-06.

**Regla de uso propuesta — TO-BE, no aprobada:** Definir y validar en servidor el ámbito permitido de ampliación; exigir pedido existente, activo y único o elección explícita autorizada. Confirmar adición solo cuando detalles y descripción se reconcilien en una transacción. Devolver y consumir resultados; no usar redirección como confirmación de adición. El helper debe definir un retorno explícito antes de comprobarlo: actualmente retornaNULL incluso con operaciones exitosas; añadir solo if(!crearPedidosDetalle(...)) rechazaría también esos éxitos.

**Límites:** UI417/local es evidencia de presentación, no autorización probada. No se ha confirmado unicidad, constraints, flags de detalle o cascadas del esquema. No se ejecutó el controlador, BD, entrega de mensajes ni sesión persistente.

**Perú:** La edición P mantiene la misma cadena en CotizacionClass.php1209-1223,1397-1422 y editarController.php38,63. P añade pasos de concesionario que no se ejecutaron; no se atribuye igualdad de todos los efectos.

### OPS-009 · La acción mostrartabla llama al listado de embarques sin el argumento logistica obligatorio

**embarquesController.php accion=mostrartabla; independiente de ajax/listaEmbarques.php · P2 · KNOWN_DEFECT**

**AS-IS:** EmbarqueClass::getListaEmbarques exige dos argumentos ($idtransportista,$logistica) y tiene tres opcionales. La acción mostrartabla pasa solo la sesión idtransportista. PHP8 arroja ArgumentCountError antes de entrar al método: no se atribuye a SQL del cuerpo ni a filas del listado. datosCotizacion.js162 contiene una petición candidata, sin demostrar reachability. Las llamadas de ajax/listaEmbarques.php40 y42 pasan respectivamente5 y2 argumentos; OPS-009 no describe un fallo de esa ruta.

**Condiciones:** La ejecución alcanza accion=mostrartabla y su llamada estática; bootstrap/guardias/dependencias previas no abortan. PHP8 reproduce rechazo de aridad antes del cuerpo. PHP5.4 declarado en Docker no se ejecutó. La llamada JavaScript solo es un candidato condicionado por #tablaCotizaciones; no se ha probado montaje, carga o alcance real.

**Evidencia de código:** `M:index_archivos/embarques/embarquesController.php:L16-L22`; `M:index_archivos/embarques/EmbarqueClass.php:L129-L135`; `M:index_archivos/embarques/js/datosCotizacion.js:L153-L163`; `M:index_archivos/embarques/ajax/listaEmbarques.php:L40-L42`; `M:Dockerfile:L1-L6`; `P:index_archivos/embarques/embarquesController.php:L18-L20`; `P:index_archivos/embarques/EmbarqueClass.php:L173-L179`.

**Validación y alcance:** Artifact del principal revisado: PHP8.4.25, 1 argumento→ArgumentCountError; 2 y5→signature_satisfied; 3/3. Se conserva la firma original y se reemplaza todo el cuerpo con sentinel. Censo reportado279files/460defs/542resolved es cobertura token-only, no cobertura de rutas ni despliegue. No se ejecutó controller ni PHP5.4.

**Deduplicación:** Mismo tipo técnico que OPS-003 pero otra llamada, método y efecto: OPS-003 borra carga antes del error; OPS-009 no entra al cuerpo del listado. RN-34 trata crearViaje con2/3 argumentos, ya documentado, sin otra entrada. Control negativo explícito: ajax/listaEmbarques.php40-42 satisface la firma.

**Baseline documental relacionado:** BL-03.

**Regla de uso propuesta — TO-BE, no aprobada:** Definir el alcance logístico requerido por mostrartabla y pasarlo validado; comprobar todas las llamadas contra la firma. No comunicar indisponibilidad de la ruta AJAX que ya pasa argumentos completos ni prometer reachability desde un candidato JS.

**Límites:** Sin alcance real o exposición comprobados. No se deduce comportamiento PHP5.4 de la prueba PHP8. No demuestra fallo de datos, consultas, permisos o listado AJAX completo.

**Perú:** P conserva la llamada de1 argumento en controller20 y firma de2 obligatorios en EmbarqueClass173. El probe PHP8 usa M; no se ejecuta el cuerpo de ninguna variante.

### IMP-T008 · Precisar qué escrituras del viaje se comprueban y cuáles pueden fallar sin error

**Documentación de multiescrituras · P2 · AS-IS_DOCUMENTATION_PRECISION**

**AS-IS:** save ignora resultados de rutas, relevo y registro de ubicaciones; EDP tampoco propaga el resultado. Puede devolver200 con esas operaciones fallidas. saveRoutes también devuelvefalse sin aduana, que puede ser ausencia opcional válida. No toda devolución false equivale a fallo empresarial.

**Condiciones:** Pasos comprobados exitosos. Rutas/relevo/catálogo de ubicaciones retornan false sin lanzar; integraciones no abortan.

**Evidencia de código:** `M:index_archivos/tracking/TrackingNewClass.php:L184-L234`; `M:index_archivos/tracking/TrackingNewClass.php:L1336-L1344`; `M:index_archivos/tracking/TrackingNewClass.php:L274-L285`; `M:index_archivos/tracking/TrackingNewClass.php:L1635-L1648`.

**Validación y alcance:** save extraído devuelve200 con false en rutas/relevo/ubicaciones. Control: saveOrder=false produce100 y DELETE cabecera. No se invocaron integraciones. La integración revisa evidencia previa; no repite la ejecución de los probes.

**Deduplicación:** Precisión de RN-21/RN-22/F-04; no se cuenta otra advertencia genérica de parcialidad ni se convierte ausencia opcional en defecto.

**Baseline documental relacionado:** BL-02, BL-08.

**Regla de uso propuesta — TO-BE, no aprobada:** Enumerar resultados comprobados/ignorados y acordar qué datos son obligatorios antes de endurecer errores.

**Límites:** Precisión documental integrada aquí; no se editan las páginas originales ni se aprueba una política de negocio.

### IMP-T009 · Distinguir fecha de modificación, interrupción y transición válida de estado

**Semántica de estados y timestamps · P2 · AS-IS_DOCUMENTATION_PRECISION**

**AS-IS:** fecha_estado es alias de updated_at, no una fecha dedicada de transición. editInfo lo actualiza aunque no cambie estado; interrupción escribe fecha_interrupcion/estado2 sin asignar updated_at. El WHERE solo exige ID, sin estado previo, borrado lógico o comprobación de filas afectadas. Los filtros de UI no acreditan una máquina de estados del servidor. No se declara transición empresarial prohibida sin política validada.

**Condiciones:** Ruta de interrupción alcanza helper con sesión/conexión válidas. Efecto persistente y actualización automática de updated_at dependen de DDL/triggers desconocidos.

**Evidencia de código:** `M:index_archivos/tracking/ListaViajesClass.php:L30-L36`; `M:index_archivos/tracking/TrackingNewClass.php:L1509-L1521`; `M:index_archivos/tracking/HerramientasClass.php:L29-L47`; `M:index_archivos/tracking/listaviajes.php:L238-L238`; `M:index_archivos/tracking/listaviajes.php:L279-L284`; `M:index_archivos/tracking/ajax/discontinued-trip.php:L1-L10`.

**Validación y alcance:** Helper extraído emite WHERE id701 sin predicado de estado; true responde success y false error. Cero filas afectadas es solo fixture con query=true: el método no consulta conteo. No se ejecutó transición real ni reloj SQL. La integración revisa evidencia previa; no repite la ejecución de los probes.

**Deduplicación:** RN-25..RN-27 ya describen etiquetas, botones y UPDATE por ID. Añadir origen exacto de fechas y alcance de garantías; no abrir nuevo bypass ni afirmar visualización de estado0 sin distinguir int/string.

**Baseline documental relacionado:** BL-07.

**Regla de uso propuesta — TO-BE, no aprobada:** Documentar campos por fuente y confirmar política de transiciones; exigirla atómicamente y comprobar filas afectadas cuando proceda.

**Límites:** Precisión documental integrada aquí; no se editan las páginas originales ni se aprueba una política de negocio.

### IMP-T010 · La conversión de fechas no valida el calendario ni acepta ISO

**Semántica de entrada de localizaciones · P2 · AS-IS_DOCUMENTATION_PRECISION**

**AS-IS:** castDate permuta tres segmentos separados por /:31/02/2026 sale2026-02-31 sin validar. ISO2026-11-18 se sustituye por1900-01-01; vacío usa el mismo centinela. No se debe describir como validación completa ni afirmar que una fecha imposible se persistirá.

**Condiciones:** Entrada alcanza castDate; contrato real de formato/ausencia requiere confirmación. Aceptación SQL depende de tipos, versión y sql_mode desconocidos.

**Evidencia de código:** `M:index_archivos/tracking/TrackingNewClass.php:L1198-L1200`; `M:index_archivos/tracking/TrackingNewClass.php:L1214-L1217`; `M:index_archivos/tracking/TrackingNewClass.php:L1304-L1312`.

**Validación y alcance:** Control DD/MM correcto ->2026-11-18; ISO ->1900-01-01; fecha imposible ->2026-02-31; vacío ->1900-01-01. Método extraído sin SQL. La integración revisa evidencia previa; no repite la ejecución de los probes.

**Deduplicación:** F-04 no promete validación completa; RN-30/RN-31 ya documentan fechas de Excel sustituidas. Precisión de otra ruta, sin duplicar esa anomalía ni inventar política calendárica.

**Baseline documental relacionado:** BL-02.

**Regla de uso propuesta — TO-BE, no aprobada:** Acordar formato/ausencia, validar calendario y responder error o NULL explícito según el contrato.

**Límites:** Precisión documental integrada aquí; no se editan las páginas originales ni se aprueba una política de negocio.

## Revisión acotada posterior a OPS-009

La [revisión independiente](../reviews/iterative-20261118/closure-transactions.md) contrasta los nueve IDs mediante dependencias de retorno, predicados relacionales y modelos de datos bajo permutaciones; no repite inyección de fallos. Aporta tres precisiones materiales dentro de los IDs existentes: efecto cero del DELETE en OPS-003, repeticiones de 26 en OPS-006 y contrato de retorno NULL incluso en éxito en OPS-008. **Pasada 6 positiva con delta**, aceptada por el usuario: las tres precisiones se integran como CLR-IMP-001..003. No es una pasada de delta cero, no añade otro ID OPS ni declara convergencia global. El código reproducible y los dominios finitos figuran en el JSON de cierre.

### CLR-IMP-001 · El éxito del DELETE no demuestra filas borradas ni pérdida de carga

**Mejora material aceptada en pasada 6 · P2 · OPS-003**

**AS-IS / precisión:** El retorno comprobado es éxito de sentencia, sin consulta de filas afectadas. El contraejemplo con DELETE aceptado y0filas alcanza la llamada4/5 igualmente, pero no borra carga previa. La condición de pérdida requiere filas coincidentes y efecto confirmado.

**Evidencia de código:** `M:index_archivos/tracking/TrackingNewClass.php:L1581-L1589`; `M:index_archivos/tracking/TrackingNewClass.php:L1517-L1521`.

**Aporte de la revisión nueva:** La pasada anterior comparó DELETEtrue/false; esta pasada distingue efecto0/positivo con sentencia exitosa, sin inyectar fallos.

**Deduplicación:** Precisión del impacto de OPS-003; no otro hallazgo de aridad ni nueva entrada OPS.

**Regla propuesta — TO-BE, no aprobada como política:** Añadir precondición explícita de carga existente/coincidente y separar error de aridad de pérdida persistente. No interpretar la excepción como comprobación de borrado.

### CLR-IMP-002 · La primera coincidencia26 en índice0 oculta también repeticiones posteriores

**Mejora material aceptada en pasada 6 · P2 · OPS-006**

**AS-IS / precisión:** Sobre90historiales con26 de longitud1..4,40no activan la guardia;25de ellos tienen otro26posterior. array_search devuelve la primera coincidencia, no basta con que exista26fuera del índice0.

**Evidencia de código:** `M:index_archivos/tracking/ListaViajesClass.php:L166-L174`; `P:index_archivos/tracking/ListaViajesClass.php:L166-L174`.

**Aporte de la revisión nueva:** La prueba diferencial anterior usó[26] frente a[3,26]. El nuevo dominio enumera repeticiones y descubre la clase[26,26] y sus extensiones.

**Deduplicación:** Misma causa de OPS-006. Distinta de la mezcla de pendientes OPS-005; no se infiere significado de negocio de26.

**Regla propuesta — TO-BE, no aprobada como política:** Ampliar caracterización para la primera coincidencia y repeticiones; evitar una especificación de presencia basada en una posición no inicial aislada.

### CLR-IMP-003 · Comprobar un retorno booleano inexistente también rechazaría adiciones exitosas

**Mejora material aceptada en pasada 6 · P2 · OPS-008**

**AS-IS / precisión:** crearPedidosDetalle llega al final sin return aun con todas las sentencias exitosas: devuelveNULL implícito. Una corrección ingenua if(!crearPedidosDetalle(...)) detectaría también los éxitos como error. Seleccionar un pedido activo/único es una obligación separada; ordenar LIMIT1por sí solo no la cumple.

**Evidencia de código:** `M:index_archivos/embarques/CotizacionClass.php:L1195-L1206`; `M:index_archivos/embarques/CotizacionClass.php:L1342-L1367`; `M:index_archivos/embarques/editarController.php:L56-L70`; `P:index_archivos/embarques/CotizacionClass.php:L1397-L1422`.

**Aporte de la revisión nueva:** Se sustituye la agenda previa de fallos por prueba de totalidad del retorno y selección relacional con operaciones exitosas. Hace explícito un criterio de corrección que no estaba en la caracterización de fallos.

**Deduplicación:** Profundiza el TO-BE de OPS-008; ausencia de resultado y selección ya pertenecen a esa entrada. No se añade OPS-010.

**Regla propuesta — TO-BE, no aprobada como política:** Definir antes un resultado explícito de detalle/conciliación y consumirlo en padre/controlador; no añadir solo un if sobre el actual retornoNULL.

## Afirmaciones del baseline documental, separadas del código

| ID | Documento/pin | Afirmación heredada | Relación |
|---|---|---|---|
| BL-01 | `K:knowledge/general/business-rules.md:L73-L73` | RN-40: sustitución de costos, controles iniciales y falso éxito ya advertidos. | OPS-001, OPS-007 |
| BL-02 | `K:knowledge/general/business-rules.md:L44-L46` | RN-21..23: secuencia de alta/EDP/edición y parcialidad ya advertidas. | OPS-002, OPS-003, IMP-T008, IMP-T010 |
| BL-03 | `K:knowledge/general/business-rules.md:L59-L62` | RN-31..34: temporales, agregador y otra aridad crearViaje ya advertidos. | OPS-004, OPS-009 |
| BL-04 | `K:knowledge/general/business-rules.md:L52-L52` | RN-29: eventos remotos y conservación del detalle cuando están vacíos. | OPS-005, OPS-006 |
| BL-05 | `K:knowledge/general/business-rules.md:L32-L33` | RN-14/15: escrituras del alta y condición417/local; no cubre la edición de nuevoschasis. | OPS-008 |
| BL-06 | `K:knowledge/glossary/business-glossary.json:L889-L889` | Creación automática condicionada al alta local: no es el contrato de ampliación por edición. | OPS-008 |
| BL-07 | `K:knowledge/general/business-rules.md:L48-L50` | RN-25..27: etiquetas, botones e interrupción por ID; no garantizan fecha dedicada ni transiciones servidor. | IMP-T009 |
| BL-08 | `K:knowledge/general/workflows.md:L65-L65` | F-04: parcialidad y fallos posteriores al alta ya advertidos. | OPS-002, OPS-003, IMP-T008 |
| BL-09 | `K:knowledge/general/workflows.md:L79-L79` | F-05: agregador de carga no garantiza cada creación. | OPS-004 |
| BL-10 | `K:knowledge/general/workflows.md:L109-L109` | F-08: sustitución y falso éxito de costos sin validación contable. | OPS-001, OPS-007 |

## Obligaciones de reparación posteriores

La [nueva revisión de obligaciones](../reviews/iterative-20261118/closure-repair-obligations.md) completa 15 checks sobre los9OPS y las6mejoras aceptadas, con contraejemplos de éxito para reparaciones TO-BE. RPR-IMP-001/002 (conteo de filas/no-op y representación válida de IDs) están aceptadas e integradas como mejoras de la pasada8positiva con dos deltas. No son nuevos OPS ni convergencia global.

### RPR-IMP-001 · El retorno de actualización debe separar filas coincidentes, cambios y una operación sin cambios permitida

**Mejora TO-BE aceptada en pasada 8; no implementación o aprobación canónica.**

**Precisión:** El modelo de una sentencia exitosa con fila existente y valores ya iguales produce cero cambios. Un arreglo que traduce affected_rows==0 a inexistencia o error rechaza ese éxito permitido. La condición no debe confundirse con una fila que no coincide o no está autorizada.

**Condición:** La política TO-BE admite repetir una operación ya satisfecha o guardar valores idénticos. La configuración del cliente SQL puede informar cambios o coincidencias; esa configuración no se ha comprobado.

**Evidencia:** `M:index_archivos/tracking/HerramientasClass.php:L29-L47`; `M:index_archivos/tracking/TrackingNewClass.php:L1509-L1521`; `M:index_archivos/tracking/ListaViajesClass.php:L30-L36`.

**Obligación propuesta:** Definir resultados distintos para CHANGED, NOOP_CONFIRMED si la política lo permite, NOT_FOUND y rechazo de transición. Fijar qué cuenta el cliente SQL; combinar predicado autorizado y estado observado para distinguirlos. Si la política no permite no-op, devolver ese resultado específico sin inferir inexistencia.

**Deduplicación:** Mejora de reparación/contrato dentro de IDs existentes; no otro defecto OPS ni una política de idempotencia declarada AS-IS.

### RPR-IMP-002 · La reparación de pertenencia debe conservar IDs numéricos válidos recibidos como string

**Mejora TO-BE aceptada en pasada 8; no implementación o aprobación canónica.**

**Precisión:** Cambiar el if de array_search por pertenencia estricta al entero26 no reconoce '26', aunque representa el mismo ID y la búsqueda previa no estricta lo reconoce. Es una regresión de un caso exitoso de lectura, independiente de la posición o repetición.

**Condición:** La representación válida del ID de evento es int26 o string decimal'26'. El tipo concreto devuelto en el despliegue no se ha verificado; la fuente no normaliza antes de la búsqueda.

**Evidencia:** `M:index_archivos/tracking/ListaViajesClass.php:L166-L174`; `M:index_archivos/tracking/ListaViajesClass.php:L387-L409`.

**Obligación propuesta:** Comparar el resultado de búsqueda con false estrictamente sin cambiar la igualdad de valores, o validar y normalizar de forma explícita el tipo de ID antes de pertenencia estricta. Conservar int26 y '26'; no convertir indiscriminadamente entradas no numéricas como'26x'.

**Deduplicación:** Precisión de TO-BE de OPS-006/CLR-IMP-002, no nuevo hallazgo OPS ni confirmación de tipos o eventos reales.

## Revisión abstracta auxiliar anterior a BR4

La [pasada abstracta auxiliar](../reviews/iterative-20261118/closure-abstract-contracts.md), posterior a aceptar las dos RPR, completa 17 checks y 729 asignaciones lógicas de tipos/estados. No identifica otro mecanismo u omisión material dentro de los 17 registros conocidos. Es un resultado acotado sin delta adicional; no modifica las pasadas 6/8 positivas ni declara convergencia global.

## Última revisión semántica posterior a BR4

La [pasada de mutaciones documentales](../reviews/iterative-20261118/closure-semantic-mutations.md) revisa los 17 registros propios y las cuatro BR aceptadas como contexto externo: 21 checks y 70 mutaciones. No aporta nuevos hallazgos o mejoras dentro de ese alcance. Conserva el abstracto previo como auxiliar anterior a BR4, sin declarar convergencia global. La integración de las BR en variantes pertenece al otro agente; no se duplican en este registro.

## Uso y límites de este registro

**Regla general de uso propuesta — TO-BE, sin aprobación:** no interpretar success/code200, retorno de ID o redirección como confirmación de integridad hasta verificar el contrato de cada operación. Las correcciones, transacciones, validaciones y reglas de selección propuestas no se han implementado. OPS-008 amplía un pedido existente por edición; no es creación automática de cabecera del alta. OPS-009 afecta a mostrartabla, no al AJAX que pasa argumentos completos.

Se incorporan las precisiones IMP-T008 (resultados ignorados), IMP-T009 (timestamps/transiciones) e IMP-T010 (fechas). No duplican hallazgos. Se mantienen separados los riesgos genéricos ya documentados y las hipótesis sin DDL.

No se revisan salidas de navegador/navegación. Sin ejecución de rutas reales, acceso a BD/red, persistencia de sesión, cambios de fuente, commits o push. ❓ Las cuestiones pendientes del JSON limitan la validez del registro.

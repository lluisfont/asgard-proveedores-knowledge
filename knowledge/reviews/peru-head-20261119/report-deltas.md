# Revisión acotada Perú HEAD — reportes

19 de noviembre de 2026, Europe/Madrid; fecha proporcionada por el usuario. No canónico.

HEAD `2a179e2e6472d5705d031665ecbc90c3d806edec`; P95 `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62`; M histórico `a8ce2c23dead8552d2c4699e4a9b9134f7a18707`; KB `0c4bb99f076d6a8c18ae98375d6e154da6319922`.

Se registran **4 hallazgos nuevos de revisión**, **5 mejoras** y **1 duplicado/rechazado**. Solo el cruce de identidad por rol depende del cambio funcional nuevo; los demás defectos nuevos para la KB se heredan de P95. No significa cuatro regresiones introducidas en HEAD.

Validación: **36/36** comprobaciones de texto, predicados y relaciones sintéticas. [Resultados](../../../source-audits/peru/2026-11-19/report-probes.json) y [script](../../../scripts/audit/peru_head_report_probes.py). Ningún PHP, handler, include, SQL, DB, red o dato real ejecutado; sin emular despliegue. Sin revisión de salidas al navegador/navegación ni del nuevo master a44.

## Contrato y población

Cadena relevante: reporte → cnfdb105 (solo inspeccionado; depende de .env/autoload) → permisos → identidad/filtros; accion=ge incluye contador (ausente del árbol), después constructor query → data.php. El menú de Reportes usa grupo8 por cuenta y se incluye después de data.php; no demuestra autorización del handler. El constructor aislado no ejecuta SQL.

HEAD exige proveedor de cabecera; P95 exigía concesionario derivado. No basta con llamar transportista a la variable de sesión: el login la alimenta con idproveedor, incluido el dominio de tipo7. Los filtros opcionales acotan aliases existentes de base; fechas tiene una frontera de sintaxis sin protección. La cardinalidad y pertenencia de relaciones por chasis no quedan garantizadas por el filtro de cabecera.

SOURCE registra comportamiento; KNOWNDEFECT registra un defecto de fuente con precondiciones. RISK no afirma impacto productivo. TOBE propone una corrección o definición pendiente, sin aprobación ni modificación de aplicación.

## TEMP-PH001 — HEAD sustituye ámbito de concesionario por proveedor de cabecera

`improvement` · `SOURCE` · frente a P95: `changed`.

P95 exige tc.idconcesionario igual al ID de sesión; HEAD exige p.proveedor_id igual a un entero obtenido en el caller. No son predicados equivalentes: HEAD admite cabeceras propias sin concesionario y excluye cabeceras de otros proveedores aunque su concesionario coincida. El SELECT auxiliar de transportistas adopta el mismo proveedor. Los demás bloques del query son idénticos tras esa sustitución exacta.

**RISK:** La mejora de aislamiento de cabecera no acredita autorización de todos los roles ni de las relaciones anexas.

**TOBE:** Documentar separadamente identidad de proveedor y concesionario y su población autorizada antes de integrar el delta.

**Evidencia:** `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacional.php:L6-L9`; `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacional.php:L52-L59`; `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L381-L391`; `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/reportes/reportepreembarquenacionalquery.php:L381-L390`

**Pruebas:** RP-01, RP-02, RP-03, RP-04, RP-36.

**Límites:** Comprobación textual del blob fijado; no acredita ejecución ni accesibilidad. M carece de ambos reportes; no es una regresión respecto de un reporte M.

**Dedup:** Actualiza solo estos dos PHP respecto de P95; no audita el tercer JS ni reemplaza los documentos previos. Referencias: IMP-SCOPE-001; knowledge/variants/peru.md.

## TEMP-PH002 — El ID genérico de proveedor se usa como transportista sin discriminar tipo7

`new_finding` · `KNOWNDEFECT` · frente a P95: `changed_role_effect`.

El login guarda idproveedor en idtransportista junto con idtipoproveedor. UserFinder resuelve tipo7 contra cn_concesionario. El reporte no consulta el tipo ni permisos de módulo antes del query y HEAD aplica p.proveedor_id al mismo número para todos. Si una cuenta tipo7 alcanza esta ruta, pierde el ámbito de concesionario de P95 y puede coincidir con el número de un transportista distinto; el cast no resuelve ese cruce de dominios. El menú de Reportes obtiene enlaces del grupo8 por cuenta, pero no demuestra qué cuentas tienen este reporte.

**RISK:** Pérdida de filas o asociación con cabeceras de otro dominio si existen acceso efectivo y colisión numérica. No se afirma acceso real de tipo7 ni que deba conservarse una política concreta de P95.

**TOBE:** Definir roles admitidos y resolver el identificador con su dominio; denegar explícitamente roles no admitidos o aplicar el alcance de concesionario aprobado.

**Evidencia:** `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/veriflogin.php:L85-L91`; `2a179e2e6472d5705d031665ecbc90c3d806edec:src/core/users/application/Find/UserFind.php:L19-L35`; `2a179e2e6472d5705d031665ecbc90c3d806edec:src/core/users/application/Find/UserFind.php:L58-L63`; `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacional.php:L2-L9`; `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L328-L382`; `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/menu.php:L60-L67`

**Pruebas:** RP-05, RP-06, RP-30.

**Límites:** Acceso, catálogos de permisos, unicidad entre tablas e identidades reales sin verificar.

**Dedup:** El soporte previo de tipo7 y la guardia genérica no describen el efecto del nuevo predicado en este reporte; hallazgo nuevo de revisión, condicionado a acceso y dominio. Referencias: knowledge/variants/peru.md: País y perfiles; knowledge/general/actors-and-permissions.md; SEC-005.

## TEMP-PH003 — El filtro de fechas puede alterar el predicado que acota al proveedor

`new_finding` · `KNOWNDEFECT` · frente a P95: `inherited_P95_new_owner_boundary_consequence`.

POST fecha1/fecha2 se divide por '/' y concatena sin escape ni validación en BETWEEN. fechafiltro=1 y dos valores no vacíos habilitan el fragmento. Un segmento con comilla y OR sale del literal y entra después de p.proveedor_id y los otros AND, pudiendo convertirlos en una alternativa booleana. El cast de sesión protege solo su operando, no el WHERE completo. La cadena llega a data.php mediante query[0].

**RISK:** Lectura fuera del proveedor si el parser, runtime, conexión y acceso permiten la consulta alterada. Sin prueba de explotación, datos, privilegios, sentencias múltiples ni SQL ejecutado.

**TOBE:** Validar fechas completas con calendario y formato explícitos, enlazarlas como parámetros y mantener autorización en una consulta construida exclusivamente en servidor.

**Evidencia:** `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacional.php:L29-L40`; `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacional.php:L85-L87`; `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L45-L50`; `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L381-L391`; `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/data.php:L11-L14`

**Pruebas:** RP-08, RP-09, RP-10, RP-11, RP-12, RP-32.

**Límites:** Testigo de construcción y precedencia; no parser MySQL ni alcance anónimo demostrados.

**Dedup:** Misma familia de interpolación de SEC-006, nueva cadena concreta no cubierta por sus cuatro sinks; el inventario histórico solo marcaba RAW_SQL_SIGNAL. Se aporta el efecto sobre el límite de proveedor, sin contar otra vulnerabilidad genérica. Referencias: SEC-006; source-audits/api/api-deep-iterative/API_DEEP_ITERATIVE_FINDINGS.md: reportepreembarquenacional.

## TEMP-PH004 — Las relaciones por chasis pueden atravesar el alcance de cabecera

`new_finding` · `KNOWNDEFECT` · frente a P95: `inherited_P95`.

HEAD acota p, pero tmp_embarques y tmp_concesionario agrupan globalmente por chasis y mdos se enlaza solo por chasis. tmp_embarques toma MAX(embarque_id) sin deleted_at de pedido/detalle. El le externo no filtra deleted_at. Un VIN reutilizado puede aportar embarque, concesionario o movimiento local2 de otra relación y cambiar estadodos. COALESCE da prioridad a te sobre mdos y tc, aun cuando otra relación sea más pertinente. El filtro de embarque usa esa misma resolución. Esto no equivale a sustituir la cabecera p por otra.

**RISK:** Decoración o estado asociados al embarque equivocado si hay VIN compartidos/reutilizados o filas borradas que sigan candidatas; constraints efectivos desconocidos.

**TOBE:** Resolver relaciones con clave de preembarque/pedido/propietario autorizada, definir unicidad y borrados lógicos y rechazar ambigüedad en vez de elegir máximos globales.

**Evidencia:** `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L28-L30`; `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L166-L261`; `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L299-L310`; `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L364-L382`

**Pruebas:** RP-15, RP-16, RP-17, RP-18, RP-19, RP-34.

**Límites:** Sin DDL autorizado ni prueba de VIN duplicados. Los movimientos m/mtres sí conservan pre_embarque_id y tipo; no se generaliza el defecto a todas las CTE.

**Dedup:** El mapa histórico inventaría nombres de CTE, no su clave ni este contraejemplo. No duplicado del cruce de identidad de TEMP-PH002 ni de SQLi. Referencias: knowledge/variants/peru.md; source-audits/brownfield/reports/process_maps/components/8dc5c196467d.md.

## TEMP-PH005 — Los MAX independientes no conservan una fila coherente de embarque y viaje

`new_finding` · `KNOWNDEFECT` · frente a P95: `inherited_P95`.

Con te/tc sin embarque y mdos con dos embarques para el mismo chasis, base puede producir dos relaciones. La agregación final toma por separado MAX de embarque_id, fecha, numero_viaje y app_tracking; puede formar un registro que no perteneció a ninguna relación. tmp_viaje elige MAX(id) activo por embarque, no orden temporal. El MAX textual de app_tracking no demuestra el estado del viaje numéricamente máximo.

**RISK:** Asociación interna incoherente si base contiene varias relaciones por grupo; no depende de ataque ni de que falle SQL.

**TOBE:** Definir cuál relación gobierna el informe y seleccionar su fila completa con desempate explícito; no usar máximos independientes como sustituto de selección de fila.

**Evidencia:** `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L262-L269`; `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L310-L320`; `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L370-L380`; `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L393-L428`

**Pruebas:** RP-20, RP-21, RP-33.

**Límites:** Caso condicionado a multiplicidad; con una sola relación no hay mezcla. No se presupone orden de collation, equivalencia de ID con fecha o política del viaje correcto.

**Dedup:** TEMP-PH004 trata pertenencia; aquí incluso relaciones del mismo proveedor producen una tupla imposible por agregación. No se encontró este mecanismo en el registro previo. Referencias: TEMP-PH004; knowledge/general/operational-findings.json.

## TEMP-PH006 — Estado y tipo filtran la población antes del pivote de inventarios

`improvement` · `SOURCE` · frente a P95: `inherited_P95`.

Los aliases de filtros pertenecen a base. tipos_inventario aporta solo1/2; cualquier tipo positivo distinto genera cero filas, no selecciona el estado3 derivado. estado1/2 filtra presencia de m por fila de tipo antes de los MAX CASE: un vehículo con tipo1 pendiente y tipo2 realizado conserva solo la primera fila al pedir estado1, y la columna tipo2 queda NULL. El campo inventario3 se deriva de local2 o preembarque3, sin unificar esos dominios.

**RISK:** Una interpretación de filtros como selección de vehículo conservando todas sus columnas sería distinta de lo implementado; no se declara esa interpretación requisito aprobado.

**TOBE:** Documentar el alcance por fila/tipo; si negocio pide filtrar vehículos conservando inventarios, evaluar ese predicado después del pivote.

**Evidencia:** `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L33-L57`; `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L158-L174`; `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L299-L305`; `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L386-L387`; `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L411-L413`

**Pruebas:** RP-13, RP-14, RP-22, RP-23, RP-33, RP-35.

**Límites:** No se simulan controles del navegador ni se decide la política de filtros; un POST no numérico para IDs se ignora en vez de producir error.

**Dedup:** VAR-001 es contador/filtro del consumidor JS; este contrato SQL de tipos/población es distinto. Mejora de precisión, no nuevo defecto de completitud aprobado. Referencias: VAR-001; knowledge/variants/peru.md.

## TEMP-PH007 — Realizado significa existencia de un registro, no completitud demostrada

`improvement` · `SOURCE` · frente a P95: `inherited_P95`.

m une accesorios, partes, contaminaciones y parámetros activos con UNION por preembarque/chasis/tipo. Una sola fila de cualquiera basta para estado Realizado; no se exige cubrir todas las secciones ni ausencia de faltantes. estadodos usa presencia de local2 o preembarque3. Los flags de faltante/desperfecto/contaminación y kilometraje se calculan en base pero no forman parte de la proyección final. El nombre Nacional no añade por sí solo un predicado de tipo de viaje.

**RISK:** Sobreinterpretar el alias como inspección completa o universo nacional validado carece de respaldo en estos predicados.

**TOBE:** Mantener los alias como etiquetas de fuente y pedir definición de completitud/población antes de convertirlos en reglas de negocio.

**Evidencia:** `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L59-L164`; `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L288-L310`; `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L328-L391`; `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L393-L428`

**Pruebas:** RP-19, RP-24.

**Límites:** No se afirma que presencia sea una regla incorrecta; no hay contrato de completitud ni catálogo nacional validado.

**Dedup:** No reutiliza semántica del contador pendiente del JS ni promueve los nombres del SQL a glosario canónico. Referencias: VAR-001; knowledge/glossary/review-register.md.

## TEMP-PH008 — La cadena local no distingue todos los fallos del reporte

`improvement` · `SOURCE` · frente a P95: `inherited_except_aux_transportista_scope`.

cnfdb105 se incluye antes de permisos y depende de .env.php/autoload externos al árbol. Con accion=ge se incluye contador.php, ausente del árbol fijado. Los SELECT auxiliares de transportistas y destinos se intentan antes del include condicional del constructor; destinos conserva población global sin proveedor. No comprueban false antes de fetch. El constructor solo prepara query[0]; data.php ejecuta su principal sin comprobar el retorno antes de fetch, a diferencia de su rama auxiliar con die. No se atribuye divulgación al navegador ni continuación universal ante errores.

**RISK:** Fallo de conexión/include/query puede abortar o producir diagnósticos según runtime; no hay contrato de fallo de informe explícito ni prueba de que resultado vacío equivalga a consulta exitosa.

**TOBE:** Comprobar identidad antes de trabajo dependiente, revisar dependencias opcionales, acotar o retirar lecturas auxiliares innecesarias y distinguir fallo SQL de resultado vacío de forma terminal y controlada.

**Evidencia:** `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacional.php:L2-L3`; `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacional.php:L29-L87`; `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/cnfdb105.php:L2-L3`; `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/cnfdb105.php:L13-L24`; `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/data.php:L6-L14`

**Pruebas:** RP-25, RP-26, RP-27, RP-28, RP-31.

**Límites:** No se abren .env, vendor o datos reales. Dependencias/versiones/errores personalizados de despliegue desconocidos. No se presenta ausencia del árbol como fallo demostrado del despliegue. La divergencia La_Paz/Lima es heredada.

**Dedup:** Amplía el contrato local de ejecución/fallo; no repite el exportador SEC-015 ni afirma un nuevo fallo productivo. Referencias: RN-47; knowledge/general/architecture.md; knowledge/variants/peru.md.

## TEMP-PH009 — No recontar la guardia ni declarar que fallback0 deniega siempre

`duplicate_or_rejected` · `KNOWNDEFECT` · frente a P95: `guard_inherited_fallback_changed`.

La guardia compartida comprueba isset(idtransportista), sin rol/módulo ni terminación explícita. Su constante datoconservar mantiene el límite de runtime documentado en SEC-005. HEAD sustituye ausencia por0, pero igualdad con proveedor0 no es denegación incondicional: depende de que no existan esas filas. No se declara alcance anónimo, ejecución de handler ni denegación garantizada. La consulta del menú no añade retrospectivamente autorización al query ya construido/ejecutado.

**RISK:** Riesgo heredado y dependiente de runtime/datos; no nuevo hallazgo contabilizado.

**TOBE:** Reutilizar SEC-005 para corrección de guardia; requerir ID válido y denegación explícita antes del reporte y definir permisos de ruta en servidor.

**Evidencia:** `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/permisos.php:L1-L27`; `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacional.php:L2-L9`; `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacional.php:L85-L87`; `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacional.php:L221-L222`; `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/MenuClass.php:L25-L42`

**Pruebas:** RP-07, RP-29, RP-30.

**Límites:** No PHP ejecutado; no inferencia de bypass anónimo en PHP8 ni existencia de proveedor0.

**Dedup:** Duplicado del defecto compartido; se rechazan las generalizaciones sobre anonimato y fail-closed por0. Referencias: SEC-005; knowledge/general/actors-and-permissions.md.

## TEMP-PH010 — Corregir el candidato histórico: query.php es constructor, no ejecutor autónomo

`improvement` · `SOURCE` · frente a P95: `builder_inherited_new_context_variable`.

El catálogo histórico clasificó query.php como candidato public_php_page GET y no halló callers. La lectura completa del blob muestra construcción de filtros/query[0]/metadatos sin include, session_start ni mysql_query. El caller real es el reporte, bajo accion=ge, seguido de data.php. Sin ese contexto faltan identidad, filtros y conexión; no se concluye que una petición directa ejecute la consulta. Todos los aliases de los fragmentos sí existen en base; tampoco se acredita compilación SQL, soporte de CTE ni sintaxis de ejecución por esa comprobación.

**RISK:** Contar el constructor como endpoint SQL ejecutable sobrestima la superficie probada.

**TOBE:** Registrar la dependencia caller→constructor→data.php y mantener accesibilidad/runtime como no verificados.

**Evidencia:** `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L1-L52`; `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L430-L438`; `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacional.php:L85-L87`; `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/data.php:L11-L14`

**Pruebas:** RP-13, RP-28.

**Límites:** No petición directa, bootstrap, handler ni parser PHP/SQL ejecutados. Ninguna conclusión sobre salidas al navegador.

**Dedup:** Corrección del inventario histórico de candidatos, no nueva vulnerabilidad de acceso directo. Referencias: source-audits/api/asgard-api-audit-augmented/api-catalog.augmented.json: aug_ce1a5a0f133b5b07c241.

## Controles negativos y exclusiones

RP-04/06 conservan los casos de identidad correcta y muestran la diferencia de poblaciones. RP-07 impide equiparar fallback0 a denegación. RP-10/12 no generalizan el problema de fechas a filtros desactivados o a los cuatro valores escapados. RP-13/14 verifican aliases y guardas de ID; no compilan SQL. RP-18/19 separan VIN distinto y claves compuestas de las uniones débiles. RP-21 elimina la mezcla con relación única. RP-22/23 muestran la exclusión de tipo3 y el efecto del filtro previo al pivote. RP-28 rechaza ejecución SQL directa por el constructor. RP-29/30 deduplican guardia y separan permisos de menú del control de servidor. RP-32/33 vinculan testigos a las concatenaciones y agregados exactos. RP-34 conserva controles de soft-delete existentes; RP-35 muestra IDs inválidos sin atribuirles inyección; RP-36 demuestra que el filtro de nombre no reemplaza por sí solo el proveedor de sesión.

No se revisa exportador, transporte de SQL al navegador, renderizado, recursos de cliente ni navegación; SEC-015 permanece como antecedente fuera de esta revisión. No se ejecuta ninguna prueba histórica que invoque PHP. Los resultados no certifican soporte de CTE, versión MySQL/PHP, privilegios, datos, unicidad, política de completitud o despliegue.

Reproducir: `python scripts/audit/peru_head_report_probes.py --source C:/repos/proveedores-peru-head-review-20261119 --knowledge C:/repos/asgard-proveedores-knowledge`. Solo escribe los tres sidecars autorizados; no cambia fuente, manifest, documentos principales, commits ni ramas.

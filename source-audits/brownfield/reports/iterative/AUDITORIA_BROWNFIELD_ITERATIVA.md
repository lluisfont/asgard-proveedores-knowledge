# Auditoria Brownfield iterativa

Fecha: 2026-09-15

## Objetivo

Instalar y ejecutar `Brownfield-Refactor-Analyst` sobre el repositorio, usandolo dentro de un bucle de mejora iterativa de auditoria. Cada version debia aportar hallazgos nuevos, alternando tecnicas diferentes y combinadas, con foco especial en codigo y base de datos. El bucle se detuvo cuando dos versiones consecutivas dejaron de aportar familias nuevas de hallazgos.

## Instalacion y alcance

- Auditor instalado desde: https://github.com/lluisfont/Brownfield-Refactor-Analyst
- Instalacion Python editable: `brownfield-refactor-kit 0.2.3`
- Directorio de herramienta: `C:\Users\GMKtek-1\.codex\tools\Brownfield-Refactor-Analyst`
- Directorio auditado: `C:\repos\proveedores-master_peru`
- Configuracion Brownfield generada en: `.brownfield/`
- Archivo de instrucciones generado por el auditor: `AGENTS.md`

El primer `seed-baseline` intento cubrir todo el arbol y quedo dominado por dependencias pesadas y assets de terceros. Se reoriento el alcance a codigo propio y base de datos excluyendo carpetas como `vendor`, `PHPExcel`, `MPDF57`, `jqwidgets*`, `datatables*`, `spreadsjs`, `bootstrap4`, `fontawesome` y `graphify-out`.

## Resultados de ejecucion

### Brownfield baseline

- Archivos analizados: 1,505
- Tamano analizado: 42,539,773 bytes
- Hash fuente: `75060ae41c623868f78e9eeb5c7be8343dcd0196a395053e4199b3eb34897e15`
- Hash base de datos: `ef3b8233e4b210cabbb5217f83a42e5456dc4a81d4918f45fa5e72278d8a5baf`
- Evidencias extraidas: 4,471
- Evidencias por tipo:
  - `sql_query`: 4,119
  - `secret_candidate`: 182
  - `state_transition`: 123
  - `transaction`: 40
  - `permission`: 7

### Diccionario de datos

- SQL files: 1
- Tablas: 1,055
- Columnas: 10,111
- Relaciones: 66
- Indices: 1,365
- Constraints: 819
- Objetos de base de datos: 96
- Objetos por tipo:
  - Procedures: 54
  - Functions: 42

### Mapa de procesos

- Rutas HTTP detectadas por Brownfield: 0
- Candidatos no HTTP: 48
- Componentes: 66
- Nodos: 530
- Aristas: 4,178

### Estado

- `verify-state`: valido
- Bloqueos: 0
- Baseline confirmado: false
- Estado de completitud: `INCOMPLETE_BASELINE`
- Cobertura deterministica: 11.62%
- Artefactos deterministas generados: 33
- Artefactos requeridos por release: 323

### Paquete

Checkpoint generado:

`.brownfield/releases/brownfield_checkpoint_20260915_141659_932337Z.zip`

## Bucle iterativo

### Version 1: instalacion, inventario y baseline

Tecnica: instalacion del auditor, verificacion de configuracion, inventario de fuentes, extraccion deterministica.

Hallazgos nuevos:

- El repositorio requiere recorte de alcance para auditar codigo propio. Sin exclusiones, el auditor queda consumido por librerias y assets de terceros.
- El codigo propio y el dump SQL reducidos aun producen 4,471 evidencias utiles.
- La base de datos domina la evidencia: `asgardpe Base de Datos Peru.sql` concentra 3,357 evidencias.
- Hay 96 objetos de BD entre procedures y functions, por lo que la auditoria no puede limitarse a PHP: la logica de negocio vive tambien en SQL.

### Version 2: reconstruccion semantica y Graphify

Tecnica: `semantic-reconstruct` combinado con importacion de `graphify-out`.

Hallazgos nuevos:

- Brownfield importo 3 artefactos de Graphify: `GRAPH_REPORT.md`, `graph.json` y `graph.html`.
- El grafo previo queda vinculado al paquete Brownfield, permitiendo cruzar estructura de codigo con diccionario y flujo semantico.
- La reconstruccion semantica genero 891 terminos de glosario.
- El resumen semantico encontro 595 cruces flujo-tabla y 10,463 cruces flujo-campo.

### Version 3: cruces proceso-tabla

Tecnica: analisis de `process_edges.csv` y matrices de flujo.

Hallazgos nuevos:

- Los componentes con mas escrituras son:
  - `index_archivos/tracking/TrackingClass.php`: 21
  - `index_archivos/tracking/TrackingNewClass.php`: 18
  - `index_archivos/embarques/CotizacionClass.php`: 15
  - `index_archivos/tracking/controllers/CargaMasiva.php`: 13
  - `index_archivos/reportes/exportaciones/ajax/ActualizarMICs.php`: 8
- Las tablas mas escritas por codigo propio incluyen:
  - `tck_asignacion_viaje`: 8
  - `tck_localizaciones`: 6
  - `tck_transportista`: 5
  - `tck_tmpcargamasiva`: 5
  - `tck_items_localizaciones`: 5
  - `tck_documentossoporte`: 5
  - `logis_embarquesoperador`: 5
- El riesgo operativo se concentra en tracking, carga masiva, cotizaciones, embarques y reset password.

### Version 4: sensibilidad de datos y privacidad

Tecnica: busqueda por patrones en `columns.csv` sobre nombres de columnas sensibles.

Hallazgos nuevos:

- Brownfield dejo el 100% de columnas con `sensitivity = UNKNOWN`.
- Aun asi, por nombres aparecen campos evidentemente sensibles: `token`, `pass`, `password`, `contrasena`, `correo`, `email`, `mail`, `telefono`, `celular`, `nit`, `username`, `usuario`, `ip`, `codigo`.
- Tablas con mayor densidad de campos sensibles por nombre:
  - `dav_casos`: 181
  - `dav_partidas`: 78
  - `dav_dav`: 67
  - `dav_damitems`: 65
  - `dav_davvehiculos`: 63
  - `dav_casos_copy`: 63
  - `tmp_regularizacion`: 48
  - `dav_facturaplanilla`: 32
  - `rnc_noconformidad`: 30
  - `rnc_mejoras_continuas`: 22
- Tablas criticas con datos o flujo sensible:
  - `prov_usuarioaccesoproveedor`
  - `dav_codigos_2fa`
  - `dav_reseteos_passswords_proveedores`
  - `master_pass`
  - `tck_location`
  - `tck_asignacion_viaje`

### Version 5: cobertura y tablas no usadas

Tecnica: contraste de `tables.csv`, uso detectado y relaciones declaradas.

Hallazgos nuevos:

- Tablas con uso detectado: 536
- Tablas sin uso detectado: 519
- La mitad aproximada del modelo SQL no aparece referenciada por el codigo escaneado. Esto puede significar tablas legacy, tablas usadas por jobs externos, cobertura incompleta o rutas PHP no clasificadas.
- Solo hay 66 relaciones declaradas para 1,055 tablas.
- Politicas de borrado detectadas:
  - `RESTRICT`: 65
  - `CASCADE`: 1
- Las tablas de autenticacion, 2FA, reset y tracking no quedan suficientemente cubiertas por relaciones formales segun la evidencia extraida.

### Version 6: deteccion de endpoints y artefactos candidatos

Tecnica: revision de `HTTP_ENDPOINT_CATALOG.md`, `ROUTE_TO_HANDLER_MATRIX.csv`, security findings y registros de hallazgos generados.

Hallazgos nuevos:

- Brownfield detecto `Route declarations: 0` y `Unique route identities: 0`, aunque el repositorio contiene muchos endpoints PHP directos y AJAX.
- El mapa de procesos clasifica candidatos como no HTTP, lo que indica una limitacion del auditor frente al patron de enrutado por archivos PHP.
- Muchos artefactos de release existen como plantillas `INFERRED_DRAFT_REVIEW_REQUIRED`, no como hallazgos completados.
- `SECURITY_FINDINGS.md`, `PERSONAL_DATA_INVENTORY.md`, `ORPHAN_TABLES_AND_COLUMNS.md`, `TECHNICAL_DEBT_REGISTER.md` y `ARCHITECTURE_RISKS.md` quedaron como slots candidatos. Se deben rellenar con evidencia del codigo y no tratar como conclusiones cerradas.

### Version 7: verificacion de estado

Tecnica: `verify-state`, `status`, `completeness-report`.

Hallazgos nuevos:

- No aparecen nuevas familias de hallazgos.
- El estado es consistente, valido y sin bloqueos, pero no confirmado.
- La siguiente accion del auditor queda como `review_seed_baseline_then_reconstruct_business_domains`.
- La cobertura sigue en 11.62%, sin aumentar respecto a la reconstruccion semantica.

### Version 8: empaquetado y repeticion de contraste

Tecnica: `package` y contraste final contra los artefactos ya generados.

Hallazgos nuevos:

- No aparecen nuevas familias de hallazgos.
- El paquete reproduce el mismo estado analitico: baseline valido, incompleto y pendiente de validacion humana.
- El bucle inicial parecia convergido, pero se reabrio por una correccion solicitada: Brownfield marcaba `0` rutas HTTP aunque el sistema usa PHP directo y AJAX.

### Version 9: correccion de endpoints PHP directos

Tecnica: scanner deterministico propio sobre PHP, superglobals, salidas JSON/header, rutas bajo `ajax`, includes, senales de sesion/autorizacion, senales CSRF, uploads/downloads y escrituras SQL importadas desde `process_edges.csv`.

Hallazgos nuevos:

- Se corrigio el falso `0` de Brownfield: se detectaron 246 candidatos de endpoint PHP directo.
- Clasificacion de fuerza:
  - `strong_ajax_endpoint`: 96
  - `strong_direct_endpoint`: 70
  - `strong_page_endpoint`: 3
  - `public_php_page_candidate`: 69
  - `public_php_logic_candidate`: 8
- Grupos con mas endpoints:
  - `embarques`: 82
  - `tracking`: 74
  - `index_archivos`: 22
  - `reportes`: 17
  - `parametros`: 15
- Se actualizaron los artefactos Brownfield:
  - `.brownfield/work/release/engineering-analysis/interfaces/HTTP_ENDPOINT_CATALOG.md`
  - `.brownfield/work/release/engineering-analysis/interfaces/ROUTE_TO_HANDLER_MATRIX.csv`

### Version 10: riesgo HTTP + base de datos

Tecnica: cruce del endpoint catalog corregido con tablas escritas por codigo propio.

Hallazgos nuevos:

- Endpoints POST/REQUEST sin senal local de CSRF: 74
- Endpoints que escriben BD sin senal local de CSRF: 7
- Upload/import endpoints: 50
- JSON endpoints: 127
- Endpoints sin evidencia local de auth/sesion: 70
- Endpoints con escritura BD y mayor prioridad de revision:
  - `/index_archivos/reportes/exportaciones/ajax/ActualizarMICs.php` escribe `dex_suma`
  - `/index_archivos/tracking/ajax/borrarempresa.php` escribe `tck_operadorestransporte`
  - `/index_archivos/tracking/ajaxAsignacion/borrar_ubicacion.php` escribe `tck_location`
  - `/index_archivos/resetpassword/ResetPassword.php` escribe `dav_reseteos_passswords_proveedores` y `prov_usuarioaccesoproveedor`
  - `/index_archivos/embarques/EmbarqueClass.php` escribe `logis_embarques`, `logis_embarquesdocumentos`, `logis_embarquesrutas`
  - `/index_archivos/embarques/CotizacionClass.php` escribe multiples tablas `logis_*`
  - `/index_archivos/tracking/TrackingNewClass.php` escribe multiples tablas `tck_*` y `logis_edp`

### Version 11: callers frontend/PHP

Tecnica: analisis de llamadas `url:`, `$.post`, `$.get`, `fetch`, `.load` y `form action` que apuntan a PHP.

Hallazgos nuevos:

- Referencias frontend/PHP hacia PHP: 91
- Endpoints del catalogo con referencias de caller: 56
- Referencias PHP no resueltas contra endpoints escaneados: 16
- Rutas invocadas pero no encontradas como archivo PHP actual:
  - `ajax/subirArchivos.php`
  - `ajax/guardarOpeTrans.php`
  - `ajax/duplicarCotizacion.php`
  - `cotizacionEditarController.php`
  - `despachoajax.php`
  - `exportaciones/ajax/filtros.php`
- `exportaciones/ajax/filtros.php` aparece repetido desde `index_archivos/reportes/exportaciones/js/formulario-filtros.js`, pero en el arbol solo existen `ActualizarMICs.php` y `RecepcionFisicaMICs.php` bajo esa carpeta AJAX.

### Version 12: repeticion y convergencia de la correccion

Tecnica: rerun del scanner corregido, `verify-state`, `completeness-report` y comparacion de hashes de artefactos custom.

Hallazgos nuevos:

- No aparecen nuevas familias de hallazgos.
- Los conteos se mantienen estables:
  - endpoints: 246
  - caller references: 91
  - endpoints con callers: 56
  - caller references no resueltas: 16
- Hashes estables de artefactos generados:
  - `http_endpoint_catalog.csv`: `4DFD2BCAFA9FAD18965B2D4B1BF3D593020C87936C9A435B4A2B3567977423A2`
  - `frontend_endpoint_callers.csv`: `7FFEBB87BB8E81B6755578324FE0A4B040A49448521E215D9947DADBA89B555A`
  - `unmatched_php_callers.csv`: `7F1AAC598F0E290F18DEE069089C4660511BC17A1B0B50F6F2CCF745854D3817`
- Se cumple de nuevo la condicion de parada para esta correccion: el rerun no aporta nuevos hallazgos y Brownfield mantiene el baseline valido sin bloqueos.

### Version 13: SQL taint, uploads y sinks peligrosos

Tecnica: scanner heuristico propio sobre PHP, buscando flujo local desde `$_GET`, `$_POST`, `$_REQUEST`, `$_FILES` y `$_COOKIE` hacia SQL, uploads, `unserialize`, `shell_exec`, includes dinamicos y uso de API MySQL legacy.

Hallazgos nuevos:

- SQL sink findings: 539
- Usos de API `mysql_*` legacy: 493
- SQL tainted por superglobals o variables derivadas: 46
- Archivos con manejo de upload propio: 19
- Sinks PHP peligrosos propios: 3
- Sinks peligrosos concretos:
  - `index_archivos/js/formulariosxls.php:13`: `unserialize` con `GET.consulta` y `GET.datos`
  - `index_archivos/tracking/generar_excel.php:8`: `unserialize` con `GET.id` y `GET.data`
  - `index_archivos/logAsgard.php:55`: `shell_exec`
- Ejemplos de SQL tainted prioritarios:
  - `index_archivos/embarques/ajax/listaRutas.php:18` con `REQUEST.idembarque`
  - `index_archivos/reportes/exportaciones/ajax/ActualizarMICs.php:40` y `:72`
  - `index_archivos/reportes/exportaciones/ajax/RecepcionFisicaMICs.php:73`
  - `index_archivos/tracking/ajax/borrarempresa.php:8` con `POST.id`
  - `index_archivos/tracking/ajaxAsignacion/borrar_ubicacion.php:13` con `POST.id`
  - `index_archivos/reporteexcel/reporteexcelNew.php:11` acepta `POST.query`, `POST.datos`, `POST.posiciones`, `POST.formatos` y `POST.cabecera`

### Version 14: seguridad de uploads

Tecnica: inspeccion de `$_FILES`, `move_uploaded_file`, `copy`, uso de nombre cliente, checks de extension, MIME, tamano, CSRF y auth local.

Hallazgos nuevos:

- Archivos de upload sin senal local de CSRF: 19
- Sin senal de allowlist de extension: 18
- Sin senal de limite de tamano: 18
- Sin senal de verificacion MIME: 16
- Uso de nombre de archivo cliente sin senal de aleatorizacion: 8
- Uso de `copy` para uploads: 4
- Sin senal local de auth: 1
- Hotspots de upload:
  - `index_archivos/cargarlibroventas_ajax.php`
  - `index_archivos/tracking/ajax/guardarunidadtransporte.php`
  - `index_archivos/tracking/ajax/guardartransportista.php`
  - `index_archivos/tracking/ajax/guardardocumentoempresatransporte.php`
  - `index_archivos/tracking/ajax/cargar-imagenes-viaje.php`
  - `index_archivos/parametros/clientes/ajax/cargar-excel-clientes-proveedores.php`
  - `index_archivos/parametros/ubicaciones/ajax/uploadexcel.php`
  - `index_archivos/versolicituddetalle.php`

### Version 15: routines SQL y transacciones

Tecnica: parser de dump SQL para procedures/functions con `CONCAT`, `PREPARE`, `EXECUTE`, tablas temporales, SQL destructivo y transacciones explicitas.

Hallazgos nuevos:

- Routines SQL con senales de riesgo: 56
- Routines con tablas temporales: 41
- Routines con concatenacion SQL/string building: 34
- Routines con SQL destructivo: 24
- Routines con SQL dinamico `PREPARE/EXECUTE`: 2
- Routines con transacciones explicitas: 2
- Routines mas relevantes:
  - `saldos_clientes`: `DYNAMIC_SQL`, `SQL_STRING_CONCAT`, `TEMP_TABLE`
  - `sp_carpetas_procesada_oficial`: `DYNAMIC_SQL`, `SQL_STRING_CONCAT`
  - `sp_delete_trip`: `EXPLICIT_TRANSACTION`
  - `tck_duplicar_viaje`: `EXPLICIT_TRANSACTION`
  - multiples `DashBoard*` combinan `DESTRUCTIVE_SQL`, `SQL_STRING_CONCAT` y `TEMP_TABLE`

### Version 16: integridad del modelo de datos

Tecnica: analisis de `columns.csv`, `tables.csv`, `indexes.csv` y `relations.csv` de Brownfield para sensibilidad, FK-like columns, indices y tablas temporales/copia.

Hallazgos nuevos:

- Columnas con nombre sensible: 1,119
- Columnas tipo FK sin relacion declarada: 2,509
- Columnas tipo FK sin relacion declarada en tablas `USED`: 1,310
- Findings de tabla: 844
- Tablas criticas sin relaciones declaradas: 6
- Flags de campos sensibles:
  - `SENSITIVITY_UNKNOWN`: 1,119
  - `SENSITIVE_FIELD_NULLABLE`: 939
  - `NO_INDEX_ON_AUTH_OR_TOKEN_FIELD`: 191
- Tablas criticas sin relaciones declaradas:
  - `dav_codigos_2fa`
  - `dav_reseteos_passswords_proveedores`
  - `master_pass`
  - `prov_usuarioaccesoproveedor`
  - `tck_asignacion_viaje`
  - `tck_location`
- Tablas con mayor densidad de columnas sensibles:
  - `dav_casos`: 50
  - `dav_partidas`: 19
  - `dav_davvehiculos`: 18
  - `dav_dav`: 17
  - `dav_damitems`: 15
  - `dav_ciudad`: 13
  - `dav_facturaplanilla`: 13

### Version 17: lint PHP 8.4

Tecnica: `php -l` con PHP 8.4 sobre PHP propio, excluyendo librerias de terceros embebidas.

Hallazgos nuevos:

- Errores de parseo PHP 8.4 en codigo propio: 3
- Archivos afectados:
  - `index_archivos/tracking/documentosempresatransporte.php:37`
  - `index_archivos/embarques/componentes/cotizaciones/local/terrestre.php:57`
  - `index_archivos/embarques/componentes/cotizaciones/local/ferreo.php:57`
- Causa comun: ternarios anidados sin parentesis, no soportados por PHP 8+.

### Version 18: rerun completo de scanners custom

Tecnica: repeticion de `php_endpoint_scanner.py`, `deep_security_scanner.py`, `db_integrity_scanner.py` y `verify-state`.

Hallazgos nuevos:

- No aparecen nuevas familias de hallazgos.
- Conteos estables:
  - endpoints: 246
  - caller references PHP: 91
  - SQL sink findings: 539
  - upload findings: 19
  - dangerous PHP sink findings: 3
  - SQL routine risk findings: 56
  - sensitive-name columns: 1,119
  - FK-like columns without declared relation: 2,509
- Brownfield sigue valido, sin blockers, con baseline pendiente de confirmacion.

### Version 19: hashes finales y convergencia

Tecnica: comparacion hash SHA256 de salidas custom tras rerun.

Hallazgos nuevos:

- No aparecen nuevas familias de hallazgos.
- Se cumple la condicion de parada global: dos versiones consecutivas no aportaron nuevos hallazgos de fondo.
- Hashes finales:
  - `http_endpoint_catalog.csv`: `4DFD2BCAFA9FAD18965B2D4B1BF3D593020C87936C9A435B4A2B3567977423A2`
  - `frontend_endpoint_callers.csv`: `7FFEBB87BB8E81B6755578324FE0A4B040A49448521E215D9947DADBA89B555A`
  - `unmatched_php_callers.csv`: `7F1AAC598F0E290F18DEE069089C4660511BC17A1B0B50F6F2CCF745854D3817`
  - `sql_taint_findings.csv`: `67B454A2C7F835ACB25D3D5ED336BDA93557C447487F99346E77EA6FBA944264`
  - `upload_security_findings.csv`: `D3393D3CFBA60497D19C8F3B0093018F75452F6CA23F1A89F088279E56FC2824`
  - `dangerous_php_sinks.csv`: `AE8698C141F86FFEE6DA44E0CC65700C80975918A60E8D17E0E696D379363A74`
  - `sql_routine_risks.csv`: `C147B866DFE24991068841D4FAB2014C1E5F6EE1129513D536998915428AB1B2`
  - `sensitive_column_findings.csv`: `680F7EE4D5422A828CF506C2FC80FF06A10F60CE90DE3769675F0810253131A1`
  - `fk_gap_findings.csv`: `585800B2594C8B74D1236E6706C7B63148447A61D59D006836DE96101769FA77`
  - `table_integrity_findings.csv`: `2682C4518B93C3A243FA48730C7DCA2EE732D7621124865B1A7CCC01DC531CF4`
  - `php_lint_errors.json`: `6FC34A48DAEBA7EFE6B48A62932794A20F7BC9FD3A51B6BBA4B6D1B4CE5E693F`

## Conclusiones principales

- Brownfield quedo instalado y ejecutado correctamente.
- El valor principal de Brownfield en este repo esta en el inventario, diccionario SQL, evidencias, matrices de proceso-dato y empaquetado reproducible.
- El falso `0` de rutas HTTP de Brownfield fue corregido con un scanner deterministico: ahora hay un catalogo de 246 endpoints PHP/AJAX candidatos.
- El auditor no debe usarse solo para seguridad: sus archivos de hallazgos de seguridad quedaron como plantillas y requieren relleno manual basado en evidencia.
- La auditoria de codigo debe combinar Brownfield, Graphify, busqueda estatica, Semgrep/PHPStan y revision manual de endpoints PHP.
- La base de datos es una parte critica de la aplicacion: 1,055 tablas, 10,111 columnas y 96 routines obligan a auditar SQL como logica de negocio.
- El mayor riesgo nuevo detectado por Brownfield es de cobertura y trazabilidad: muchas tablas sin uso detectado, pocas relaciones formales, sensibilidad no clasificada y rutas HTTP no reconocidas.
- Los scanners custom anaden hallazgos ejecutables de seguridad: SQL tainted, uploads sin controles visibles, sinks peligrosos, routines SQL con SQL dinamico/temporal/destructivo y errores de parseo PHP 8.4.

## Artefactos clave

- `.brownfield/work/evidence/evidence.jsonl`
- `.brownfield/work/data_dictionary/DATA_DICTIONARY.md`
- `.brownfield/work/data_dictionary/columns.csv`
- `.brownfield/work/data_dictionary/tables.csv`
- `.brownfield/work/data_dictionary/database_objects.csv`
- `.brownfield/work/process_maps/PROCESS_MAP.md`
- `.brownfield/work/process_maps/process_edges.csv`
- `.brownfield/work/semantic_flow_analysis/FLOW_TABLE_USAGE_MATRIX.csv`
- `.brownfield/work/semantic_flow_analysis/FLOW_FIELD_USAGE_MATRIX.csv`
- `.brownfield/work/custom/http_endpoint_catalog.csv`
- `.brownfield/work/custom/frontend_endpoint_callers.csv`
- `.brownfield/work/custom/unmatched_php_callers.csv`
- `.brownfield/work/custom/HTTP_ENDPOINT_CATALOG_AUGMENTED.md`
- `.brownfield/work/custom/ENDPOINT_FINDINGS_AUGMENTED.md`
- `.brownfield/work/custom/DEEP_SECURITY_FINDINGS.md`
- `.brownfield/work/custom/sql_taint_findings.csv`
- `.brownfield/work/custom/upload_security_findings.csv`
- `.brownfield/work/custom/dangerous_php_sinks.csv`
- `.brownfield/work/custom/sql_routine_risks.csv`
- `.brownfield/work/custom/DATA_MODEL_INTEGRITY_FINDINGS.md`
- `.brownfield/work/custom/sensitive_column_findings.csv`
- `.brownfield/work/custom/fk_gap_findings.csv`
- `.brownfield/work/custom/table_integrity_findings.csv`
- `.brownfield/work/custom/php_lint_errors.json`
- `.brownfield/work/completeness/ANALYSIS_COMPLETENESS_REPORT.md`
- `.brownfield/work/graphify/GRAPHIFY_IMPORT.md`
- `.brownfield/releases/brownfield_checkpoint_20260915_141659_932337Z.zip`

## Recomendacion inmediata

Rellenar los artefactos candidatos de seguridad, datos personales y arquitectura con evidencia directa del codigo, usando como semillas los hotspots encontrados:

- `index_archivos/tracking/TrackingClass.php`
- `index_archivos/tracking/TrackingNewClass.php`
- `index_archivos/tracking/controllers/CargaMasiva.php`
- `index_archivos/embarques/CotizacionClass.php`
- `index_archivos/embarques/EmbarqueClass.php`
- `index_archivos/resetpassword/ResetPassword.php`
- `asgardpe Base de Datos Peru.sql`

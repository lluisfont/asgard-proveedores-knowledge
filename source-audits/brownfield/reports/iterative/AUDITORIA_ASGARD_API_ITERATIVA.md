# Auditoria Asgard API iterativa

Fecha: 2026-09-15

## Objetivo

Instalar y ejecutar `asgard-api-auditor` sobre este repositorio y usarlo dentro de un bucle de mejora iterativa. Cada version de la auditoria debia aportar hallazgos nuevos mediante tecnicas distintas o combinadas, con foco en codigo, APIs y base de datos. El bucle se detuvo cuando dos pasadas consecutivas no generaron nuevas familias de hallazgos.

## Instalacion

- Auditor instalado desde: https://github.com/lluisfont/asgard-api-auditor
- Version ejecutada: `asgard-api-auditor 0.8.0`
- Directorio de herramienta: `C:\Users\GMKtek-1\.codex\tools\asgard-api-auditor`
- Instalacion: `python -m pip install -e C:\Users\GMKtek-1\.codex\tools\asgard-api-auditor`
- Repositorio auditado: `C:\repos\proveedores-master_peru`

El auditor nativo exige un repositorio Git con `HEAD`. Como este directorio no tiene `.git`, se creo una copia temporal de solo auditoria en `C:\Users\GMKtek-1\.codex\work\asgard-api-audit-target-20260915`, se inicializo Git alli y se audito el commit temporal `f4f6d607c39d5b911b2f6e1dbf98c9658d5b3f4a`. No se convirtio ni reescribio el repositorio original.

## Artefactos generados

- Auditoria nativa v1: `.brownfield/work/custom/asgard-api-audit/`
- Auditoria nativa v2, con exclusiones de vendors/assets: `.brownfield/work/custom/asgard-api-audit-v2/`
- Catalogo aumentado: `.brownfield/work/custom/asgard-api-audit-augmented/api-catalog.augmented.json`
- CSV de APIs consumidas: `.brownfield/work/custom/asgard-api-audit-augmented/consumed_api_augmented.csv`
- Matriz endpoint-seguridad-BD: `.brownfield/work/custom/asgard-api-audit-augmented/api_endpoint_security_matrix.csv`
- OpenAPI provisional: `.brownfield/work/custom/asgard-api-audit-augmented/openapi.augmented.yaml`
- Script reproducible de aumento: `.brownfield/custom_tools/asgard_api_augmentation.py`
- Informe aumentado: `.brownfield/work/custom/asgard-api-audit-augmented/ASGARD_API_AUDIT_AUGMENTED.md`
- Scanner profundo iterativo: `.brownfield/custom_tools/api_iterative_deep_audit.py`
- Riesgos profundos por endpoint: `.brownfield/work/custom/api-deep-iterative/endpoint_deep_risks.csv`
- Riesgos profundos por consumidor: `.brownfield/work/custom/api-deep-iterative/consumer_deep_risks.csv`
- Informe profundo iterativo: `.brownfield/work/custom/api-deep-iterative/API_DEEP_ITERATIVE_FINDINGS.md`
- Checkpoints empaquetados: `.brownfield/releases/`

Hashes SHA256 de artefactos principales:

| Artefacto | SHA256 |
| --- | --- |
| `asgard-api-audit-v2/findings.json` | `7F4A1E0E35273625AA0C2612DD4F06CD154994287DC0925082867D16F4557CEA` |
| `api-catalog.augmented.json` | `BEEFBB749CD9B04DD9CDD8DA34D76F7D5992F153A3BB1C37EDC0E5D66247C61F` |
| `consumed_api_augmented.csv` | `3240132B91DBEF8BBCCC0EAE3FDA46061A3D4FD735C59FA36C76D55A6BE30CA8` |
| `api_endpoint_security_matrix.csv` | `F2CD4BA51B62D80F5F3C081316BD7563A8A39C000FA0EC347ADC47227DD49372` |
| `api-deep-iterative/endpoint_deep_risks.csv` | `90EECF6C632E0E5B8AD2905B0A12B930BA712D5BB2F5ACF15FD76A356AB51EF9` |
| `api-deep-iterative/consumer_deep_risks.csv` | `6A466AB181C61BB981BAF28CD4BE401A3D774AAC6369AF010FBCEFF263F77BC6` |

## Bucle iterativo

### Version 1: Asgard nativo sobre copia Git

Tecnica: `inventory`, `discover`, `audit` y `catalog-api` con el motor original.

Hallazgos nuevos:

- Resultado nativo `PARTIAL`.
- Endpoints expuestos detectados: `0`.
- Endpoints consumidos detectados: `2`.
- Asgard detecto clientes HTTP `fetch`, `guzzle` y `php-curl`, pero dejo multiples bloqueos por llamadas dinamicas/complejas.
- La herramienta no reconoce la arquitectura principal del repo: endpoints PHP directos y AJAX file-routed.

### Version 2: Asgard nativo con alcance depurado

Tecnica: reejecucion excluyendo vendors, JS minificado y librerias pesadas para separar codigo propio de ruido.

Hallazgos nuevos:

- Los bloqueos bajaron de `23` a `1`.
- El unico bloqueo restante fue `http_client_detected_no_calls` para Guzzle.
- El catalogo siguio en `0 exposed / 2 consumed`, confirmando que el problema no era solo ruido de vendors, sino limitacion del detector frente a PHP legacy sin Slim/Laravel.

### Version 3: Analisis manual dirigido por el bloqueo Guzzle

Tecnica: busqueda especifica de `GuzzleHttp\Client`, `createRequest`, constantes de URL y opciones de transporte.

Hallazgos nuevos:

- Asgard no capturo `POST URL_API.'enviar-whatsapp'` en `index_archivos/tracking/TrackingNewClass.php:971`.
- Esa llamada usa `verify => false` en `index_archivos/tracking/TrackingNewClass.php:972` y envia `Authorization` desde `$_SESSION['tokenJWT']` en `index_archivos/tracking/TrackingNewClass.php:976`.
- Asgard tampoco capturo `POST TRACKING_URL.'/event/journey'` en `index_archivos/tracking/ListaViajesClass.php:205-207`, tambien con `verify => false`.
- `URL_API` y `TRACKING_URL` aparecen usadas pero no estan definidas en `.env-example.php`; el despliegue depende de configuracion no documentada en el ejemplo.

### Version 4: Correccion del falso `0 endpoints`

Tecnica: aumentar Asgard con el catalogo deterministico PHP/AJAX generado previamente.

Hallazgos nuevos:

- Endpoints PHP/AJAX candidatos: `246`.
- Por fuerza de evidencia: `96` `strong_ajax_endpoint`, `70` `strong_direct_endpoint`, `3` `strong_page_endpoint`, `69` `public_php_page_candidate` y `8` `public_php_logic_candidate`.
- Endpoints con referencias desde frontend/PHP: `56`.
- Referencias a endpoints PHP no casadas contra handler local: `16`.
- Grupos con mayor superficie: `embarques` con `82`, `tracking` con `74`, `reportes` con `17` y `parametros` con `15`.

### Version 5: Matriz API-seguridad-BD

Tecnica: cruce de endpoints con metodos HTTP, señales CSRF, escrituras SQL y llamadas desde frontend.

Hallazgos nuevos:

- Endpoints `POST` o `REQUEST` sin senal local de CSRF: `74`.
- Endpoints con escritura a BD sin senal local de CSRF: `7`.
- Endpoints activos con caller y escritura a BD: `2`.
- Endpoint activo `POST|GET` que escribe `dex_suma`: `/index_archivos/reportes/exportaciones/ajax/ActualizarMICs.php`.
- Endpoint activo `POST` que escribe `tck_operadorestransporte`: `/index_archivos/tracking/ajax/borrarempresa.php`.

### Version 6: APIs consumidas aumentadas

Tecnica: resolucion de URLs literales, constantes PHP, `<?=CONST?>`, `<?php echo CONST ?>`, cURL, `fetch` y `createRequest`.

Hallazgos nuevos:

- Contratos consumidos auditables tras filtrado de ruido: `23`.
- Contratos con base no resuelta: `10`.
- Contratos o llamadas con clave/token/autorizacion en contexto: `12`.
- Contratos por HTTP plano: `3`.
- Contratos con TLS verification desactivada: `3`.
- SendGrid se usa desde dos rutas de codigo: `index_archivos/MailClass.php:84` e `index_archivos/embarques/EmbarqueClass.php:558`.
- Google Maps se usa con API key en llamadas JS y script tags.
- `DOCUMENTS_API` en `.env-example.php:23` esta en `http://api-documents-dev.kpogroup.bo`, mientras `DOCUMENTS_API_SECURE` en `.env-example.php:24` existe pero convive con la variante insegura.

### Version 7: Secretos y configuracion de integraciones

Tecnica: cruce de constantes de entorno, headers de APIs externas y sinks cURL/Guzzle.

Hallazgos nuevos:

- Credenciales de base de datos en `.env-example.php:8-11`, incluyendo host IP, usuario `root` y password en claro.
- `GOOGLE_MAP_KEY` en `.env-example.php:14`.
- `PUSHER_SECRET` en `.env-example.php:19`.
- Token SendGrid hardcoded en `index_archivos/cnfdb105.php:7`.
- Headers SendGrid con bearer token variable en `index_archivos/MailClass.php:14` e `index_archivos/embarques/EmbarqueClass.php:525`.

### Version 8: Respuestas, errores y contratos incompletos

Tecnica: perfilado por handler de salida JSON, redirects, codigos HTTP explicitos y fugas de error.

Hallazgos nuevos:

- Endpoints sin senal de codigo HTTP explicito: `239`.
- Endpoints con senal JSON: `127`.
- Endpoints con senal `mysql_error()` / `die()`: `2`.
- Handlers con fuga potencial por error SQL: `index_archivos/data.php` e `index_archivos/embarques/CotizacionClass.php`.
- Se genero `openapi.augmented.yaml`, pero se marca provisional porque los schemas de request/response no estan probados dinamicamente.

### Version 9: Cruce con subida/importacion

Tecnica: combinacion del catalogo API con el scanner profundo de uploads.

Hallazgos nuevos:

- Endpoints con senal `FILE_UPLOAD_OR_IMPORT`: `50`.
- Scanner profundo de uploads: `19` archivos con uso de `$_FILES`, `move_uploaded_file` o copia asociada.
- Patrones repetidos en uploads: falta de CSRF, falta de allowlist de extension, falta de limite de tamano y falta de validacion MIME.
- Ejemplos: `index_archivos/cargarlibroventas_ajax.php`, `index_archivos/parametros/clientes/ajax/cargar-excel-clientes-proveedores.php`, `index_archivos/parametros/ubicaciones/ajax/uploadexcel.php`, `index_archivos/tracking/ajax/actualizartransportista.php`.

### Version 10: Convergencia

Tecnica: dos reejecuciones consecutivas del aumentador comparando contenido semantico, no timestamps.

Resultado:

- Rutas proveedoras iguales: `true`.
- Contratos consumidos iguales: `true`.
- Proveedores: `246`.
- Consumidos: `23`.
- Nuevas familias en la segunda pasada: `0`.

El bucle se considera detenido porque dos versiones consecutivas no anadieron nuevas familias de hallazgos.

### Version 11: Graphify como contraste de arquitectura

Tecnica: consulta sobre `graphify-out/graph.json` para contrastar comunidades de API, uploads, descargas e integraciones.

Hallazgos nuevos:

- La consulta de grafo devolvio muchas comunidades de vendor (`spreadsjs`, `PHPExcel`, `datatable`, `jqGrid`) al buscar APIs/uploads.
- Ese resultado confirma que la auditoria necesita filtros por codigo propio y no puede depender de busquedas globales sin contexto.
- Se uso este contraste para reforzar el scanner profundo con exclusiones y cruces basados en el catalogo PHP/AJAX ya depurado.

### Version 12: Matriz IDOR, autorizacion local y path traversal

Tecnica: cruce de parametros `id*`, `proveedor`, `cliente`, `embarque`, `viaje`, `documento`, `archivo`, sinks de archivo y senales de propiedad/sesion en el handler.

Hallazgos nuevos:

- Riesgos profundos de endpoint: `194`.
- Candidatos IDOR: `51`.
- Endpoints sin senal local de auth: `70`.
- Candidatos path traversal o manejo riesgoso de archivo/ruta: `2`.
- Endpoints de alto riesgo inicial: `/index_archivos/embarques/EmbarqueClass.php`, `/index_archivos/tracking/ajax/borrarempresa.php` y `/index_archivos/versolicituddetalle.php`.

### Version 13: Cruce endpoint contra SQL taint y `mysql_*`

Tecnica: combinacion del catalogo API con `sql_taint_findings.csv`, separando taint probado de deuda legacy.

Hallazgos nuevos:

- Endpoints con SQL taint: `16`.
- Endpoints con API `mysql_*` legacy: `43`.
- Endpoint critico: `/index_archivos/tracking/ajax/borrarempresa.php` concatena `$_POST['id']` en un `UPDATE` y queda con flags `DB_WRITE`, `NO_CSRF`, `CALLER_REFERENCED`, `IDOR_CANDIDATE`, `SQL_TAINT`, `SENSITIVE_TABLE_ACCESS` y `FK_GAP_TABLE_ACCESS`.
- Endpoint critico: `/index_archivos/embarques/ajax/listaRutas.php` usa `$_REQUEST["idembarque"]` en SQL y no muestra auth local.
- Endpoint critico: `/index_archivos/tracking/generar_excel.php` combina GET, `unserialize($_GET["data"])` y exportacion Excel.

### Version 14: Password, egress y convergencia profunda

Tecnica: cruce de parametros de password, consumidores API, TLS, secretos, bases no resueltas y dominios dev/plaintext.

Hallazgos nuevos:

- Endpoints de password sin senal local suficiente de auth/CSRF: `2`.
- Riesgos de consumidor: `22`.
- Consumidores con secreto/token/key en contexto: `12`.
- Consumidores con base no resuelta: `10`.
- Consumidores dev o HTTP plano: `6`.
- Consumidores con TLS verification desactivada: `3`.
- Dos ejecuciones consecutivas del scanner profundo dieron los mismos `194` riesgos de endpoint y `22` riesgos de consumidor; nuevas familias en la segunda pasada: `0`.

## Hallazgos principales

1. Asgard nativo no cubre la arquitectura API real del repo: reporta `0` endpoints expuestos, pero el repositorio contiene al menos `246` candidatos PHP/AJAX file-routed.
2. Hay `74` endpoints mutativos sin senal local de CSRF y `7` endpoints que escriben BD sin CSRF detectable.
3. Existen dos endpoints activos con callers y escritura de BD, ambos sin CSRF detectable: `ActualizarMICs.php` y `borrarempresa.php`.
4. La integracion Guzzle queda parcialmente invisible para Asgard y contiene `verify => false` en llamadas externas.
5. La configuracion expone secretos o valores sensibles en archivos versionados de ejemplo y codigo PHP, incluyendo credenciales DB, Google Maps, Pusher y SendGrid.
6. Hay `23` contratos consumidos auditables; `10` dependen de bases no resueltas como `URL_API` o `TRACKING_URL`.
7. La superficie de subida/importacion es relevante: `50` endpoints marcados por API y `19` archivos detectados por scanner profundo.
8. La semantica de respuestas es debil para contratos formales: `239` endpoints sin codigo HTTP explicito y OpenAPI solo provisional.
9. La ronda profunda encontro `51` candidatos IDOR, `16` endpoints con SQL taint y `43` endpoints con uso de `mysql_*`.
10. Hay `2` endpoints de password sin senal local suficiente de auth/CSRF y `2` candidatos path traversal/manejo riesgoso de archivo.

## Prioridad de correccion

1. Rotar secretos expuestos y sacar tokens/credenciales de codigo y ejemplos versionados.
2. Documentar y validar `URL_API` y `TRACKING_URL` en configuracion desplegable.
3. Rehabilitar TLS verification en Guzzle y centralizar cliente HTTP.
4. Introducir CSRF obligatorio en endpoints `POST`/`REQUEST`, empezando por los `7` que escriben BD.
5. Revisar los `2` endpoints activos con escritura y caller: `ActualizarMICs.php` y `borrarempresa.php`.
6. Revisar los endpoints IDOR con parametros `id*`, `embarque`, `viaje`, `proveedor`, `cliente` o `documento`, exigiendo propiedad/alcance por sesion en la consulta.
7. Endurecer uploads: allowlist de extensiones, MIME real, tamano maximo, nombres aleatorios y ubicacion no ejecutable.
8. Migrar queries criticas de `mysql_*`/SQL concatenado a consultas preparadas, empezando por los `16` endpoints con SQL taint.
9. Proteger endpoints de password con sesion/autorizacion explicita, token de cambio y CSRF.
10. Definir codigos HTTP y schemas de respuesta para convertir el OpenAPI provisional en contrato verificable.

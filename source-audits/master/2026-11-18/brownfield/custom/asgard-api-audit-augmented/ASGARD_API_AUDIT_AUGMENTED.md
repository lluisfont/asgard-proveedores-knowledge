# ASGARD API Auditor - augmented iterative audit

Status: REVIEW_REQUIRED

Static augmentation for a legacy PHP file-routed application. Native findings are included only when an actual native findings file was supplied.

## Native ASGARD result

- Status: `not_executed_no_findings_supplied`
- Native exposed endpoints: not measured
- Native consumed endpoints: not measured
- Native unresolved items: not measured

## Augmented provider surface

- PHP/AJAX exposed endpoint candidates: 241
- Endpoints referenced by frontend/PHP callers: 55
- Endpoints writing database tables: 7
- Active caller + DB-write endpoints: 2
- Endpoints with upload/import signal: 47
- Endpoints without explicit status-code signal: 232
- Endpoints with `mysql_error()` / `die()` leak signal: 1

## Provider route strength

| Strength | Count |
| --- | ---: |
| `strong_ajax_endpoint` | 96 |
| `public_php_page_candidate` | 69 |
| `strong_direct_endpoint` | 65 |
| `public_php_logic_candidate` | 8 |
| `strong_page_endpoint` | 3 |

## Provider groups

| Group | Count |
| --- | ---: |
| `embarques` | 81 |
| `tracking` | 75 |
| `parametros` | 15 |
| `reportes` | 15 |
| `js` | 7 |
| `libs` | 6 |
| `resetpassword` | 4 |
| `2fa` | 3 |
| `rating` | 3 |
| `logistica` | 2 |
| `reporteexcel` | 2 |
| `usuario` | 2 |
| `(root)` | 1 |
| `2fa.php` | 1 |
| `ajax` | 1 |
| `cambiocontrasena.php` | 1 |
| `cambiocontrasena_update.php` | 1 |
| `cargarlibroventas.php` | 1 |
| `cargarlibroventas_ajax.php` | 1 |
| `data.php` | 1 |
| `download.php` | 1 |
| `encodeUser.php` | 1 |
| `excel.php` | 1 |
| `footer.php` | 1 |
| `footerbs4.php` | 1 |
| `guardia_descargas_rel.php` | 1 |
| `logAsgard.php` | 1 |
| `login.php` | 1 |
| `logout.php` | 1 |
| `MailClass.php` | 1 |
| `menu.php` | 1 |
| `menu_b4.php` | 1 |
| `permisos.php` | 1 |
| `php-jwt-5.2.0` | 1 |
| `principal.php` | 1 |
| `veriflogin.php` | 1 |
| `versolicitud.php` | 1 |
| `versolicituddetalle.php` | 1 |

## Augmented consumed API surface

- Consumed call candidates: 20

| Flag | Count |
| --- | ---: |
| `CREDENTIAL_OR_KEY_IN_CALL` | 11 |
| `UNRESOLVED_BASE_CONSTANT` | 8 |
| `TLS_VERIFY_DISABLED` | 3 |
| `PLAINTEXT_HTTP` | 3 |

## Consumed calls

| Method | URL | Evidence count | Evidence samples | Flags |
| --- | --- | ---: | --- | --- |
| `GET_OR_UNKNOWN` | `UNRESOLVED_CONST:TRACKING_URL` | 1 | `index_archivos/tracking/viajedetalle.php:580` | `UNRESOLVED_BASE_CONSTANT` |
| `GET_OR_UNKNOWN` | `UNRESOLVED_CONST:TRACKING_URL/event/journey` | 1 | `index_archivos/tracking/ListaViajesClass.php:205` | `TLS_VERIFY_DISABLED;UNRESOLVED_BASE_CONSTANT` |
| `GET_OR_UNKNOWN` | `UNRESOLVED_CONST:URL_API` | 3 | `index_archivos/embarques/frames/inventario.php:77;index_archivos/embarques/frames/inventario_local.php:85;index_archivos/logistica/inventario-chasis.php:146` | `CREDENTIAL_OR_KEY_IN_CALL;UNRESOLVED_BASE_CONSTANT` |
| `GET_OR_UNKNOWN` | `UNRESOLVED_CONST:URL_API/inventario/proveedores/reportes/buscar-chasis` | 1 | `index_archivos/reportes/inventario-por-chasis.php:71` | `CREDENTIAL_OR_KEY_IN_CALL;UNRESOLVED_BASE_CONSTANT` |
| `GET_OR_UNKNOWN` | `UNRESOLVED_CONST:URL_API/inventario/proveedores/reportes/resumen-inventario` | 1 | `index_archivos/reportes/inventario-por-chasis.php:93` | `CREDENTIAL_OR_KEY_IN_CALL;UNRESOLVED_BASE_CONSTANT` |
| `GET_OR_UNKNOWN` | `http://181.188.187.222/sistemas/clientes` | 1 | `.env-example.php:22` | `PLAINTEXT_HTTP` |
| `GET_OR_UNKNOWN` | `http://api-documents-dev.kpogroup.bo` | 1 | `.env-example.php:23` | `PLAINTEXT_HTTP` |
| `GET_OR_UNKNOWN` | `http://ip-api.com/json/` | 1 | `index_archivos/2fa/TwoFaClass.php:55` | `PLAINTEXT_HTTP` |
| `GET_OR_UNKNOWN` | `https://api-documents-dev.kpogroup.bo` | 4 | `.env-example.php:24;index_archivos/embarques/frames/aduanas.php:94;index_archivos/embarques/frames/documentos.php:63;index_archivos/versolicituddetalle.php:344` | `CREDENTIAL_OR_KEY_IN_CALL` |
| `GET_OR_UNKNOWN` | `https://api.mapbox.com/styles/v1/` | 2 | `index_archivos/tracking/js/asignarviaje.js:146;index_archivos/tracking/js/localizacion.js:119` | `CREDENTIAL_OR_KEY_IN_CALL` |
| `GET_OR_UNKNOWN` | `https://api.sendgrid.com/v3/mail/send` | 2 | `index_archivos/MailClass.php:84;index_archivos/embarques/EmbarqueClass.php:542` | `` |
| `GET_OR_UNKNOWN` | `https://asgard.kpogroup.bo/sistemas/clientes/index_archivos/logistica/embarquever.php?id=` | 1 | `index_archivos/tracking/ajaxAsignacion/guardar_asignacion.php:120` | `CREDENTIAL_OR_KEY_IN_CALL` |
| `GET_OR_UNKNOWN` | `https://developer1.kpogroup.bo:4431/asesoria-gestion/public/index.php` | 2 | `.env-example.php:27;index_archivos/embarques/asesoria-gestion/index.php:39` | `` |
| `GET_OR_UNKNOWN` | `https://files-documents-dev.kpogroup.bo` | 4 | `.env-example.php:25;index_archivos/embarques/frames/aduanas.php:95;index_archivos/embarques/frames/documentos.php:68;index_archivos/versolicituddetalle.php:345` | `CREDENTIAL_OR_KEY_IN_CALL` |
| `GET_OR_UNKNOWN` | `https://maps.googleapis.com/maps/api/geocode/json?key=` | 1 | `index_archivos/parametros/ubicaciones/js/mapaEventoViaje.js:68` | `CREDENTIAL_OR_KEY_IN_CALL` |
| `GET_OR_UNKNOWN` | `https://maps.googleapis.com/maps/api/geocode/json?key=$` | 1 | `index_archivos/tracking/vue/components/location.component.js:104` | `CREDENTIAL_OR_KEY_IN_CALL` |
| `GET_OR_UNKNOWN` | `https://maps.googleapis.com/maps/api/js?key=` | 4 | `index_archivos/embarques/frames/rutas.php:196;index_archivos/parametros/ubicaciones/index.php:133;index_archivos/tracking/listaviajes.php:365;index_archivos/tracking/viajedetalle.php:599` | `CREDENTIAL_OR_KEY_IN_CALL` |
| `POST` | `UNRESOLVED_CONST:TRACKING_URL/event/journey` | 1 | `index_archivos/tracking/ListaViajesClass.php:206` | `TLS_VERIFY_DISABLED;UNRESOLVED_BASE_CONSTANT` |
| `POST` | `UNRESOLVED_CONST:URL_API/enviar-whatsapp` | 1 | `index_archivos/tracking/TrackingNewClass.php:971` | `CREDENTIAL_OR_KEY_IN_CALL;TLS_VERIFY_DISABLED;UNRESOLVED_BASE_CONSTANT` |
| `PUT` | `UNRESOLVED_CONST:URL_API` | 1 | `index_archivos/embarques/frames/items.php:43` | `UNRESOLVED_BASE_CONSTANT` |

## Active DB-writing API candidates

| Route | Methods | Callers | Tables written | Flags |
| --- | --- | ---: | --- | --- |
| `/index_archivos/reportes/exportaciones/ajax/ActualizarMICs.php` | `POST|GET` | 3 | `dex_suma` | `DB_WRITE_WITHOUT_CSRF_SIGNAL ; DESTRUCTIVE_OR_MUTATING_ACTION ; FILE_DOWNLOAD_OR_EXPORT ; JSON_ENDPOINT ; POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL ; RAW_SQL_SIGNAL` |
| `/index_archivos/tracking/ajax/borrarempresa.php` | `POST` | 1 | `tck_operadorestransporte` | `DB_WRITE_WITHOUT_CSRF_SIGNAL ; DESTRUCTIVE_OR_MUTATING_ACTION ; JSON_ENDPOINT ; POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL ; RAW_SQL_SIGNAL` |

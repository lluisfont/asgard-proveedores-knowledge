# ASGARD API Auditor - augmented iterative audit

Status: REVIEW_REQUIRED

This report combines native `asgard-api-auditor` v0.8.0 output with deterministic augmentation for this legacy PHP file-routed application.

## Native ASGARD result

- Status: `partial`
- Native exposed endpoints: 0
- Native consumed endpoints: 2
- Native unresolved items: 1

## Augmented provider surface

- PHP/AJAX exposed endpoint candidates: 246
- Endpoints referenced by frontend/PHP callers: 56
- Endpoints writing database tables: 7
- Active caller + DB-write endpoints: 2
- Endpoints with upload/import signal: 50
- Endpoints without explicit status-code signal: 239
- Endpoints with `mysql_error()` / `die()` leak signal: 2

## Provider route strength

| Strength | Count |
| --- | ---: |
| `strong_ajax_endpoint` | 96 |
| `strong_direct_endpoint` | 70 |
| `public_php_page_candidate` | 69 |
| `public_php_logic_candidate` | 8 |
| `strong_page_endpoint` | 3 |

## Provider groups

| Group | Count |
| --- | ---: |
| `embarques` | 82 |
| `tracking` | 74 |
| `reportes` | 17 |
| `parametros` | 15 |
| `js` | 7 |
| `libs` | 6 |
| `preembarques` | 4 |
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

- Consumed call candidates: 23

| Flag | Count |
| --- | ---: |
| `CREDENTIAL_OR_KEY_IN_CALL` | 12 |
| `UNRESOLVED_BASE_CONSTANT` | 10 |
| `TLS_VERIFY_DISABLED` | 3 |
| `PLAINTEXT_HTTP` | 3 |

## Consumed calls

| Method | URL | Evidence count | Evidence samples | Flags |
| --- | --- | ---: | --- | --- |
| `GET_OR_UNKNOWN` | `UNRESOLVED_CONST:TRACKING_URL` | 1 | `index_archivos/tracking/viajedetalle.php:580` | `UNRESOLVED_BASE_CONSTANT` |
| `GET_OR_UNKNOWN` | `UNRESOLVED_CONST:TRACKING_URL/event/journey` | 1 | `index_archivos/tracking/ListaViajesClass.php:205` | `TLS_VERIFY_DISABLED;UNRESOLVED_BASE_CONSTANT` |
| `GET_OR_UNKNOWN` | `UNRESOLVED_CONST:URL_API` | 5 | `index_archivos/embarques/frames/inventario.php:66;index_archivos/embarques/frames/inventario_local.php:74;index_archivos/logistica/inventario-chasis.php:146;index_archivos/preembarques/frames/inventario.php:560;index_archivos/preembarques/index.php:110` | `CREDENTIAL_OR_KEY_IN_CALL;UNRESOLVED_BASE_CONSTANT` |
| `GET_OR_UNKNOWN` | `UNRESOLVED_CONST:URL_API/cargar-excel-destino-viaje` | 1 | `index_archivos/tracking/listaviajes.php:417` | `UNRESOLVED_BASE_CONSTANT` |
| `GET_OR_UNKNOWN` | `UNRESOLVED_CONST:URL_API/inventario/proveedores/reportes/buscar-chasis` | 1 | `index_archivos/reportes/inventario-por-chasis.php:71` | `CREDENTIAL_OR_KEY_IN_CALL;UNRESOLVED_BASE_CONSTANT` |
| `GET_OR_UNKNOWN` | `UNRESOLVED_CONST:URL_API/inventario/proveedores/reportes/resumen-inventario` | 1 | `index_archivos/reportes/inventario-por-chasis.php:93` | `CREDENTIAL_OR_KEY_IN_CALL;UNRESOLVED_BASE_CONSTANT` |
| `GET_OR_UNKNOWN` | `UNRESOLVED_CONST:URL_API/proveedores/lista-pedidos` | 1 | `index_archivos/embarques/pedidos.php:267` | `CREDENTIAL_OR_KEY_IN_CALL;UNRESOLVED_BASE_CONSTANT` |
| `GET_OR_UNKNOWN` | `http://181.188.187.222/sistemas/clientes` | 1 | `.env-example.php:22` | `PLAINTEXT_HTTP` |
| `GET_OR_UNKNOWN` | `http://api-documents-dev.kpogroup.bo` | 1 | `.env-example.php:23` | `PLAINTEXT_HTTP` |
| `GET_OR_UNKNOWN` | `http://ip-api.com/json/` | 1 | `index_archivos/2fa/TwoFaClass.php:54` | `PLAINTEXT_HTTP` |
| `GET_OR_UNKNOWN` | `https://api-documents-dev.kpogroup.bo` | 4 | `.env-example.php:24;index_archivos/embarques/pedidos.php:218;index_archivos/embarques/pedidos.php:220;index_archivos/versolicituddetalle.php:344` | `CREDENTIAL_OR_KEY_IN_CALL` |
| `GET_OR_UNKNOWN` | `https://api.mapbox.com/styles/v1/` | 2 | `index_archivos/tracking/js/asignarviaje.js:146;index_archivos/tracking/js/localizacion.js:119` | `CREDENTIAL_OR_KEY_IN_CALL` |
| `GET_OR_UNKNOWN` | `https://api.sendgrid.com/v3/mail/send` | 2 | `index_archivos/MailClass.php:84;index_archivos/embarques/EmbarqueClass.php:558` | `` |
| `GET_OR_UNKNOWN` | `https://asgard.kpogroup.bo/sistemas/clientes/index_archivos/logistica/embarquever.php?id=` | 1 | `index_archivos/tracking/ajaxAsignacion/guardar_asignacion.php:120` | `CREDENTIAL_OR_KEY_IN_CALL` |
| `GET_OR_UNKNOWN` | `https://asgardapispe.kpogroup.bo/api/asgard-clientes/public/index.php` | 1 | `index_archivos/preembarques/js/datosPreembarques.js:1021` | `CREDENTIAL_OR_KEY_IN_CALL` |
| `GET_OR_UNKNOWN` | `https://developer1.kpogroup.bo:4431/asesoria-gestion/public/index.php` | 2 | `.env-example.php:27;index_archivos/embarques/asesoria-gestion/index.php:39` | `` |
| `GET_OR_UNKNOWN` | `https://files-documents-dev.kpogroup.bo` | 3 | `.env-example.php:25;index_archivos/embarques/pedidos.php:221;index_archivos/versolicituddetalle.php:345` | `` |
| `GET_OR_UNKNOWN` | `https://maps.googleapis.com/maps/api/geocode/json?key=` | 1 | `index_archivos/parametros/ubicaciones/js/mapaEventoViaje.js:68` | `CREDENTIAL_OR_KEY_IN_CALL` |
| `GET_OR_UNKNOWN` | `https://maps.googleapis.com/maps/api/geocode/json?key=$` | 1 | `index_archivos/tracking/vue/components/location.component.js:104` | `CREDENTIAL_OR_KEY_IN_CALL` |
| `GET_OR_UNKNOWN` | `https://maps.googleapis.com/maps/api/js?key=` | 4 | `index_archivos/embarques/frames/rutas.php:177;index_archivos/parametros/ubicaciones/index.php:133;index_archivos/tracking/listaviajes.php:462;index_archivos/tracking/viajedetalle.php:599` | `CREDENTIAL_OR_KEY_IN_CALL` |
| `POST` | `UNRESOLVED_CONST:TRACKING_URL/event/journey` | 1 | `index_archivos/tracking/ListaViajesClass.php:206` | `TLS_VERIFY_DISABLED;UNRESOLVED_BASE_CONSTANT` |
| `POST` | `UNRESOLVED_CONST:URL_API/enviar-whatsapp` | 1 | `index_archivos/tracking/TrackingNewClass.php:971` | `CREDENTIAL_OR_KEY_IN_CALL;TLS_VERIFY_DISABLED;UNRESOLVED_BASE_CONSTANT` |
| `PUT` | `UNRESOLVED_CONST:URL_API` | 3 | `index_archivos/embarques/frames/items.php:48;index_archivos/embarques/pedidos.php:84;index_archivos/preembarques/frames/items.php:26` | `UNRESOLVED_BASE_CONSTANT` |

## Active DB-writing API candidates

| Route | Methods | Callers | Tables written | Flags |
| --- | --- | ---: | --- | --- |
| `/index_archivos/reportes/exportaciones/ajax/ActualizarMICs.php` | `POST|GET` | 3 | `dex_suma` | `DB_WRITE_WITHOUT_CSRF_SIGNAL ; DESTRUCTIVE_OR_MUTATING_ACTION ; FILE_DOWNLOAD_OR_EXPORT ; JSON_ENDPOINT ; POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL ; RAW_SQL_SIGNAL` |
| `/index_archivos/tracking/ajax/borrarempresa.php` | `POST` | 1 | `tck_operadorestransporte` | `DB_WRITE_WITHOUT_CSRF_SIGNAL ; DESTRUCTIVE_OR_MUTATING_ACTION ; JSON_ENDPOINT ; POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL ; RAW_SQL_SIGNAL` |

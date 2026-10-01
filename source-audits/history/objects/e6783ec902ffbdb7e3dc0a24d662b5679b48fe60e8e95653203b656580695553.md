# API Deep Iterative Findings

Generated: 2026-09-15T17:25:05.077469+00:00

## Summary

- Endpoint risk rows: 194
- Consumer risk rows: 22
- High endpoint risk rows (score >= 80): 19
- High consumer risk rows (score >= 40): 1

## Endpoint Risk Families

| Family | Count |
| --- | ---: |
| `NO_CSRF` | 74 |
| `NO_LOCAL_AUTH` | 70 |
| `CALLER_REFERENCED` | 56 |
| `IDOR_CANDIDATE` | 51 |
| `SENSITIVE_TABLE_ACCESS` | 50 |
| `UPLOAD_IMPORT` | 50 |
| `FK_GAP_TABLE_ACCESS` | 49 |
| `LEGACY_MYSQL_API` | 43 |
| `SQL_TAINT` | 16 |
| `DB_WRITE` | 7 |
| `DANGEROUS_SINK` | 3 |
| `PATH_TRAVERSAL_CANDIDATE` | 2 |
| `PASSWORD_CHANGE_NO_LOCAL_AUTH` | 2 |

## Consumer Risk Families

| Family | Count |
| --- | ---: |
| `SECRET_IN_CONTEXT` | 12 |
| `UNRESOLVED_BASE_CONSTANT` | 10 |
| `DEV_OR_PLAINTEXT_EGRESS` | 6 |
| `TLS_VERIFY_DISABLED` | 3 |

## Top Endpoint Risks

| Score | Route | Method | Flags | Evidence |
| ---: | --- | --- | --- | --- |
| 141 | `/index_archivos/tracking/ajax/borrarempresa.php` | `POST` | `DB_WRITE;NO_CSRF;CALLER_REFERENCED;IDOR_CANDIDATE;SQL_TAINT;SENSITIVE_TABLE_ACCESS;FK_GAP_TABLE_ACCESS` | `DB_WRITE_WITHOUT_CSRF_SIGNAL;DESTRUCTIVE_OR_MUTATING_ACTION;JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL;RAW_SQL_SIGNAL | tainted_sql:mysql_query@L8` |
| 141 | `/index_archivos/versolicituddetalle.php` | `POST|GET` | `NO_CSRF;CALLER_REFERENCED;PATH_TRAVERSAL_CANDIDATE;SQL_TAINT;LEGACY_MYSQL_API;UPLOAD_IMPORT;SENSITIVE_TABLE_ACCESS;FK_GAP_TABLE_ACCESS` | `DESTRUCTIVE_OR_MUTATING_ACTION;FILE_DOWNLOAD_OR_EXPORT;FILE_UPLOAD_OR_IMPORT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL;RAW_SQL_SIGNAL | tainted_sql:mysql_query@L10 | tainted_sql:mysql_query@L27` |
| 131 | `/index_archivos/embarques/EmbarqueClass.php` | `POST` | `DB_WRITE;NO_CSRF;PATH_TRAVERSAL_CANDIDATE;LEGACY_MYSQL_API;UPLOAD_IMPORT;SENSITIVE_TABLE_ACCESS;FK_GAP_TABLE_ACCESS` | `DB_WRITE_WITHOUT_CSRF_SIGNAL;DESTRUCTIVE_OR_MUTATING_ACTION;FILE_DOWNLOAD_OR_EXPORT;FILE_UPLOAD_OR_IMPORT;JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL;RAW_SQL_SIGNAL | legacy_mysql_api:mysql_query@L23 | legacy_mysql_api:mysql_query@L41` |
| 121 | `/index_archivos/reportes/exportaciones/ajax/ActualizarMICs.php` | `POST|GET` | `DB_WRITE;NO_CSRF;CALLER_REFERENCED;SQL_TAINT;SENSITIVE_TABLE_ACCESS;FK_GAP_TABLE_ACCESS` | `DB_WRITE_WITHOUT_CSRF_SIGNAL;DESTRUCTIVE_OR_MUTATING_ACTION;FILE_DOWNLOAD_OR_EXPORT;JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL;RAW_SQL_SIGNAL | tainted_sql:mysql_query@L40 | tainted_sql:mysql_query@L72` |
| 119 | `/index_archivos/embarques/ajax/listaRutas.php` | `REQUEST` | `NO_CSRF;NO_LOCAL_AUTH;IDOR_CANDIDATE;SQL_TAINT;SENSITIVE_TABLE_ACCESS;FK_GAP_TABLE_ACCESS` | `DESTRUCTIVE_OR_MUTATING_ACTION;JSON_ENDPOINT;NO_LOCAL_AUTH_SIGNAL;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL;RAW_SQL_SIGNAL | tainted_sql:mysql_query@L18` |
| 117 | `/index_archivos/tracking/ajax/cargar-imagenes-viaje.php` | `POST` | `NO_CSRF;IDOR_CANDIDATE;SQL_TAINT;UPLOAD_IMPORT;SENSITIVE_TABLE_ACCESS;FK_GAP_TABLE_ACCESS` | `DESTRUCTIVE_OR_MUTATING_ACTION;FILE_UPLOAD_OR_IMPORT;JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL;RAW_SQL_SIGNAL | tainted_sql:mysql_query@L11 | tainted_sql:mysql_query@L18` |
| 109 | `/index_archivos/reporteexcel/reporteexcelNew.php` | `POST` | `NO_CSRF;SQL_TAINT;LEGACY_MYSQL_API;UPLOAD_IMPORT;SENSITIVE_TABLE_ACCESS;FK_GAP_TABLE_ACCESS` | `DESTRUCTIVE_OR_MUTATING_ACTION;FILE_DOWNLOAD_OR_EXPORT;FILE_UPLOAD_OR_IMPORT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL;RAW_SQL_SIGNAL | tainted_sql:mysql_query@L11 | legacy_mysql_api:mysql_query@L125` |
| 103 | `/index_archivos/cambiocontrasena_update.php` | `POST` | `NO_CSRF;NO_LOCAL_AUTH;CALLER_REFERENCED;IDOR_CANDIDATE;PASSWORD_CHANGE_NO_LOCAL_AUTH` | `JSON_ENDPOINT;NO_LOCAL_AUTH_SIGNAL;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL` |
| 103 | `/index_archivos/reportes/exportaciones/ajax/RecepcionFisicaMICs.php` | `POST` | `NO_CSRF;CALLER_REFERENCED;SQL_TAINT;LEGACY_MYSQL_API;SENSITIVE_TABLE_ACCESS;FK_GAP_TABLE_ACCESS` | `JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL;RAW_SQL_SIGNAL | tainted_sql:mysql_query@L73 | legacy_mysql_api:mysql_query@L95` |
| 94 | `/index_archivos/js/formularios.php` | `GET` | `NO_LOCAL_AUTH;SQL_TAINT;LEGACY_MYSQL_API;UPLOAD_IMPORT;SENSITIVE_TABLE_ACCESS` | `DESTRUCTIVE_OR_MUTATING_ACTION;FILE_UPLOAD_OR_IMPORT;NO_LOCAL_AUTH_SIGNAL;RAW_SQL_SIGNAL | legacy_mysql_api:mysql_query@L502 | tainted_sql:mysql_query@L772` |
| 94 | `/index_archivos/js/formulariosA.php` | `GET` | `NO_LOCAL_AUTH;SQL_TAINT;LEGACY_MYSQL_API;UPLOAD_IMPORT;SENSITIVE_TABLE_ACCESS` | `DESTRUCTIVE_OR_MUTATING_ACTION;FILE_UPLOAD_OR_IMPORT;NO_LOCAL_AUTH_SIGNAL;RAW_SQL_SIGNAL | legacy_mysql_api:mysql_query@L482 | tainted_sql:mysql_query@L754` |
| 94 | `/index_archivos/js/formulariosB.php` | `GET` | `NO_LOCAL_AUTH;SQL_TAINT;LEGACY_MYSQL_API;UPLOAD_IMPORT;SENSITIVE_TABLE_ACCESS` | `DESTRUCTIVE_OR_MUTATING_ACTION;FILE_UPLOAD_OR_IMPORT;NO_LOCAL_AUTH_SIGNAL;RAW_SQL_SIGNAL | legacy_mysql_api:mysql_query@L502 | tainted_sql:mysql_query@L766` |
| 94 | `/index_archivos/js/formulariosR.php` | `GET` | `NO_LOCAL_AUTH;SQL_TAINT;LEGACY_MYSQL_API;UPLOAD_IMPORT;SENSITIVE_TABLE_ACCESS` | `DESTRUCTIVE_OR_MUTATING_ACTION;FILE_UPLOAD_OR_IMPORT;NO_LOCAL_AUTH_SIGNAL;RAW_SQL_SIGNAL | legacy_mysql_api:mysql_query@L509 | tainted_sql:mysql_query@L776` |
| 93 | `/index_archivos/reportes/reportepreembarquenacional.php` | `POST|GET` | `NO_CSRF;CALLER_REFERENCED;LEGACY_MYSQL_API;UPLOAD_IMPORT;SENSITIVE_TABLE_ACCESS;FK_GAP_TABLE_ACCESS` | `FILE_UPLOAD_OR_IMPORT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL;RAW_SQL_SIGNAL | legacy_mysql_api:mysql_query@L54 | legacy_mysql_api:mysql_query@L68` |
| 93 | `/index_archivos/reportes/reporteviajescargamasiva.php` | `POST|GET` | `NO_CSRF;CALLER_REFERENCED;LEGACY_MYSQL_API;UPLOAD_IMPORT;SENSITIVE_TABLE_ACCESS;FK_GAP_TABLE_ACCESS` | `FILE_UPLOAD_OR_IMPORT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL;RAW_SQL_SIGNAL | legacy_mysql_api:mysql_query@L116` |
| 93 | `/index_archivos/tracking/ajaxAsignacion/borrar_ubicacion.php` | `POST` | `DB_WRITE;NO_CSRF;SQL_TAINT;FK_GAP_TABLE_ACCESS` | `DB_WRITE_WITHOUT_CSRF_SIGNAL;DESTRUCTIVE_OR_MUTATING_ACTION;JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL;RAW_SQL_SIGNAL | tainted_sql:mysql_query@L13` |
| 86 | `/index_archivos/embarques/CotizacionClass.php` | `GET_OR_INCLUDE` | `DB_WRITE;LEGACY_MYSQL_API;UPLOAD_IMPORT;SENSITIVE_TABLE_ACCESS;FK_GAP_TABLE_ACCESS` | `DB_WRITE_WITHOUT_CSRF_SIGNAL;DESTRUCTIVE_OR_MUTATING_ACTION;FILE_UPLOAD_OR_IMPORT;RAW_SQL_SIGNAL | legacy_mysql_api:mysql_query@L20 | legacy_mysql_api:mysql_query@L40` |
| 84 | `/index_archivos/embarques/pedidos.php` | `GET` | `SQL_TAINT;LEGACY_MYSQL_API;UPLOAD_IMPORT;SENSITIVE_TABLE_ACCESS;FK_GAP_TABLE_ACCESS` | `DESTRUCTIVE_OR_MUTATING_ACTION;FILE_DOWNLOAD_OR_EXPORT;FILE_UPLOAD_OR_IMPORT;RAW_SQL_SIGNAL | legacy_mysql_api:mysql_query@L8 | legacy_mysql_api:mysql_query@L22` |
| 83 | `/index_archivos/cargarlibroventas_ajax.php` | `POST` | `NO_CSRF;CALLER_REFERENCED;LEGACY_MYSQL_API;UPLOAD_IMPORT;SENSITIVE_TABLE_ACCESS` | `DESTRUCTIVE_OR_MUTATING_ACTION;FILE_UPLOAD_OR_IMPORT;JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL;RAW_SQL_SIGNAL | legacy_mysql_api:mysql_query@L94 | legacy_mysql_api:mysql_query@L107` |
| 78 | `/index_archivos/embarques/componentes/embarques_rutas.php` | `GET` | `NO_LOCAL_AUTH;IDOR_CANDIDATE;LEGACY_MYSQL_API;SENSITIVE_TABLE_ACCESS;FK_GAP_TABLE_ACCESS` | `NO_LOCAL_AUTH_SIGNAL;RAW_SQL_SIGNAL | legacy_mysql_api:mysql_query@L10` |
| 75 | `/index_archivos/embarques/editarController.php` | `POST|REQUEST` | `NO_CSRF;CALLER_REFERENCED;LEGACY_MYSQL_API;SENSITIVE_TABLE_ACCESS;FK_GAP_TABLE_ACCESS` | `POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL;RAW_SQL_SIGNAL | legacy_mysql_api:mysql_query@L76 | legacy_mysql_api:mysql_query@L84` |
| 75 | `/index_archivos/tracking/ajax/actualizardocumentoempresatransporte.php` | `POST` | `NO_CSRF;CALLER_REFERENCED;IDOR_CANDIDATE;UPLOAD_IMPORT` | `FILE_UPLOAD_OR_IMPORT;JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL` |
| 75 | `/index_archivos/tracking/ajax/actualizartransportista.php` | `POST` | `NO_CSRF;CALLER_REFERENCED;IDOR_CANDIDATE;UPLOAD_IMPORT` | `FILE_UPLOAD_OR_IMPORT;JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL` |
| 75 | `/index_archivos/tracking/ajax/actualizarunidadtransporte.php` | `POST` | `NO_CSRF;CALLER_REFERENCED;IDOR_CANDIDATE;UPLOAD_IMPORT` | `FILE_UPLOAD_OR_IMPORT;JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL` |
| 75 | `/index_archivos/tracking/ajax/guardardocumentoempresatransporte.php` | `POST` | `NO_CSRF;CALLER_REFERENCED;IDOR_CANDIDATE;UPLOAD_IMPORT` | `FILE_UPLOAD_OR_IMPORT;JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL` |
| 75 | `/index_archivos/tracking/ajax/guardartransportista.php` | `POST` | `NO_CSRF;CALLER_REFERENCED;IDOR_CANDIDATE;UPLOAD_IMPORT` | `FILE_UPLOAD_OR_IMPORT;JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL` |
| 75 | `/index_archivos/tracking/ajax/guardarunidadtransporte.php` | `POST` | `NO_CSRF;CALLER_REFERENCED;IDOR_CANDIDATE;UPLOAD_IMPORT` | `FILE_UPLOAD_OR_IMPORT;JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL` |
| 72 | `/index_archivos/embarques/frames/estado-pedidos.php` | `GET` | `SQL_TAINT;UPLOAD_IMPORT;SENSITIVE_TABLE_ACCESS;FK_GAP_TABLE_ACCESS` | `FILE_DOWNLOAD_OR_EXPORT;FILE_UPLOAD_OR_IMPORT;JSON_ENDPOINT;RAW_SQL_SIGNAL | tainted_sql:mysql_query@L21` |
| 71 | `/index_archivos/resetpassword/ajax/resetPassword.php` | `POST` | `NO_CSRF;IDOR_CANDIDATE;PASSWORD_CHANGE_NO_LOCAL_AUTH` | `JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL` |
| 68 | `/index_archivos/logAsgard.php` | `GET_OR_INCLUDE` | `DANGEROUS_SINK;LEGACY_MYSQL_API;SENSITIVE_TABLE_ACCESS;FK_GAP_TABLE_ACCESS` | `DESTRUCTIVE_OR_MUTATING_ACTION;JSON_ENDPOINT;RAW_SQL_SIGNAL | shell_exec@L55 | legacy_mysql_api:mysql_query@L32 | legacy_mysql_api:mysql_query@L48` |

## Top Consumer Risks

| Score | Method | URL | Flags | Evidence |
| ---: | --- | --- | --- | --- |
| 40 | `POST` | `UNRESOLVED_CONST:URL_API/enviar-whatsapp` | `UNRESOLVED_BASE_CONSTANT;TLS_VERIFY_DISABLED;SECRET_IN_CONTEXT` | `index_archivos/tracking/TrackingNewClass.php:971` |
| 26 | `GET_OR_UNKNOWN` | `UNRESOLVED_CONST:TRACKING_URL/event/journey` | `UNRESOLVED_BASE_CONSTANT;TLS_VERIFY_DISABLED` | `index_archivos/tracking/ListaViajesClass.php:205` |
| 26 | `POST` | `UNRESOLVED_CONST:TRACKING_URL/event/journey` | `UNRESOLVED_BASE_CONSTANT;TLS_VERIFY_DISABLED` | `index_archivos/tracking/ListaViajesClass.php:206` |
| 26 | `GET_OR_UNKNOWN` | `https://api-documents-dev.kpogroup.bo` | `DEV_OR_PLAINTEXT_EGRESS;SECRET_IN_CONTEXT` | `.env-example.php:24;index_archivos/embarques/pedidos.php:218;index_archivos/embarques/pedidos.php:220;index_archivos/versolicituddetalle.php:344` |
| 24 | `GET_OR_UNKNOWN` | `UNRESOLVED_CONST:URL_API` | `UNRESOLVED_BASE_CONSTANT;SECRET_IN_CONTEXT` | `index_archivos/embarques/frames/inventario.php:66;index_archivos/embarques/frames/inventario_local.php:74;index_archivos/logistica/inventario-chasis.php:146;index_archivos/preembarques/frames/inventario.php:560;index_archivos/preembarques/index.php:110` |
| 24 | `GET_OR_UNKNOWN` | `UNRESOLVED_CONST:URL_API/inventario/proveedores/reportes/buscar-chasis` | `UNRESOLVED_BASE_CONSTANT;SECRET_IN_CONTEXT` | `index_archivos/reportes/inventario-por-chasis.php:71` |
| 24 | `GET_OR_UNKNOWN` | `UNRESOLVED_CONST:URL_API/inventario/proveedores/reportes/resumen-inventario` | `UNRESOLVED_BASE_CONSTANT;SECRET_IN_CONTEXT` | `index_archivos/reportes/inventario-por-chasis.php:93` |
| 24 | `GET_OR_UNKNOWN` | `UNRESOLVED_CONST:URL_API/proveedores/lista-pedidos` | `UNRESOLVED_BASE_CONSTANT;SECRET_IN_CONTEXT` | `index_archivos/embarques/pedidos.php:267` |
| 14 | `GET_OR_UNKNOWN` | `https://api.mapbox.com/styles/v1/` | `SECRET_IN_CONTEXT` | `index_archivos/tracking/js/asignarviaje.js:146;index_archivos/tracking/js/localizacion.js:119` |
| 14 | `GET_OR_UNKNOWN` | `https://asgard.kpogroup.bo/sistemas/clientes/index_archivos/logistica/embarquever.php?id=` | `SECRET_IN_CONTEXT` | `index_archivos/tracking/ajaxAsignacion/guardar_asignacion.php:120` |
| 14 | `GET_OR_UNKNOWN` | `https://asgardapispe.kpogroup.bo/api/asgard-clientes/public/index.php` | `SECRET_IN_CONTEXT` | `index_archivos/preembarques/js/datosPreembarques.js:1021` |
| 14 | `GET_OR_UNKNOWN` | `https://maps.googleapis.com/maps/api/geocode/json?key=` | `SECRET_IN_CONTEXT` | `index_archivos/parametros/ubicaciones/js/mapaEventoViaje.js:68` |
| 14 | `GET_OR_UNKNOWN` | `https://maps.googleapis.com/maps/api/geocode/json?key=$` | `SECRET_IN_CONTEXT` | `index_archivos/tracking/vue/components/location.component.js:104` |
| 14 | `GET_OR_UNKNOWN` | `https://maps.googleapis.com/maps/api/js?key=` | `SECRET_IN_CONTEXT` | `index_archivos/embarques/frames/rutas.php:177;index_archivos/parametros/ubicaciones/index.php:133;index_archivos/tracking/listaviajes.php:462;index_archivos/tracking/viajedetalle.php:599` |
| 12 | `GET_OR_UNKNOWN` | `http://181.188.187.222/sistemas/clientes` | `DEV_OR_PLAINTEXT_EGRESS` | `.env-example.php:22` |
| 12 | `GET_OR_UNKNOWN` | `http://api-documents-dev.kpogroup.bo` | `DEV_OR_PLAINTEXT_EGRESS` | `.env-example.php:23` |
| 12 | `GET_OR_UNKNOWN` | `http://ip-api.com/json/` | `DEV_OR_PLAINTEXT_EGRESS` | `index_archivos/2fa/TwoFaClass.php:54` |
| 12 | `GET_OR_UNKNOWN` | `https://developer1.kpogroup.bo:4431/asesoria-gestion/public/index.php` | `DEV_OR_PLAINTEXT_EGRESS` | `.env-example.php:27;index_archivos/embarques/asesoria-gestion/index.php:39` |
| 12 | `GET_OR_UNKNOWN` | `https://files-documents-dev.kpogroup.bo` | `DEV_OR_PLAINTEXT_EGRESS` | `.env-example.php:25;index_archivos/embarques/pedidos.php:221;index_archivos/versolicituddetalle.php:345` |
| 10 | `GET_OR_UNKNOWN` | `UNRESOLVED_CONST:TRACKING_URL` | `UNRESOLVED_BASE_CONSTANT` | `index_archivos/tracking/viajedetalle.php:580` |
| 10 | `PUT` | `UNRESOLVED_CONST:URL_API` | `UNRESOLVED_BASE_CONSTANT` | `index_archivos/embarques/frames/items.php:48;index_archivos/embarques/pedidos.php:84;index_archivos/preembarques/frames/items.php:26` |
| 10 | `GET_OR_UNKNOWN` | `UNRESOLVED_CONST:URL_API/cargar-excel-destino-viaje` | `UNRESOLVED_BASE_CONSTANT` | `index_archivos/tracking/listaviajes.php:417` |

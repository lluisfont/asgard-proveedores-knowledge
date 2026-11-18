# API Deep Iterative Findings

Generated: 2026-11-18T15:07:59.403612+00:00

## Summary

- Endpoint risk rows: 176
- Consumer risk rows: 19
- High endpoint risk rows (score >= 80): 9
- High consumer risk rows (score >= 40): 1

## Endpoint Risk Families

| Family | Count |
| --- | ---: |
| `NO_CSRF` | 73 |
| `NO_LOCAL_AUTH` | 71 |
| `CALLER_REFERENCED` | 55 |
| `IDOR_CANDIDATE` | 51 |
| `UPLOAD_IMPORT` | 47 |
| `SQL_TAINT` | 16 |
| `DB_WRITE` | 7 |
| `DANGEROUS_SINK` | 3 |
| `PASSWORD_CHANGE_NO_LOCAL_AUTH` | 2 |
| `PATH_TRAVERSAL_CANDIDATE` | 2 |

## Consumer Risk Families

| Family | Count |
| --- | ---: |
| `SECRET_IN_CONTEXT` | 11 |
| `UNRESOLVED_BASE_CONSTANT` | 8 |
| `DEV_OR_PLAINTEXT_EGRESS` | 6 |
| `TLS_VERIFY_DISABLED` | 3 |

## Top Endpoint Risks

| Score | Route | Method | Flags | Evidence |
| ---: | --- | --- | --- | --- |
| 115 | `/index_archivos/tracking/ajax/borrarempresa.php` | `POST` | `DB_WRITE;NO_CSRF;CALLER_REFERENCED;IDOR_CANDIDATE;SQL_TAINT` | `DB_WRITE_WITHOUT_CSRF_SIGNAL;DESTRUCTIVE_OR_MUTATING_ACTION;JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL;RAW_SQL_SIGNAL | tainted_sql:mysqli_query@L8` |
| 103 | `/index_archivos/cambiocontrasena_update.php` | `POST` | `NO_CSRF;NO_LOCAL_AUTH;CALLER_REFERENCED;IDOR_CANDIDATE;PASSWORD_CHANGE_NO_LOCAL_AUTH` | `JSON_ENDPOINT;NO_LOCAL_AUTH_SIGNAL;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL` |
| 103 | `/index_archivos/versolicituddetalle.php` | `POST|GET` | `NO_CSRF;CALLER_REFERENCED;PATH_TRAVERSAL_CANDIDATE;SQL_TAINT;UPLOAD_IMPORT` | `DESTRUCTIVE_OR_MUTATING_ACTION;FILE_DOWNLOAD_OR_EXPORT;FILE_UPLOAD_OR_IMPORT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL;RAW_SQL_SIGNAL | tainted_sql:mysqli_query@L10 | tainted_sql:mysqli_query@L27` |
| 95 | `/index_archivos/reportes/exportaciones/ajax/ActualizarMICs.php` | `POST|GET` | `DB_WRITE;NO_CSRF;CALLER_REFERENCED;SQL_TAINT` | `DB_WRITE_WITHOUT_CSRF_SIGNAL;DESTRUCTIVE_OR_MUTATING_ACTION;FILE_DOWNLOAD_OR_EXPORT;JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL;RAW_SQL_SIGNAL | tainted_sql:mysqli_query@L40 | tainted_sql:mysqli_query@L72` |
| 93 | `/index_archivos/embarques/EmbarqueClass.php` | `POST` | `DB_WRITE;NO_CSRF;PATH_TRAVERSAL_CANDIDATE;UPLOAD_IMPORT` | `DB_WRITE_WITHOUT_CSRF_SIGNAL;DESTRUCTIVE_OR_MUTATING_ACTION;FILE_DOWNLOAD_OR_EXPORT;FILE_UPLOAD_OR_IMPORT;JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL;RAW_SQL_SIGNAL | review_sql:mysqli_query@L23 | review_sql:mysqli_query@L41` |
| 93 | `/index_archivos/embarques/ajax/listaRutas.php` | `REQUEST` | `NO_CSRF;NO_LOCAL_AUTH;IDOR_CANDIDATE;SQL_TAINT` | `DESTRUCTIVE_OR_MUTATING_ACTION;JSON_ENDPOINT;NO_LOCAL_AUTH_SIGNAL;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL;RAW_SQL_SIGNAL | tainted_sql:mysqli_query@L18` |
| 91 | `/index_archivos/tracking/ajax/cargar-imagenes-viaje.php` | `POST` | `NO_CSRF;IDOR_CANDIDATE;SQL_TAINT;UPLOAD_IMPORT` | `DESTRUCTIVE_OR_MUTATING_ACTION;FILE_UPLOAD_OR_IMPORT;JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL;RAW_SQL_SIGNAL | tainted_sql:mysqli_query@L11 | tainted_sql:mysqli_query@L18` |
| 83 | `/index_archivos/reportes/reportecontrolad.php` | `POST|GET|REQUEST` | `NO_CSRF;CALLER_REFERENCED;SQL_TAINT;UPLOAD_IMPORT` | `DESTRUCTIVE_OR_MUTATING_ACTION;FILE_UPLOAD_OR_IMPORT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL;RAW_SQL_SIGNAL | tainted_sql:mysqli_query@L136` |
| 83 | `/index_archivos/tracking/ajaxAsignacion/borrar_ubicacion.php` | `POST` | `DB_WRITE;NO_CSRF;SQL_TAINT` | `DB_WRITE_WITHOUT_CSRF_SIGNAL;DESTRUCTIVE_OR_MUTATING_ACTION;JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL;RAW_SQL_SIGNAL | tainted_sql:mysqli_query@L13` |
| 75 | `/index_archivos/tracking/ajax/actualizardocumentoempresatransporte.php` | `POST` | `NO_CSRF;CALLER_REFERENCED;IDOR_CANDIDATE;UPLOAD_IMPORT` | `FILE_UPLOAD_OR_IMPORT;JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL` |
| 75 | `/index_archivos/tracking/ajax/actualizartransportista.php` | `POST` | `NO_CSRF;CALLER_REFERENCED;IDOR_CANDIDATE;UPLOAD_IMPORT` | `FILE_UPLOAD_OR_IMPORT;JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL` |
| 75 | `/index_archivos/tracking/ajax/actualizarunidadtransporte.php` | `POST` | `NO_CSRF;CALLER_REFERENCED;IDOR_CANDIDATE;UPLOAD_IMPORT` | `FILE_UPLOAD_OR_IMPORT;JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL` |
| 75 | `/index_archivos/tracking/ajax/guardardocumentoempresatransporte.php` | `POST` | `NO_CSRF;CALLER_REFERENCED;IDOR_CANDIDATE;UPLOAD_IMPORT` | `FILE_UPLOAD_OR_IMPORT;JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL` |
| 75 | `/index_archivos/tracking/ajax/guardartransportista.php` | `POST` | `NO_CSRF;CALLER_REFERENCED;IDOR_CANDIDATE;UPLOAD_IMPORT` | `FILE_UPLOAD_OR_IMPORT;JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL` |
| 75 | `/index_archivos/tracking/ajax/guardarunidadtransporte.php` | `POST` | `NO_CSRF;CALLER_REFERENCED;IDOR_CANDIDATE;UPLOAD_IMPORT` | `FILE_UPLOAD_OR_IMPORT;JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL` |
| 71 | `/index_archivos/reporteexcel/reporteexcelNew.php` | `POST` | `NO_CSRF;SQL_TAINT;UPLOAD_IMPORT` | `DESTRUCTIVE_OR_MUTATING_ACTION;FILE_DOWNLOAD_OR_EXPORT;FILE_UPLOAD_OR_IMPORT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL;RAW_SQL_SIGNAL | tainted_sql:mysqli_query@L11` |
| 71 | `/index_archivos/resetpassword/ajax/resetPassword.php` | `POST` | `NO_CSRF;IDOR_CANDIDATE;PASSWORD_CHANGE_NO_LOCAL_AUTH` | `JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL` |
| 68 | `/index_archivos/tracking/generar_excel.php` | `GET` | `NO_LOCAL_AUTH;DANGEROUS_SINK;UPLOAD_IMPORT` | `FILE_UPLOAD_OR_IMPORT;NO_LOCAL_AUTH_SIGNAL | unserialize@L8` |
| 66 | `/index_archivos/js/formularios.php` | `GET` | `NO_LOCAL_AUTH;SQL_TAINT;UPLOAD_IMPORT` | `DESTRUCTIVE_OR_MUTATING_ACTION;FILE_UPLOAD_OR_IMPORT;NO_LOCAL_AUTH_SIGNAL;RAW_SQL_SIGNAL | review_sql:mysqli_query@L502 | tainted_sql:mysqli_query@L772` |
| 66 | `/index_archivos/js/formulariosA.php` | `GET` | `NO_LOCAL_AUTH;SQL_TAINT;UPLOAD_IMPORT` | `DESTRUCTIVE_OR_MUTATING_ACTION;FILE_UPLOAD_OR_IMPORT;NO_LOCAL_AUTH_SIGNAL;RAW_SQL_SIGNAL | review_sql:mysqli_query@L482 | tainted_sql:mysqli_query@L754` |
| 66 | `/index_archivos/js/formulariosB.php` | `GET` | `NO_LOCAL_AUTH;SQL_TAINT;UPLOAD_IMPORT` | `DESTRUCTIVE_OR_MUTATING_ACTION;FILE_UPLOAD_OR_IMPORT;NO_LOCAL_AUTH_SIGNAL;RAW_SQL_SIGNAL | review_sql:mysqli_query@L502 | tainted_sql:mysqli_query@L766` |
| 66 | `/index_archivos/js/formulariosR.php` | `GET` | `NO_LOCAL_AUTH;SQL_TAINT;UPLOAD_IMPORT` | `DESTRUCTIVE_OR_MUTATING_ACTION;FILE_UPLOAD_OR_IMPORT;NO_LOCAL_AUTH_SIGNAL;RAW_SQL_SIGNAL | review_sql:mysqli_query@L509 | tainted_sql:mysqli_query@L776` |
| 65 | `/index_archivos/rating/get-rating.php` | `POST` | `NO_CSRF;NO_LOCAL_AUTH;IDOR_CANDIDATE` | `JSON_ENDPOINT;NO_LOCAL_AUTH_SIGNAL;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL` |
| 65 | `/index_archivos/rating/rating.php` | `POST` | `NO_CSRF;NO_LOCAL_AUTH;IDOR_CANDIDATE` | `JSON_ENDPOINT;NO_LOCAL_AUTH_SIGNAL;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL` |
| 65 | `/index_archivos/rating/verifica-mensual.php` | `POST` | `NO_CSRF;NO_LOCAL_AUTH;IDOR_CANDIDATE` | `JSON_ENDPOINT;NO_LOCAL_AUTH_SIGNAL;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL` |
| 65 | `/index_archivos/reportes/exportaciones/ajax/RecepcionFisicaMICs.php` | `POST` | `NO_CSRF;CALLER_REFERENCED;SQL_TAINT` | `JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL;RAW_SQL_SIGNAL | tainted_sql:mysqli_query@L73 | review_sql:mysqli_query@L95` |
| 63 | `/index_archivos/js/bootstrap-filestyle/test/upload.php` | `POST` | `NO_CSRF;NO_LOCAL_AUTH;UPLOAD_IMPORT` | `FILE_UPLOAD_OR_IMPORT;JSON_ENDPOINT;NO_LOCAL_AUTH_SIGNAL;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL` |
| 57 | `/index_archivos/embarques/ajax/borrarEmbarque.php` | `POST` | `NO_CSRF;CALLER_REFERENCED;IDOR_CANDIDATE` | `DESTRUCTIVE_OR_MUTATING_ACTION;JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL` |
| 57 | `/index_archivos/embarques/ajax/guardarAgenteProveedor.php` | `POST` | `NO_CSRF;CALLER_REFERENCED;IDOR_CANDIDATE` | `JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL` |
| 57 | `/index_archivos/embarques/ajax/listaPais.php` | `POST` | `NO_CSRF;CALLER_REFERENCED;IDOR_CANDIDATE` | `POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL` |

## Top Consumer Risks

| Score | Method | URL | Flags | Evidence |
| ---: | --- | --- | --- | --- |
| 40 | `POST` | `UNRESOLVED_CONST:URL_API/enviar-whatsapp` | `UNRESOLVED_BASE_CONSTANT;TLS_VERIFY_DISABLED;SECRET_IN_CONTEXT` | `index_archivos/tracking/TrackingNewClass.php:971` |
| 26 | `GET_OR_UNKNOWN` | `UNRESOLVED_CONST:TRACKING_URL/event/journey` | `UNRESOLVED_BASE_CONSTANT;TLS_VERIFY_DISABLED` | `index_archivos/tracking/ListaViajesClass.php:205` |
| 26 | `POST` | `UNRESOLVED_CONST:TRACKING_URL/event/journey` | `UNRESOLVED_BASE_CONSTANT;TLS_VERIFY_DISABLED` | `index_archivos/tracking/ListaViajesClass.php:206` |
| 26 | `GET_OR_UNKNOWN` | `https://api-documents-dev.kpogroup.bo` | `DEV_OR_PLAINTEXT_EGRESS;SECRET_IN_CONTEXT` | `.env-example.php:24;index_archivos/embarques/frames/aduanas.php:94;index_archivos/embarques/frames/documentos.php:63;index_archivos/versolicituddetalle.php:344` |
| 26 | `GET_OR_UNKNOWN` | `https://files-documents-dev.kpogroup.bo` | `DEV_OR_PLAINTEXT_EGRESS;SECRET_IN_CONTEXT` | `.env-example.php:25;index_archivos/embarques/frames/aduanas.php:95;index_archivos/embarques/frames/documentos.php:68;index_archivos/versolicituddetalle.php:345` |
| 24 | `GET_OR_UNKNOWN` | `UNRESOLVED_CONST:URL_API` | `UNRESOLVED_BASE_CONSTANT;SECRET_IN_CONTEXT` | `index_archivos/embarques/frames/inventario.php:77;index_archivos/embarques/frames/inventario_local.php:85;index_archivos/logistica/inventario-chasis.php:146` |
| 24 | `GET_OR_UNKNOWN` | `UNRESOLVED_CONST:URL_API/inventario/proveedores/reportes/buscar-chasis` | `UNRESOLVED_BASE_CONSTANT;SECRET_IN_CONTEXT` | `index_archivos/reportes/inventario-por-chasis.php:71` |
| 24 | `GET_OR_UNKNOWN` | `UNRESOLVED_CONST:URL_API/inventario/proveedores/reportes/resumen-inventario` | `UNRESOLVED_BASE_CONSTANT;SECRET_IN_CONTEXT` | `index_archivos/reportes/inventario-por-chasis.php:93` |
| 14 | `GET_OR_UNKNOWN` | `https://api.mapbox.com/styles/v1/` | `SECRET_IN_CONTEXT` | `index_archivos/tracking/js/asignarviaje.js:146;index_archivos/tracking/js/localizacion.js:119` |
| 14 | `GET_OR_UNKNOWN` | `https://asgard.kpogroup.bo/sistemas/clientes/index_archivos/logistica/embarquever.php?id=` | `SECRET_IN_CONTEXT` | `index_archivos/tracking/ajaxAsignacion/guardar_asignacion.php:120` |
| 14 | `GET_OR_UNKNOWN` | `https://maps.googleapis.com/maps/api/geocode/json?key=` | `SECRET_IN_CONTEXT` | `index_archivos/parametros/ubicaciones/js/mapaEventoViaje.js:68` |
| 14 | `GET_OR_UNKNOWN` | `https://maps.googleapis.com/maps/api/geocode/json?key=$` | `SECRET_IN_CONTEXT` | `index_archivos/tracking/vue/components/location.component.js:104` |
| 14 | `GET_OR_UNKNOWN` | `https://maps.googleapis.com/maps/api/js?key=` | `SECRET_IN_CONTEXT` | `index_archivos/embarques/frames/rutas.php:196;index_archivos/parametros/ubicaciones/index.php:133;index_archivos/tracking/listaviajes.php:365;index_archivos/tracking/viajedetalle.php:599` |
| 12 | `GET_OR_UNKNOWN` | `http://181.188.187.222/sistemas/clientes` | `DEV_OR_PLAINTEXT_EGRESS` | `.env-example.php:22` |
| 12 | `GET_OR_UNKNOWN` | `http://api-documents-dev.kpogroup.bo` | `DEV_OR_PLAINTEXT_EGRESS` | `.env-example.php:23` |
| 12 | `GET_OR_UNKNOWN` | `http://ip-api.com/json/` | `DEV_OR_PLAINTEXT_EGRESS` | `index_archivos/2fa/TwoFaClass.php:55` |
| 12 | `GET_OR_UNKNOWN` | `https://developer1.kpogroup.bo:4431/asesoria-gestion/public/index.php` | `DEV_OR_PLAINTEXT_EGRESS` | `.env-example.php:27;index_archivos/embarques/asesoria-gestion/index.php:39` |
| 10 | `GET_OR_UNKNOWN` | `UNRESOLVED_CONST:TRACKING_URL` | `UNRESOLVED_BASE_CONSTANT` | `index_archivos/tracking/viajedetalle.php:580` |
| 10 | `PUT` | `UNRESOLVED_CONST:URL_API` | `UNRESOLVED_BASE_CONSTANT` | `index_archivos/embarques/frames/items.php:43` |

# HTTP Endpoint Catalog - PHP direct routes

Status: AUGMENTED_DETERMINISTIC_SCAN

Brownfield's native route extractor reports zero route declarations for this legacy codebase.
This catalog corrects that blind spot by treating public PHP files and AJAX scripts as file-routed HTTP endpoints.

## Summary

- Endpoint candidates: 241
- Strong AJAX endpoints: 96
- Strong direct endpoints: 65
- Public PHP logic candidates: 8
- Likely third-party/test endpoints: 5
- Endpoints referenced by frontend/PHP callers: 55
- POST/REQUEST endpoints without local CSRF signal: 73
- DB-writing endpoints without local CSRF signal: 7
- Upload/import endpoints: 47
- Endpoints without local auth/session signal: 71

## Endpoint groups

| Group | Endpoints |
| --- | ---: |
| `embarques` | 81 |
| `tracking` | 75 |
| `index_archivos` | 23 |
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
| `ajax` | 1 |
| `php-jwt-5.2.0` | 1 |

## Highest risk candidates

| Route | Method | Caller refs | Tables written | Flags |
| --- | --- | ---: | --- | --- |
| `/index_archivos/embarques/EmbarqueClass.php` | `POST` | 0 | `logis_embarques;logis_embarquesdocumentos;logis_embarquesrutas` | `DB_WRITE_WITHOUT_CSRF_SIGNAL;DESTRUCTIVE_OR_MUTATING_ACTION;FILE_DOWNLOAD_OR_EXPORT;FILE_UPLOAD_OR_IMPORT;JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL;RAW_SQL_SIGNAL` |
| `/index_archivos/embarques/CotizacionClass.php` | `GET_OR_INCLUDE` | 0 | `logis_embarques;logis_embarquescontenedor;logis_embarquesdatos;logis_embarquesdocumentos;logis_embarquesmagnitudes;logis_embarquesoperador;logis_tramos` | `DB_WRITE_WITHOUT_CSRF_SIGNAL;DESTRUCTIVE_OR_MUTATING_ACTION;FILE_UPLOAD_OR_IMPORT;RAW_SQL_SIGNAL` |
| `/index_archivos/reportes/exportaciones/ajax/ActualizarMICs.php` | `POST|GET` | 3 | `dex_suma` | `DB_WRITE_WITHOUT_CSRF_SIGNAL;DESTRUCTIVE_OR_MUTATING_ACTION;FILE_DOWNLOAD_OR_EXPORT;JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL;RAW_SQL_SIGNAL` |
| `/index_archivos/tracking/ajax/borrarempresa.php` | `POST` | 1 | `tck_operadorestransporte` | `DB_WRITE_WITHOUT_CSRF_SIGNAL;DESTRUCTIVE_OR_MUTATING_ACTION;JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL;RAW_SQL_SIGNAL` |
| `/index_archivos/tracking/ajaxAsignacion/borrar_ubicacion.php` | `POST` | 0 | `tck_location` | `DB_WRITE_WITHOUT_CSRF_SIGNAL;DESTRUCTIVE_OR_MUTATING_ACTION;JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL;RAW_SQL_SIGNAL` |
| `/index_archivos/tracking/listaviajes.php` | `POST` | 0 | `` | `DESTRUCTIVE_OR_MUTATING_ACTION;FILE_DOWNLOAD_OR_EXPORT;FILE_UPLOAD_OR_IMPORT;JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL;RAW_SQL_SIGNAL` |
| `/index_archivos/tracking/TrackingNewClass.php` | `GET_OR_INCLUDE` | 0 | `logis_edp;tck_asignacion_viaje;tck_carga;tck_documentossoporte;tck_empresa_transporte;tck_items_localizaciones;tck_localizaciones;tck_location;tck_orden_viaje;tck_rutasautorizadas;tck_transportista` | `DB_WRITE_WITHOUT_CSRF_SIGNAL;DESTRUCTIVE_OR_MUTATING_ACTION;FILE_DOWNLOAD_OR_EXPORT;JSON_ENDPOINT;RAW_SQL_SIGNAL` |
| `/index_archivos/cargarlibroventas_ajax.php` | `POST` | 1 | `` | `DESTRUCTIVE_OR_MUTATING_ACTION;FILE_UPLOAD_OR_IMPORT;JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL;RAW_SQL_SIGNAL` |
| `/index_archivos/embarques/componentes/embarques_documentacion.php` | `GET_OR_INCLUDE` | 0 | `` | `DESTRUCTIVE_OR_MUTATING_ACTION;FILE_DOWNLOAD_OR_EXPORT;FILE_UPLOAD_OR_IMPORT;NO_LOCAL_AUTH_SIGNAL;RAW_SQL_SIGNAL` |
| `/index_archivos/reporteexcel/reporteexcelNew.php` | `POST` | 0 | `` | `DESTRUCTIVE_OR_MUTATING_ACTION;FILE_DOWNLOAD_OR_EXPORT;FILE_UPLOAD_OR_IMPORT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL;RAW_SQL_SIGNAL` |
| `/index_archivos/tracking/ajax/cargar-imagenes-viaje.php` | `POST` | 0 | `` | `DESTRUCTIVE_OR_MUTATING_ACTION;FILE_UPLOAD_OR_IMPORT;JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL;RAW_SQL_SIGNAL` |
| `/index_archivos/tracking/documentosempresatransporte.php` | `GET` | 0 | `` | `DESTRUCTIVE_OR_MUTATING_ACTION;FILE_DOWNLOAD_OR_EXPORT;FILE_UPLOAD_OR_IMPORT;JSON_ENDPOINT;RAW_SQL_SIGNAL` |
| `/index_archivos/tracking/reporte-viajes.php` | `POST|GET` | 1 | `` | `FILE_DOWNLOAD_OR_EXPORT;FILE_UPLOAD_OR_IMPORT;JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL;RAW_SQL_SIGNAL` |
| `/index_archivos/versolicituddetalle.php` | `POST|GET` | 2 | `` | `DESTRUCTIVE_OR_MUTATING_ACTION;FILE_DOWNLOAD_OR_EXPORT;FILE_UPLOAD_OR_IMPORT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL;RAW_SQL_SIGNAL` |
| `/index_archivos/embarques/ajax/duplicarEmbarque.php` | `POST|REQUEST` | 1 | `` | `DESTRUCTIVE_OR_MUTATING_ACTION;FILE_UPLOAD_OR_IMPORT;JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL` |
| `/index_archivos/embarques/embarquecrear.php` | `GET` | 0 | `` | `DESTRUCTIVE_OR_MUTATING_ACTION;FILE_UPLOAD_OR_IMPORT;JSON_ENDPOINT;RAW_SQL_SIGNAL` |
| `/index_archivos/embarques/embarquesController.php` | `POST|REQUEST` | 9 | `` | `FILE_DOWNLOAD_OR_EXPORT;FILE_UPLOAD_OR_IMPORT;JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL` |
| `/index_archivos/embarques/frames/documentos.php` | `GET` | 0 | `` | `DESTRUCTIVE_OR_MUTATING_ACTION;FILE_UPLOAD_OR_IMPORT;JSON_ENDPOINT;RAW_SQL_SIGNAL` |
| `/index_archivos/embarques/frames/estado-pedidos.php` | `GET` | 0 | `` | `FILE_DOWNLOAD_OR_EXPORT;FILE_UPLOAD_OR_IMPORT;JSON_ENDPOINT;RAW_SQL_SIGNAL` |
| `/index_archivos/embarques/frames/rutas.php` | `GET` | 0 | `` | `DESTRUCTIVE_OR_MUTATING_ACTION;FILE_UPLOAD_OR_IMPORT;JSON_ENDPOINT;RAW_SQL_SIGNAL` |
| `/index_archivos/js/bootstrap-filestyle/test/upload.php` | `POST` | 0 | `` | `FILE_UPLOAD_OR_IMPORT;JSON_ENDPOINT;NO_LOCAL_AUTH_SIGNAL;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL` |
| `/index_archivos/js/formularios.php` | `GET` | 0 | `` | `DESTRUCTIVE_OR_MUTATING_ACTION;FILE_UPLOAD_OR_IMPORT;NO_LOCAL_AUTH_SIGNAL;RAW_SQL_SIGNAL` |
| `/index_archivos/js/formulariosA.php` | `GET` | 0 | `` | `DESTRUCTIVE_OR_MUTATING_ACTION;FILE_UPLOAD_OR_IMPORT;NO_LOCAL_AUTH_SIGNAL;RAW_SQL_SIGNAL` |
| `/index_archivos/js/formulariosB.php` | `GET` | 0 | `` | `DESTRUCTIVE_OR_MUTATING_ACTION;FILE_UPLOAD_OR_IMPORT;NO_LOCAL_AUTH_SIGNAL;RAW_SQL_SIGNAL` |
| `/index_archivos/js/formulariosR.php` | `GET` | 0 | `` | `DESTRUCTIVE_OR_MUTATING_ACTION;FILE_UPLOAD_OR_IMPORT;NO_LOCAL_AUTH_SIGNAL;RAW_SQL_SIGNAL` |
| `/index_archivos/parametros/clientes/index.php` | `GET_OR_INCLUDE` | 0 | `` | `DESTRUCTIVE_OR_MUTATING_ACTION;FILE_UPLOAD_OR_IMPORT;JSON_ENDPOINT;RAW_SQL_SIGNAL` |
| `/index_archivos/parametros/ubicaciones/ajax/uploadexcel.php` | `POST` | 1 | `` | `DESTRUCTIVE_OR_MUTATING_ACTION;FILE_UPLOAD_OR_IMPORT;JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL` |
| `/index_archivos/reportes/reportecontrolad.php` | `POST|GET|REQUEST` | 1 | `` | `DESTRUCTIVE_OR_MUTATING_ACTION;FILE_UPLOAD_OR_IMPORT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL;RAW_SQL_SIGNAL` |
| `/index_archivos/resetpassword/ResetPassword.php` | `GET_OR_INCLUDE` | 0 | `dav_reseteos_passswords_proveedores;prov_usuarioaccesoproveedor` | `DB_WRITE_WITHOUT_CSRF_SIGNAL;DESTRUCTIVE_OR_MUTATING_ACTION;RAW_SQL_SIGNAL` |
| `/index_archivos/tracking/empresatransporte.php` | `GET_OR_INCLUDE` | 0 | `` | `DESTRUCTIVE_OR_MUTATING_ACTION;FILE_UPLOAD_OR_IMPORT;JSON_ENDPOINT;RAW_SQL_SIGNAL` |
| `/index_archivos/download.php` | `GET` | 0 | `` | `FILE_DOWNLOAD_OR_EXPORT;FILE_UPLOAD_OR_IMPORT;NO_LOCAL_AUTH_SIGNAL` |
| `/index_archivos/embarques/ajax/listaEmbarques.php` | `POST|REQUEST` | 0 | `` | `DESTRUCTIVE_OR_MUTATING_ACTION;FILE_DOWNLOAD_OR_EXPORT;JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL;RAW_SQL_SIGNAL` |
| `/index_archivos/embarques/ajax/listaRutas.php` | `REQUEST` | 0 | `` | `DESTRUCTIVE_OR_MUTATING_ACTION;JSON_ENDPOINT;NO_LOCAL_AUTH_SIGNAL;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL;RAW_SQL_SIGNAL` |
| `/index_archivos/embarques/componentes/embarques_detalle_gestion_aduanera.php` | `GET_OR_INCLUDE` | 0 | `` | `DESTRUCTIVE_OR_MUTATING_ACTION;FILE_UPLOAD_OR_IMPORT;RAW_SQL_SIGNAL` |
| `/index_archivos/excel.php` | `GET_OR_INCLUDE` | 0 | `` | `FILE_DOWNLOAD_OR_EXPORT;FILE_UPLOAD_OR_IMPORT;NO_LOCAL_AUTH_SIGNAL` |
| `/index_archivos/parametros/clientes/ajax/cargar-excel-clientes-proveedores.php` | `POST` | 1 | `` | `FILE_UPLOAD_OR_IMPORT;JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL` |
| `/index_archivos/reporteexcel/reporteexcel.php` | `POST` | 3 | `` | `FILE_DOWNLOAD_OR_EXPORT;FILE_UPLOAD_OR_IMPORT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL` |
| `/index_archivos/reportes/reportetrackingnacionallocal.php` | `POST|GET` | 5 | `` | `FILE_UPLOAD_OR_IMPORT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL;RAW_SQL_SIGNAL` |
| `/index_archivos/tracking/ajax/actualizardocumentoempresatransporte.php` | `POST` | 1 | `` | `FILE_UPLOAD_OR_IMPORT;JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL` |
| `/index_archivos/tracking/ajax/actualizartransportista.php` | `POST` | 1 | `` | `FILE_UPLOAD_OR_IMPORT;JSON_ENDPOINT;POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL` |

## Notes

- `auth_signal` is local evidence only. Included files may enforce authorization indirectly.
- `csrf_signal` is based on token naming patterns. Absence is a review finding, not final proof of exploitability.
- Table reads/writes are imported from Brownfield process edges when available.

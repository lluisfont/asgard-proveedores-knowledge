# Deep Security Findings - augmented pass

Status: REVIEW_REQUIRED

This pass adds targeted PHP and SQL-dump checks on top of Brownfield's baseline.

## Summary

- SQL sink findings: 450
- Upload handling findings: 19
- Dangerous PHP sink findings: 3
- SQL routine risk findings: 0

## SQL sink risk counts

| Risk | Count |
| --- | ---: |
| `review_sql` | 403 |
| `tainted_sql` | 46 |
| `legacy_mysql_api` | 1 |

## Upload flags

| Flag | Count |
| --- | ---: |
| `NO_CSRF_SIGNAL` | 19 |
| `NO_SIZE_LIMIT_SIGNAL` | 19 |
| `NO_EXTENSION_ALLOWLIST_SIGNAL` | 18 |
| `NO_MIME_CHECK_SIGNAL` | 16 |
| `CLIENT_FILENAME_USED_WITHOUT_RANDOMIZATION_SIGNAL` | 8 |
| `COPY_USED_FOR_UPLOAD` | 4 |
| `NO_AUTH_SIGNAL` | 1 |

## Dangerous sink counts

| Sink | Count |
| --- | ---: |
| `unserialize` | 2 |
| `shell_exec` | 1 |

## SQL routine flags

| Flag | Count |
| --- | ---: |

## Highest priority SQL sinks

| File | Line | Risk | Signal |
| --- | ---: | --- | --- |
| `index_archivos/embarques/ajax/listaRutas.php` | 18 | `tainted_sql` | `REQUEST.idembarque` |
| `index_archivos/embarques/frames/costos.php` | 54 | `tainted_sql` | `$id` |
| `index_archivos/embarques/frames/estado-pedidos.php` | 21 | `tainted_sql` | `GET.id` |
| `index_archivos/js/formularios.php` | 772 | `tainted_sql` | `GET.IraPagina;GET.IraPagina` |
| `index_archivos/js/formularios.php` | 891 | `tainted_sql` | `$datog` |
| `index_archivos/js/formularios.php` | 1004 | `tainted_sql` | `$datog` |
| `index_archivos/js/formularios.php` | 1185 | `tainted_sql` | `$PaginaActual` |
| `index_archivos/js/formulariosA.php` | 754 | `tainted_sql` | `GET.IraPagina;GET.IraPagina` |
| `index_archivos/js/formulariosA.php` | 865 | `tainted_sql` | `$datog` |
| `index_archivos/js/formulariosA.php` | 964 | `tainted_sql` | `$datog` |
| `index_archivos/js/formulariosB.php` | 766 | `tainted_sql` | `GET.IraPagina;GET.IraPagina` |
| `index_archivos/js/formulariosB.php` | 881 | `tainted_sql` | `$datog` |
| `index_archivos/js/formulariosB.php` | 989 | `tainted_sql` | `$datog` |
| `index_archivos/js/formulariosB.php` | 1170 | `tainted_sql` | `$PaginaActual` |
| `index_archivos/js/formulariosR.php` | 776 | `tainted_sql` | `GET.IraPagina;GET.IraPagina` |
| `index_archivos/js/formulariosR.php` | 891 | `tainted_sql` | `$datog` |
| `index_archivos/js/formulariosR.php` | 1000 | `tainted_sql` | `$datog` |
| `index_archivos/js/formulariosR.php` | 1181 | `tainted_sql` | `$PaginaActual` |
| `index_archivos/reporteexcel/reporteexcelNew.php` | 11 | `tainted_sql` | `POST.idreportescliente;POST.query;POST.datos;POST.posiciones;POST.formatos;POST.cabecera` |
| `index_archivos/reportes/exportaciones/ajax/ActualizarMICs.php` | 40 | `tainted_sql` | `$tipo` |
| `index_archivos/reportes/exportaciones/ajax/ActualizarMICs.php` | 72 | `tainted_sql` | `$tipo` |
| `index_archivos/reportes/exportaciones/ajax/RecepcionFisicaMICs.php` | 73 | `tainted_sql` | `$estadoDocumento;$placa` |
| `index_archivos/reportes/reportecontrolad.php` | 136 | `tainted_sql` | `$modalidad` |
| `index_archivos/tracking/ajax/borrarempresa.php` | 8 | `tainted_sql` | `POST.id` |
| `index_archivos/tracking/ajax/cargar-imagenes-viaje.php` | 11 | `tainted_sql` | `FILES.image;POST.viaje-id` |
| `index_archivos/tracking/ajax/cargar-imagenes-viaje.php` | 18 | `tainted_sql` | `$viajeId` |
| `index_archivos/tracking/ajaxAsignacion/borrar_ubicacion.php` | 13 | `tainted_sql` | `POST.id` |
| `index_archivos/tracking/ajaxAsignacion/guardar_asignacion.php` | 127 | `tainted_sql` | `$idEmbarque` |
| `index_archivos/tracking/ajaxAsignacion/guardar_asignacion.php` | 128 | `tainted_sql` | `$idEmbarque` |
| `index_archivos/versolicituddetalle.php` | 10 | `tainted_sql` | `GET.idcasosprevios;GET.idcasos;GET.accion` |
| `index_archivos/versolicituddetalle.php` | 27 | `tainted_sql` | `$idcasos;$idcasosprevios` |
| `index_archivos/versolicituddetalle.php` | 64 | `tainted_sql` | `POST.otrosdocumentosprevios-0-0;FILES.filesotro-0-0` |
| `index_archivos/versolicituddetalle.php` | 66 | `tainted_sql` | `POST.otrosdocumentosprevios-0-0;FILES.filesotro-0-0` |
| `index_archivos/versolicituddetalle.php` | 86 | `tainted_sql` | `FILES.filesotro-0-0;FILES.filesotro-0-0;FILES.filesotro-0-0;FILES.filesotro-0-0` |
| `index_archivos/versolicituddetalle.php` | 95 | `tainted_sql` | `FILES.filesotro-0-0` |
| `index_archivos/versolicituddetalle.php` | 98 | `tainted_sql` | `$accion;$idcasosprevios` |
| `index_archivos/versolicituddetalle.php` | 112 | `tainted_sql` | `FILES.files` |
| `index_archivos/versolicituddetalle.php` | 123 | `tainted_sql` | `POST.cantidadotrosdocumentos` |
| `index_archivos/versolicituddetalle.php` | 135 | `tainted_sql` | `GET.idotrosdocumentosprevios;GET.idotrosdocumentosprevios;GET.idotrosdocumentosprevios;GET.idotrosdocumentosprevios` |
| `index_archivos/versolicituddetalle.php` | 140 | `tainted_sql` | `GET.idotrosdocumentosprevios;GET.idotrosdocumentosprevios;GET.idotrosdocumentosprevios;GET.idotrosdocumentosprevios;GET.idotrosdocumentosprevios` |

## Upload files needing review

| File | Flags |
| --- | --- |
| `index_archivos/cargarlibroventas_ajax.php` | `CLIENT_FILENAME_USED_WITHOUT_RANDOMIZATION_SIGNAL;COPY_USED_FOR_UPLOAD;NO_CSRF_SIGNAL;NO_EXTENSION_ALLOWLIST_SIGNAL;NO_SIZE_LIMIT_SIGNAL` |
| `index_archivos/embarques/CotizacionClass.php` | `COPY_USED_FOR_UPLOAD;NO_CSRF_SIGNAL;NO_EXTENSION_ALLOWLIST_SIGNAL;NO_MIME_CHECK_SIGNAL;NO_SIZE_LIMIT_SIGNAL` |
| `index_archivos/tracking/ajax/actualizardocumentoempresatransporte.php` | `CLIENT_FILENAME_USED_WITHOUT_RANDOMIZATION_SIGNAL;NO_CSRF_SIGNAL;NO_EXTENSION_ALLOWLIST_SIGNAL;NO_MIME_CHECK_SIGNAL;NO_SIZE_LIMIT_SIGNAL` |
| `index_archivos/tracking/ajax/actualizartransportista.php` | `CLIENT_FILENAME_USED_WITHOUT_RANDOMIZATION_SIGNAL;NO_CSRF_SIGNAL;NO_EXTENSION_ALLOWLIST_SIGNAL;NO_MIME_CHECK_SIGNAL;NO_SIZE_LIMIT_SIGNAL` |
| `index_archivos/tracking/ajax/actualizarunidadtransporte.php` | `CLIENT_FILENAME_USED_WITHOUT_RANDOMIZATION_SIGNAL;NO_CSRF_SIGNAL;NO_EXTENSION_ALLOWLIST_SIGNAL;NO_MIME_CHECK_SIGNAL;NO_SIZE_LIMIT_SIGNAL` |
| `index_archivos/tracking/ajax/guardardocumentoempresatransporte.php` | `CLIENT_FILENAME_USED_WITHOUT_RANDOMIZATION_SIGNAL;NO_CSRF_SIGNAL;NO_EXTENSION_ALLOWLIST_SIGNAL;NO_MIME_CHECK_SIGNAL;NO_SIZE_LIMIT_SIGNAL` |
| `index_archivos/tracking/ajax/guardartransportista.php` | `CLIENT_FILENAME_USED_WITHOUT_RANDOMIZATION_SIGNAL;NO_CSRF_SIGNAL;NO_EXTENSION_ALLOWLIST_SIGNAL;NO_MIME_CHECK_SIGNAL;NO_SIZE_LIMIT_SIGNAL` |
| `index_archivos/tracking/ajax/guardarunidadtransporte.php` | `CLIENT_FILENAME_USED_WITHOUT_RANDOMIZATION_SIGNAL;NO_CSRF_SIGNAL;NO_EXTENSION_ALLOWLIST_SIGNAL;NO_MIME_CHECK_SIGNAL;NO_SIZE_LIMIT_SIGNAL` |
| `index_archivos/tracking/TrackingClass.php` | `COPY_USED_FOR_UPLOAD;NO_CSRF_SIGNAL;NO_EXTENSION_ALLOWLIST_SIGNAL;NO_MIME_CHECK_SIGNAL;NO_SIZE_LIMIT_SIGNAL` |
| `index_archivos/versolicituddetalle.php` | `CLIENT_FILENAME_USED_WITHOUT_RANDOMIZATION_SIGNAL;NO_CSRF_SIGNAL;NO_EXTENSION_ALLOWLIST_SIGNAL;NO_MIME_CHECK_SIGNAL;NO_SIZE_LIMIT_SIGNAL` |
| `index_archivos/controllers/GlobalClass.php` | `NO_CSRF_SIGNAL;NO_EXTENSION_ALLOWLIST_SIGNAL;NO_MIME_CHECK_SIGNAL;NO_SIZE_LIMIT_SIGNAL` |
| `index_archivos/embarques/ajax/duplicarEmbarque.php` | `NO_CSRF_SIGNAL;NO_EXTENSION_ALLOWLIST_SIGNAL;NO_MIME_CHECK_SIGNAL;NO_SIZE_LIMIT_SIGNAL` |
| `index_archivos/embarques/EmbarqueClass.php` | `NO_CSRF_SIGNAL;NO_EXTENSION_ALLOWLIST_SIGNAL;NO_MIME_CHECK_SIGNAL;NO_SIZE_LIMIT_SIGNAL` |
| `index_archivos/embarques/embarquesController.php` | `NO_CSRF_SIGNAL;NO_EXTENSION_ALLOWLIST_SIGNAL;NO_MIME_CHECK_SIGNAL;NO_SIZE_LIMIT_SIGNAL` |
| `index_archivos/parametros/clientes/ajax/cargar-excel-clientes-proveedores.php` | `NO_CSRF_SIGNAL;NO_EXTENSION_ALLOWLIST_SIGNAL;NO_MIME_CHECK_SIGNAL;NO_SIZE_LIMIT_SIGNAL` |
| `index_archivos/parametros/ubicaciones/Ubicacion.php` | `NO_AUTH_SIGNAL;NO_CSRF_SIGNAL;NO_EXTENSION_ALLOWLIST_SIGNAL;NO_SIZE_LIMIT_SIGNAL` |
| `index_archivos/tracking/ajax/cargar-imagenes-viaje.php` | `COPY_USED_FOR_UPLOAD;NO_CSRF_SIGNAL;NO_MIME_CHECK_SIGNAL;NO_SIZE_LIMIT_SIGNAL` |
| `index_archivos/tracking/ajax/uploadExcelCargaMasiva.php` | `NO_CSRF_SIGNAL;NO_EXTENSION_ALLOWLIST_SIGNAL;NO_MIME_CHECK_SIGNAL;NO_SIZE_LIMIT_SIGNAL` |
| `index_archivos/parametros/ubicaciones/ajax/uploadexcel.php` | `NO_CSRF_SIGNAL;NO_EXTENSION_ALLOWLIST_SIGNAL;NO_SIZE_LIMIT_SIGNAL` |

## SQL routines needing review

| Routine | Kind | Lines | Flags |
| --- | --- | --- | --- |

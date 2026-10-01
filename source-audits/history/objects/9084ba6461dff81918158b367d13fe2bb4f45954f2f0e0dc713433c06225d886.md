# Deep Security Findings - augmented pass

Status: REVIEW_REQUIRED

This pass adds targeted PHP and SQL-dump checks on top of Brownfield's baseline.

## Summary

- SQL sink findings: 539
- Upload handling findings: 19
- Dangerous PHP sink findings: 3
- SQL routine risk findings: 56

## SQL sink risk counts

| Risk | Count |
| --- | ---: |
| `legacy_mysql_api` | 493 |
| `tainted_sql` | 46 |

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
| `TEMP_TABLE` | 41 |
| `SQL_STRING_CONCAT` | 34 |
| `DESTRUCTIVE_SQL` | 24 |
| `DYNAMIC_SQL` | 2 |
| `EXPLICIT_TRANSACTION` | 2 |

## Highest priority SQL sinks

| File | Line | Risk | Signal |
| --- | ---: | --- | --- |
| `index_archivos/embarques/ajax/listaRutas.php` | 18 | `tainted_sql` | `REQUEST.idembarque` |
| `index_archivos/embarques/frames/costos.php` | 54 | `tainted_sql` | `$id` |
| `index_archivos/embarques/frames/estado-pedidos.php` | 21 | `tainted_sql` | `GET.id` |
| `index_archivos/embarques/pedidos.php` | 37 | `tainted_sql` | `GET.idpedido` |
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
| `DashBoardIASA` | `PROCEDURE` | 15215-15903 | `DESTRUCTIVE_SQL;SQL_STRING_CONCAT;TEMP_TABLE` |
| `DashBoardIndicadores` | `PROCEDURE` | 15904-16197 | `DESTRUCTIVE_SQL;TEMP_TABLE` |
| `DashBoardIndicadoresA` | `PROCEDURE` | 16198-16491 | `DESTRUCTIVE_SQL;TEMP_TABLE` |
| `DashBoardObservadasArchivo` | `PROCEDURE` | 16492-16724 | `DESTRUCTIVE_SQL;SQL_STRING_CONCAT` |
| `DashBoardPrestamoDevoluciones` | `PROCEDURE` | 16725-16768 | `DESTRUCTIVE_SQL` |
| `DashBoardReporteMaestro` | `PROCEDURE` | 16769-17017 | `DESTRUCTIVE_SQL;TEMP_TABLE` |
| `DashBoardReporteMaestro2` | `PROCEDURE` | 17018-17157 | `DESTRUCTIVE_SQL` |
| `DashBoardSoat` | `PROCEDURE` | 17158-17204 | `DESTRUCTIVE_SQL` |
| `DashBoardSoat2` | `PROCEDURE` | 17205-17302 | `DESTRUCTIVE_SQL;SQL_STRING_CONCAT` |
| `DashBoardSoatNC` | `PROCEDURE` | 17303-17343 | `DESTRUCTIVE_SQL;SQL_STRING_CONCAT` |
| `DashBoardTigo` | `PROCEDURE` | 17344-18635 | `DESTRUCTIVE_SQL;SQL_STRING_CONCAT;TEMP_TABLE` |
| `DashBoardTigo2` | `PROCEDURE` | 18636-19069 | `DESTRUCTIVE_SQL;SQL_STRING_CONCAT;TEMP_TABLE` |
| `DashBoardTigobk` | `PROCEDURE` | 19070-20265 | `DESTRUCTIVE_SQL;SQL_STRING_CONCAT;TEMP_TABLE` |
| `DashBoardTotal` | `PROCEDURE` | 20266-21424 | `DESTRUCTIVE_SQL;SQL_STRING_CONCAT;TEMP_TABLE` |
| `DashBoardTotalIMCRUZ` | `PROCEDURE` | 21425-22562 | `DESTRUCTIVE_SQL;SQL_STRING_CONCAT;TEMP_TABLE` |
| `DashboardTrackingNacionalLocalImcruz` | `PROCEDURE` | 22563-22718 | `DESTRUCTIVE_SQL;SQL_STRING_CONCAT;TEMP_TABLE` |
| `DashBoardVehiculos` | `PROCEDURE` | 22719-23167 | `DESTRUCTIVE_SQL;TEMP_TABLE` |
| `DashBoardVehiculosV2` | `PROCEDURE` | 23168-23762 | `DESTRUCTIVE_SQL;TEMP_TABLE` |
| `derivaciones` | `PROCEDURE` | 23763-23957 | `DESTRUCTIVE_SQL;SQL_STRING_CONCAT;TEMP_TABLE` |
| `ExtractNumber` | `FUNCTION` | 24029-24058 | `SQL_STRING_CONCAT` |
| `liquidacion` | `PROCEDURE` | 24689-24930 | `DESTRUCTIVE_SQL;SQL_STRING_CONCAT;TEMP_TABLE` |
| `liquidacionvehiculos` | `PROCEDURE` | 24931-25347 | `DESTRUCTIVE_SQL;SQL_STRING_CONCAT;TEMP_TABLE` |
| `NewProc` | `PROCEDURE` | 25380-25393 | `DESTRUCTIVE_SQL` |
| `prorratear` | `PROCEDURE` | 25394-25667 | `TEMP_TABLE` |
| `regularizacion` | `PROCEDURE` | 25668-25764 | `SQL_STRING_CONCAT;TEMP_TABLE` |
| `regularizacioncaso` | `PROCEDURE` | 25765-25859 | `SQL_STRING_CONCAT;TEMP_TABLE` |
| `regularizacionusuario` | `PROCEDURE` | 25860-25955 | `SQL_STRING_CONCAT;TEMP_TABLE` |
| `resumenoperaciones` | `PROCEDURE` | 25956-26159 | `SQL_STRING_CONCAT;TEMP_TABLE` |
| `saldobancofecha` | `PROCEDURE` | 26160-26185 | `TEMP_TABLE` |
| `saldos` | `PROCEDURE` | 26315-27000 | `SQL_STRING_CONCAT;TEMP_TABLE` |
| `saldos111` | `PROCEDURE` | 27001-27408 | `SQL_STRING_CONCAT;TEMP_TABLE` |
| `saldosbk` | `PROCEDURE` | 27409-28040 | `SQL_STRING_CONCAT;TEMP_TABLE` |
| `saldos_clientes` | `PROCEDURE` | 28041-28361 | `DYNAMIC_SQL;SQL_STRING_CONCAT;TEMP_TABLE` |
| `sp_carpetas_procesada_oficial` | `PROCEDURE` | 28413-28490 | `DYNAMIC_SQL;SQL_STRING_CONCAT` |
| `sp_delete_trip` | `PROCEDURE` | 28491-28513 | `EXPLICIT_TRANSACTION` |
| `sp_listanoconformidad` | `PROCEDURE` | 28514-28545 | `SQL_STRING_CONCAT` |
| `sp_lista_embarques` | `PROCEDURE` | 28546-28702 | `SQL_STRING_CONCAT;TEMP_TABLE` |
| `sp_lista_pedidos` | `PROCEDURE` | 28703-28786 | `SQL_STRING_CONCAT;TEMP_TABLE` |
| `sp_lista_pedidos_general` | `PROCEDURE` | 28787-28878 | `SQL_STRING_CONCAT;TEMP_TABLE` |
| `sp_lista_pedidos_general_bk` | `PROCEDURE` | 28879-28963 | `SQL_STRING_CONCAT;TEMP_TABLE` |
| `sp_lista_pedidos_general_concesionario` | `PROCEDURE` | 28964-29055 | `SQL_STRING_CONCAT;TEMP_TABLE` |
| `sp_llenar_reporte_casos_clientes` | `PROCEDURE` | 29056-29071 | `DESTRUCTIVE_SQL` |
| `sp_pareto_hallazgo` | `PROCEDURE` | 29072-29097 | `TEMP_TABLE` |
| `sp_pareto_hallazgo_cliente` | `PROCEDURE` | 29098-29123 | `TEMP_TABLE` |
| `sp_pareto_procesos` | `PROCEDURE` | 29124-29157 | `TEMP_TABLE` |
| `sp_pareto_procesos_clientes` | `PROCEDURE` | 29158-29191 | `TEMP_TABLE` |
| `sp_reportevehiculos` | `PROCEDURE` | 29192-29247 | `SQL_STRING_CONCAT;TEMP_TABLE` |
| `sp_reportezdam` | `PROCEDURE` | 29248-29542 | `SQL_STRING_CONCAT;TEMP_TABLE` |
| `sp_reporte_fiscal_tmp` | `PROCEDURE` | 29543-29590 | `SQL_STRING_CONCAT;TEMP_TABLE` |
| `sp_reporte_inventario` | `PROCEDURE` | 29591-29720 | `TEMP_TABLE` |
| `sp_rnc_caso_reabierto` | `FUNCTION` | 29721-29739 | `SQL_STRING_CONCAT` |
| `sp_rnc_reporte_general` | `PROCEDURE` | 29740-29753 | `DESTRUCTIVE_SQL` |
| `tareaactual` | `PROCEDURE` | 29942-30001 | `SQL_STRING_CONCAT;TEMP_TABLE` |
| `tck_duplicar_viaje` | `PROCEDURE` | 30002-30057 | `EXPLICIT_TRANSACTION` |
| `valorcomision` | `FUNCTION` | 30133-30214 | `TEMP_TABLE` |
| `valorcomisiondecimal` | `FUNCTION` | 30215-30296 | `TEMP_TABLE` |

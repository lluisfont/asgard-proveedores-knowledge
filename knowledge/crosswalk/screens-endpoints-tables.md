# Pantallas, endpoints y tablas

Cruce estatico historico. `caller_sources` procede del catalogo aumentado; una referencia no demuestra que la ruta este desplegada ni que su autorizacion sea correcta. Fuente: `source-audits/brownfield/reports/custom/http_endpoint_catalog.csv`.

| Handler / fuente | Metodo inferido | Callers detectados | Tablas leidas | Tablas escritas | Confianza |
| --- | --- | --- | --- | --- | --- |
| index.php | GET |  |  |  | inferred_file_route |
| index_archivos/2fa/ajax/autenticar.php | POST |  |  |  | inferred_file_route |
| index_archivos/2fa/ajax/reenviar-codigo.php | POST |  |  |  | inferred_file_route |
| index_archivos/2fa/ajax/verificar-codigo.php | POST |  |  |  | inferred_file_route |
| index_archivos/2fa.php | GET |  |  |  | inferred_file_route |
| index_archivos/ajax/buscarDatos.php | GET |  |  |  | inferred_file_route |
| index_archivos/cambiocontrasena.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/cambiocontrasena_update.php | POST | index_archivos/cambiocontrasena.php:104 |  |  | inferred_file_route |
| index_archivos/cargarlibroventas.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/cargarlibroventas_ajax.php | POST | index_archivos/cargarlibroventas.php:25 |  |  | inferred_file_route |
| index_archivos/data.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/download.php | GET |  |  |  | inferred_file_route |
| index_archivos/embarques/ajax/asignar-viaje-embarque.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/embarques/ajax/borrarEmbarque.php | POST | index_archivos/embarques/js/datosEmbarques.js:476 |  |  | inferred_file_route |
| index_archivos/embarques/ajax/duplicarEmbarque.php | POST\|REQUEST | index_archivos/embarques/js/datosEmbarques.js:515 |  |  | inferred_file_route |
| index_archivos/embarques/ajax/get-categorias.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/embarques/ajax/get-conceptos.php | GET |  |  |  | inferred_file_route |
| index_archivos/embarques/ajax/get-costos.php | GET |  |  |  | inferred_file_route |
| index_archivos/embarques/ajax/get-monedas.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/embarques/ajax/guardar-costos.php | GET |  |  |  | inferred_file_route |
| index_archivos/embarques/ajax/guardarAgenteProveedor.php | POST | index_archivos/embarques/js/datosEmbarques.js:1069 |  |  | inferred_file_route |
| index_archivos/embarques/ajax/guardarCostos.php | POST | index_archivos/embarques/componentes/embarques_costos.php:1 |  |  | inferred_file_route |
| index_archivos/embarques/ajax/guardarGestionAduanera.php | POST\|GET |  |  |  | inferred_file_route |
| index_archivos/embarques/ajax/guardarRuta.php | POST |  |  |  | inferred_file_route |
| index_archivos/embarques/ajax/listaAerolineas.php | POST |  |  |  | inferred_file_route |
| index_archivos/embarques/ajax/listaClientes.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/embarques/ajax/listaClientesFiltro.php | GET_OR_INCLUDE | index_archivos/embarques/js/datosEmbarques.js:327 |  |  | inferred_file_route |
| index_archivos/embarques/ajax/listaEmbarques.php | POST\|REQUEST |  |  |  | inferred_file_route |
| index_archivos/embarques/ajax/listaEstado.php | GET_OR_INCLUDE | index_archivos/embarques/js/datosEmbarques.js:365 |  |  | inferred_file_route |
| index_archivos/embarques/ajax/listaLineasFiltro.php | GET_OR_INCLUDE |  | dav_clientelineas;logis_embarques |  | inferred_file_route |
| index_archivos/embarques/ajax/listaModalidadTransporte.php | GET_OR_INCLUDE | index_archivos/embarques/js/datosEmbarques.js:346 |  |  | inferred_file_route |
| index_archivos/embarques/ajax/listaPais.php | POST | index_archivos/embarques/js/datosCotizacion.js:426;index_archivos/embarques/js/datosEmbarques.js:864 |  |  | inferred_file_route |
| index_archivos/embarques/ajax/listaProveedoresFiltro.php | GET_OR_INCLUDE | index_archivos/embarques/js/datosEmbarques.js:384 |  |  | inferred_file_route |
| index_archivos/embarques/ajax/listaRutas.php | REQUEST |  | logis_embarques |  | inferred_file_route |
| index_archivos/embarques/ajax/listaTipoMercancia.php | POST | index_archivos/embarques/js/datosCotizacion.js:110;index_archivos/embarques/js/datosCotizacion.js:94;index_archivos/embarques/js/datosEmbarques.js:159;index_archivos/embarques/js/datosEmbarques.js:175 |  |  | inferred_file_route |
| index_archivos/embarques/ajax/notificacionDiariaRutas.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/embarques/ajax/recuperar-viajes.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/embarques/ajax/saveDescripcionItems.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/embarques/asesoria-gestion/index.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/embarques/componentes/cotizaciones/internacional/aereo.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/embarques/componentes/cotizaciones/internacional/ferreo.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/embarques/componentes/cotizaciones/internacional/multimodal.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/embarques/componentes/cotizaciones/internacional/terrestre.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/embarques/componentes/cotizaciones/internacional/textoplano.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/embarques/componentes/cotizaciones/local/ferreo.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/embarques/componentes/cotizaciones/local/terrestre.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/embarques/componentes/cotizaciones/local/textoplano.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/embarques/componentes/cotizaciones/nacional/aereo.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/embarques/componentes/cotizaciones/nacional/ferreo.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/embarques/componentes/cotizaciones/nacional/terrestre.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/embarques/componentes/cotizaciones/nacional/textoplano.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/embarques/componentes/embarques_contenedor_modal.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/embarques/componentes/embarques_crear_documentacion.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/embarques/componentes/embarques_datos.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/embarques/componentes/embarques_datosotros.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/embarques/componentes/embarques_datosotrosemb.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/embarques/componentes/embarques_detalle_gestion_aduanera.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/embarques/componentes/embarques_diccionario_palabras.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/embarques/componentes/embarques_documentacion.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/embarques/componentes/embarques_lista_viajes.php | GET |  | logis_embarques |  | inferred_file_route |
| index_archivos/embarques/componentes/embarques_mercancia.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/embarques/componentes/embarques_rutas.php | GET |  | logis_embarques |  | inferred_file_route |
| index_archivos/embarques/componentes/embarques_rutas_modal.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/embarques/componentes/embarques_textoplano.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/embarques/componentes/embarques_tramos.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/embarques/componentes/embarques_ver_gestion_aduanera.php | GET_OR_INCLUDE | index_archivos/embarques/componentes/embarques_detalle_gestion_aduanera.php:345 |  |  | inferred_file_route |
| index_archivos/embarques/componentes/embarques_viaje_detalle.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/embarques/componentes/estado-pedidos/ajax/eliminar.php | GET | index_archivos/parametros/ubicaciones/js/datos.js:26 |  |  | inferred_file_route |
| index_archivos/embarques/componentes/estado-pedidos/ajax/get-estado-pedidos.php | GET |  |  |  | inferred_file_route |
| index_archivos/embarques/componentes/estado-pedidos/ajax/get-estados.php | GET |  |  |  | inferred_file_route |
| index_archivos/embarques/componentes/estado-pedidos/ajax/guardar-edp.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/embarques/costos.php | GET |  | dav_proveedor;logis_costos;logis_costosconcepto;logis_costosdetalles;logis_cotizacionoperador |  | inferred_file_route |
| index_archivos/embarques/CotizacionClass.php | GET_OR_INCLUDE |  | cn_clienteconcesionario;cn_concesionario;dav_ciudad;dav_cliente;dav_clientealmacen;dav_clientelineas;dav_clienteproveedor;dav_clientetransportista;dav_localidad;dav_pais;dav_proveedor;dav_puerto;dav_region;dav_transportista;dav_unidad;logis_aeropuertos;logis_contenedor;logis_costosdetalles;logis_embarquereferencias;logis_embarques;logis_embarquescontenedor;logis_embarquesdatos;logis_embarquesdocumentos;logis_embarquesmagnitudes;logis_embarquesoperador;logis_estados;logis_incoterms;logis_tipocarga;logis_tipoembarque;logis_tipomercancia;logis_tipomercanciaclase;logis_tipomercanciaun;logis_tipoviaje;prov_clientes_proveedores;prov_usuarioaccesoproveedor;tck_lugaresentregacarga | logis_embarques;logis_embarquescontenedor;logis_embarquesdatos;logis_embarquesdocumentos;logis_embarquesmagnitudes;logis_embarquesoperador;logis_tramos | inferred_file_route |
| index_archivos/embarques/datoscaso.php | GET |  |  |  | inferred_file_route |
| index_archivos/embarques/editar.php | GET |  |  |  | inferred_file_route |
| index_archivos/embarques/editarController.php | POST\|REQUEST | index_archivos/embarques/editar.php:111 |  |  | inferred_file_route |
| index_archivos/embarques/EmbarqueClass.php | POST |  | adaprov_agenteproveedor;adaprov_agenteproveedormercancia;ads_agenteseguro;dav_aerolineas;dav_casosprevios;dav_cliente;dav_clientetransportista;dav_localidad;dav_modotransporte;dav_navieras;dav_pais;dav_proveedor;dav_region;dav_tramites;dav_transportista;logis_clientemails;logis_embarques;logis_embarquesdocumentos;logis_embarquesoperador;logis_embarquesrutas;logis_estados;logis_tipoembarque;logis_tipoviaje;logis_tramos;tck_asignacion_viaje | logis_embarques;logis_embarquesdocumentos;logis_embarquesrutas | inferred_file_route |
| index_archivos/embarques/embarquecrear.php | GET |  |  |  | inferred_file_route |
| index_archivos/embarques/embarquesController.php | POST\|REQUEST | index_archivos/embarques/componentes/embarques_documentacion.php:2;index_archivos/embarques/editar.php:382;index_archivos/embarques/embarquecrear.php:160;index_archivos/embarques/js/datosCotizacion.js:177;index_archivos/embarques/js/datosCotizacion.js:261;index_archivos/embarques/js/datosCotizacion.js:315;index_archivos/embarques/js/datosCotizacion.js:356;index_archivos/embarques/js/datosEmbarques.js:552;index_archivos/embarques/js/datosEmbarques.js:599;index_archivos/embarques/js/datosPedidos.js:261 |  |  | inferred_file_route |
| index_archivos/embarques/embarquever.php | GET |  | logis_embarques |  | inferred_file_route |
| index_archivos/embarques/frames/aduanas.php | GET |  |  |  | inferred_file_route |
| index_archivos/embarques/frames/costos.php | GET |  | logis_embarques |  | inferred_file_route |
| index_archivos/embarques/frames/datoscaso.php | GET |  |  |  | inferred_file_route |
| index_archivos/embarques/frames/documentos.php | GET |  | logis_embarques |  | inferred_file_route |
| index_archivos/embarques/frames/estado-pedidos.php | GET |  | logis_embarques |  | inferred_file_route |
| index_archivos/embarques/frames/inventario.php | GET |  |  |  | inferred_file_route |
| index_archivos/embarques/frames/inventario_local.php | GET | index_archivos/js/formularios.php:116;index_archivos/js/formulariosA.php:116;index_archivos/js/formulariosB.php:116;index_archivos/js/formulariosR.php:116 |  |  | inferred_file_route |
| index_archivos/embarques/frames/items.php | GET |  |  |  | inferred_file_route |
| index_archivos/embarques/frames/rutas.php | GET |  |  |  | inferred_file_route |
| index_archivos/embarques/frames/servicios-adicionales.php | GET |  |  |  | inferred_file_route |
| index_archivos/embarques/frames/tracking.php | GET |  |  |  | inferred_file_route |
| index_archivos/embarques/index.php | GET |  |  |  | inferred_file_route |
| index_archivos/embarques/pedidos.php | GET |  |  |  | inferred_file_route |
| index_archivos/embarques/verembarque.php | GET |  |  |  | inferred_file_route |
| index_archivos/encodeUser.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/excel.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/footer.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/footerbs4.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/js/bootstrap-filestyle/test/upload.php | POST |  |  |  | inferred_file_route |
| index_archivos/js/formularios.php | GET |  |  |  | inferred_file_route |
| index_archivos/js/formulariosA.php | GET |  |  |  | inferred_file_route |
| index_archivos/js/formulariosB.php | GET |  |  |  | inferred_file_route |
| index_archivos/js/formulariosR.php | GET |  |  |  | inferred_file_route |
| index_archivos/js/formulariosxls.php | GET |  |  |  | inferred_file_route |
| index_archivos/js/fValidate/fValidate.server.php | GET |  |  |  | inferred_file_route |
| index_archivos/libs/carbon/src/Carbon/Carbon.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/libs/carbon/src/JsonSerializable.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/libs/modulos/config.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/libs/modulos/libs/Correo.class.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/libs/modulos/libs/PDO.class.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/libs/pdo/PDO.class.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/logAsgard.php | GET_OR_INCLUDE |  | prov_usuarioaccesoproveedor |  | inferred_file_route |
| index_archivos/login.php | POST\|GET |  |  |  | inferred_file_route |
| index_archivos/logistica/embarquereferencia.php | POST |  |  |  | inferred_file_route |
| index_archivos/logistica/inventario-chasis.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/logout.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/MailClass.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/menu.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/menu_b4.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/parametros/clientes/ajax/actualizar-cliente.php | POST | index_archivos/parametros/clientes/js/index.js:171 |  |  | inferred_file_route |
| index_archivos/parametros/clientes/ajax/borrar-cliente.php | POST | index_archivos/parametros/clientes/js/index.js:133 |  |  | inferred_file_route |
| index_archivos/parametros/clientes/ajax/cargar-excel-clientes-proveedores.php | POST | index_archivos/parametros/clientes/js/index.js:190 |  |  | inferred_file_route |
| index_archivos/parametros/clientes/ajax/get-cliente.php | POST | index_archivos/parametros/clientes/js/index.js:151 |  |  | inferred_file_route |
| index_archivos/parametros/clientes/ajax/get-clientes.php | GET_OR_INCLUDE | index_archivos/parametros/clientes/js/index.js:26 |  |  | inferred_file_route |
| index_archivos/parametros/clientes/ajax/nuevo-cliente.php | POST | index_archivos/parametros/clientes/js/index.js:98 |  |  | inferred_file_route |
| index_archivos/parametros/clientes/index.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/parametros/ubicaciones/ajax/editar.php | POST |  |  |  | inferred_file_route |
| index_archivos/parametros/ubicaciones/ajax/eliminar.php | POST | index_archivos/parametros/ubicaciones/js/datos.js:26 |  |  | inferred_file_route |
| index_archivos/parametros/ubicaciones/ajax/guardar.php | POST |  |  |  | inferred_file_route |
| index_archivos/parametros/ubicaciones/ajax/lista.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/parametros/ubicaciones/ajax/uploadexcel.php | POST | index_archivos/parametros/ubicaciones/js/datos.js:148 |  |  | inferred_file_route |
| index_archivos/parametros/ubicaciones/componentes/datos.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/parametros/ubicaciones/importar.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/parametros/ubicaciones/index.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/permisos.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/php-jwt-5.2.0/src/JWT.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/preembarques/frames/inventario.php | GET |  |  |  | inferred_file_route |
| index_archivos/preembarques/frames/items.php | GET |  |  |  | inferred_file_route |
| index_archivos/preembarques/index.php | GET |  |  |  | inferred_file_route |
| index_archivos/preembarques/preembarquever.php | GET |  |  |  | inferred_file_route |
| index_archivos/principal.php | GET_OR_INCLUDE |  | ada_clienteagenteaduana;dav_clientetransportista;ges_clientegestortransporte |  | inferred_file_route |
| index_archivos/rating/get-rating.php | POST |  |  |  | inferred_file_route |
| index_archivos/rating/rating.php | POST |  |  |  | inferred_file_route |
| index_archivos/rating/verifica-mensual.php | POST |  |  |  | inferred_file_route |
| index_archivos/reporteexcel/reporteexcel.php | POST | index_archivos/reportes/reportecontrolad.php:111;index_archivos/reportes/reportecontrolol.php:111;index_archivos/reportes/reportepreembarquenacional.php:258;index_archivos/reportes/reporteviajescargamasiva.php:182 |  |  | inferred_file_route |
| index_archivos/reporteexcel/reporteexcelNew.php | POST |  |  |  | inferred_file_route |
| index_archivos/reportes/exportaciones/ajax/ActualizarMICs.php | POST\|GET | index_archivos/reportes/exportaciones/js/recepcion_fisica_mics.js:154;index_archivos/reportes/exportaciones/js/recepcion_fisica_mics.js:216;index_archivos/reportes/exportaciones/js/recepcion_fisica_mics.js:255 |  | dex_suma | inferred_file_route |
| index_archivos/reportes/exportaciones/ajax/RecepcionFisicaMICs.php | POST | index_archivos/reportes/exportaciones/js/recepcion_fisica_mics.js:62 | dav_clienteusuarios;dex_suma;dex_suma_estado_historial;prov_usuarioaccesoproveedor |  | inferred_file_route |
| index_archivos/reportes/filtros/clientes.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/reportes/filtros/fechas.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/reportes/filtros/logis_estados.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/reportes/filtros/operadores.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/reportes/filtros/proveedores.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/reportes/inventario-por-chasis.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/reportes/recepcion_fisica_mics.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/reportes/reportecontrolad.php | POST\|GET\|REQUEST | index_archivos/reportes/reportecontrolad.php:72 |  |  | inferred_file_route |
| index_archivos/reportes/reportecontroladquery.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/reportes/reportecontrolol.php | POST\|GET\|REQUEST | index_archivos/reportes/reportecontrolol.php:72 |  |  | inferred_file_route |
| index_archivos/reportes/reportecontrololquery.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/reportes/reportepreembarquenacional.php | POST\|GET | index_archivos/reportes/reportepreembarquenacional.php:224 |  |  | inferred_file_route |
| index_archivos/reportes/reportepreembarquenacionalquery.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/reportes/reporteviajescargamasiva.php | POST\|GET | index_archivos/reportes/reporteviajescargamasiva.php:103 |  |  | inferred_file_route |
| index_archivos/reportes/reporteviajescargamasivaquery.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/resetpassword/ajax/generateToken.php | POST |  |  |  | inferred_file_route |
| index_archivos/resetpassword/ajax/resetPassword.php | POST |  |  |  | inferred_file_route |
| index_archivos/resetpassword/ajax/sendCredentials.php | POST |  |  |  | inferred_file_route |
| index_archivos/resetpassword/ResetPassword.php | GET_OR_INCLUDE |  | dav_reseteos_passswords_proveedores;prov_usuarioaccesoproveedor | dav_reseteos_passswords_proveedores;prov_usuarioaccesoproveedor | inferred_file_route |
| index_archivos/tracking/ajax/actualizardocumentoempresatransporte.php | POST | index_archivos/tracking/components/modal-edit-document.php:11 |  |  | inferred_file_route |
| index_archivos/tracking/ajax/actualizarempresatransporte.php | POST | index_archivos/tracking/js/empresatransporte.js:167 |  |  | inferred_file_route |
| index_archivos/tracking/ajax/actualizartransportista.php | POST | index_archivos/tracking/components/modal-edit-user-transport.php:11 |  |  | inferred_file_route |
| index_archivos/tracking/ajax/actualizarubicacion.php | POST | index_archivos/tracking/js/localizacion.js:82 |  |  | inferred_file_route |
| index_archivos/tracking/ajax/actualizarunidadtransporte.php | POST | index_archivos/tracking/components/modal-edit-unity.php:11 |  |  | inferred_file_route |
| index_archivos/tracking/ajax/agregar_chofer.php | POST |  |  |  | inferred_file_route |
| index_archivos/tracking/ajax/borrarempresa.php | POST | index_archivos/tracking/js/empresatransporte.js:117 |  | tck_operadorestransporte | inferred_file_route |
| index_archivos/tracking/ajax/borrarparametros.php | POST | index_archivos/tracking/js/documentosempresatransporte.js:323 |  |  | inferred_file_route |
| index_archivos/tracking/ajax/buscar-partida.php | GET_OR_INCLUDE |  | dav_casos;dav_facturacomercial;dav_partidas |  | inferred_file_route |
| index_archivos/tracking/ajax/cargar-imagenes-viaje.php | POST |  | tck_registrareventos |  | inferred_file_route |
| index_archivos/tracking/ajax/comprobar_ci.php | POST |  |  |  | inferred_file_route |
| index_archivos/tracking/ajax/delete_trip.php | POST |  |  |  | inferred_file_route |
| index_archivos/tracking/ajax/discontinued-trip.php | POST |  |  |  | inferred_file_route |
| index_archivos/tracking/ajax/duplicar-viaje.php | GET |  |  |  | inferred_file_route |
| index_archivos/tracking/ajax/eliminarviaje.php | POST |  |  |  | inferred_file_route |
| index_archivos/tracking/ajax/getdocumentostransporte.php | POST | index_archivos/tracking/js/documentosempresatransporte.js:248 |  |  | inferred_file_route |
| index_archivos/tracking/ajax/getempresatransporte.php | POST | index_archivos/tracking/js/empresatransporte.js:146 |  |  | inferred_file_route |
| index_archivos/tracking/ajax/gettransportista.php | POST | index_archivos/tracking/js/documentosempresatransporte.js:268 |  |  | inferred_file_route |
| index_archivos/tracking/ajax/getunidadtransporte.php | POST | index_archivos/tracking/js/documentosempresatransporte.js:290 |  |  | inferred_file_route |
| index_archivos/tracking/ajax/guardarasigancionviaje.php | POST | index_archivos/tracking/js/asignarviaje.js:91 |  |  | inferred_file_route |
| index_archivos/tracking/ajax/guardardocumentoempresatransporte.php | POST | index_archivos/tracking/js/documentosempresatransporte.js:109 |  |  | inferred_file_route |
| index_archivos/tracking/ajax/guardarempresatransporte.php | POST | index_archivos/tracking/js/empresatransporte.js:57 |  |  | inferred_file_route |
| index_archivos/tracking/ajax/guardartransportista.php | POST | index_archivos/tracking/js/documentosempresatransporte.js:201 |  |  | inferred_file_route |
| index_archivos/tracking/ajax/guardarunidadtransporte.php | POST | index_archivos/tracking/js/documentosempresatransporte.js:153 |  |  | inferred_file_route |
| index_archivos/tracking/ajax/imagenes.php | POST |  |  |  | inferred_file_route |
| index_archivos/tracking/ajax/localizacion.php | POST | index_archivos/tracking/js/localizacion.js:54 |  |  | inferred_file_route |
| index_archivos/tracking/ajax/reasignacion-viajes/buscar-chofer-viaje.php | GET |  |  |  | inferred_file_route |
| index_archivos/tracking/ajax/reasignacion-viajes/datos-iniciales.php | GET |  |  |  | inferred_file_route |
| index_archivos/tracking/ajax/reasignacion-viajes/eliminar-destino.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/tracking/ajax/reasignacion-viajes/lista-choferes.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/tracking/ajax/reasignacion-viajes/lista-destinos-asignados.php | GET |  |  |  | inferred_file_route |
| index_archivos/tracking/ajax/reasignacion-viajes/lista-unidades.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/tracking/ajax/reasignacion-viajes/reasignar-viaje.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/tracking/ajax/unidadestransporte.php | POST | index_archivos/tracking/js/datostransporte.js:103 |  |  | inferred_file_route |
| index_archivos/tracking/ajax/uploadExcelCargaMasiva.php | POST | index_archivos/tracking/js/cargaMasiva.js:16 |  |  | inferred_file_route |
| index_archivos/tracking/ajaxAsignacion/borrar_ubicacion.php | POST |  |  | tck_location | inferred_file_route |
| index_archivos/tracking/ajaxAsignacion/conductores.php | GET |  |  |  | inferred_file_route |
| index_archivos/tracking/ajaxAsignacion/detalle_cliente.php | GET |  |  |  | inferred_file_route |
| index_archivos/tracking/ajaxAsignacion/editar_asignacion.php | GET |  |  |  | inferred_file_route |
| index_archivos/tracking/ajaxAsignacion/embarques.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/tracking/ajaxAsignacion/guardar_asignacion.php | GET |  |  |  | inferred_file_route |
| index_archivos/tracking/ajaxAsignacion/guardar_ubicacion.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/tracking/ajaxAsignacion/origen.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/tracking/ajaxAsignacion/parametros.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/tracking/ajaxAsignacion/transporte.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/tracking/asignacionviaje.php | GET |  |  |  | inferred_file_route |
| index_archivos/tracking/carga-masiva.php | GET |  |  |  | inferred_file_route |
| index_archivos/tracking/components/asignacion_viaje/aduana_ruta_plazo.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/tracking/components/asignacion_viaje/datos_generales.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/tracking/components/asignacion_viaje/datos_mercancia.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/tracking/components/asignacion_viaje/multimodal-programacion-embarque.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/tracking/components/asignacion_viaje/programacion_embarque-local.php | GET_OR_INCLUDE | index_archivos/js/formularios.php:116;index_archivos/js/formulariosA.php:116;index_archivos/js/formulariosB.php:116;index_archivos/js/formulariosR.php:116 |  |  | inferred_file_route |
| index_archivos/tracking/components/asignacion_viaje/programacion_embarque-nacional.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/tracking/components/asignacion_viaje/programacion_embarque.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/tracking/components/asignacion_viaje/terrestre-programacion-embarque.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/tracking/components/modal-edit-unity.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/tracking/components/modal-edit-user-transport.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/tracking/crear-viaje.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/tracking/documentosempresatransporte.php | GET |  |  |  | inferred_file_route |
| index_archivos/tracking/editar-viaje.php | GET |  |  |  | inferred_file_route |
| index_archivos/tracking/empresatransporte.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/tracking/generar_excel.php | GET |  |  |  | inferred_file_route |
| index_archivos/tracking/generar_excel_detalle.php | GET |  |  |  | inferred_file_route |
| index_archivos/tracking/getImage.php | GET |  |  |  | inferred_file_route |
| index_archivos/tracking/listaviajes.php | POST |  |  |  | inferred_file_route |
| index_archivos/tracking/ListaViajesClass.php | GET_OR_INCLUDE |  | dav_cliente;dav_unidad;dav_vehiculosprevios;logis_embarques;prov_clientes_proveedores;tck_asignacion_viaje;tck_carga;tck_empresa_transporte;tck_eventos;tck_imagenes;tck_localizaciones;tck_location;tck_operadorestransporte;tck_registrareventos;tck_registrarincidentes;tck_registros_entregas_recojos;tck_trackeo;tck_transportista;v_tck_infoviajecliente |  | inferred_file_route |
| index_archivos/tracking/localizacion.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/tracking/logistica-internacional.php | GET |  |  |  | inferred_file_route |
| index_archivos/tracking/logistica-local.php | GET | index_archivos/js/formularios.php:116;index_archivos/js/formulariosA.php:116;index_archivos/js/formulariosB.php:116;index_archivos/js/formulariosR.php:116 |  |  | inferred_file_route |
| index_archivos/tracking/logistica-nacional.php | GET |  |  |  | inferred_file_route |
| index_archivos/tracking/reporte-detalle-viaje.php | GET |  |  |  | inferred_file_route |
| index_archivos/tracking/reporte-viajes.php | POST\|GET | index_archivos/tracking/reporte-viajes.php:62 |  |  | inferred_file_route |
| index_archivos/tracking/TrackingNewClass.php | GET_OR_INCLUDE |  | dav_aduana;dav_cliente;dav_clientetransportista;dav_pais;dav_proveedor;dav_tipodeclaracion;dav_transportista;dav_unidad;ges_gestores_transporte;logis_contenedor;logis_edp;logis_embarques;logis_embarquesdatos;logis_embarquesmagnitudes;logis_embarquesoperador;logis_tipocarga;logis_tipoembarque;logis_tipomercancia;logis_tipomercanciaclase;logis_tipomercanciaun;logis_tipoviaje;logis_tramos;tck_asignacion_viaje;tck_carga;tck_documentos_soporte_lista;tck_documentossoporte;tck_empresa_transporte;tck_items_localizaciones;tck_localizaciones;tck_location;tck_operadorestransporte;tck_orden_viaje;tck_rutas;tck_rutasautorizadas;tck_transportista;tck_unidadestransporte | logis_edp;tck_asignacion_viaje;tck_carga;tck_documentossoporte;tck_empresa_transporte;tck_items_localizaciones;tck_localizaciones;tck_location;tck_orden_viaje;tck_rutasautorizadas;tck_transportista | inferred_file_route |
| index_archivos/tracking/viajedetalle.php | GET |  |  |  | inferred_file_route |
| index_archivos/usuario/ajax/update-password.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/usuario/editar-perfil.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/veriflogin.php | POST | index_archivos/login.php:92 | master_pass;prov_tipoproveedor;prov_usuarioaccesoproveedor |  | inferred_file_route |
| index_archivos/versolicitud.php | GET_OR_INCLUDE |  |  |  | inferred_file_route |
| index_archivos/versolicituddetalle.php | POST\|GET | index_archivos/versolicituddetalle.php:372;index_archivos/versolicituddetalle.php:472 |  |  | inferred_file_route |

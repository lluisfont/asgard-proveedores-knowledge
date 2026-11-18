# Referencias de datos observadas en master

Estado: candidatos de referencias SQL, sin DDL de master.
Tipos, claves, relaciones e invariantes fisicas quedan desconocidos.

| Tabla candidata | Lecturas | Escrituras | Fuentes de ejemplo |
| --- | ---: | ---: | --- |
| `Selected` | 1 | 0 | index_archivos/js/ux/form/ItemSelector.js:40 |
| `ada_agentesaduana` | 5 | 0 | index_archivos/embarques/CostosClass.php:142; index_archivos/embarques/CostosClass.php:329; index_archivos/reportes/reportecontroladquery.php:189 |
| `ada_agentescontactos` | 3 | 0 | index_archivos/embarques/componentes/embarques_detalle_gestion_aduanera.php:500; index_archivos/reportes/reportecontroladquery.php:188; index_archivos/reportes/reportecontrololquery.php:68 |
| `adaprov_agenteproveedor` | 1 | 0 | index_archivos/embarques/CostosClass.php:144 |
| `adaprov_agenteproveedormercancia` | 1 | 0 | index_archivos/embarques/EmbarqueClass.php:657 |
| `ads_agenteseguro` | 6 | 0 | index_archivos/embarques/EmbarqueClass.php:77; index_archivos/embarques/EmbarqueClass.php:271; index_archivos/embarques/EmbarqueClass.php:285 |
| `ages_solicitudes_asesoria_gestion` | 1 | 0 | index_archivos/embarques/componentes/estado-pedidos/controllers/EstadoPedidosClass.php:122 |
| `all` | 0 | 2 | index_archivos/js/datatables.js:2097; index_archivos/js/datatables.js:2782 |
| `capacidad` | 1 | 0 | index_archivos/tracking/TrackingClass.php:504 |
| `dav_aduana` | 18 | 0 | index_archivos/embarques/SolicitudesClass.php:41; index_archivos/embarques/SolicitudesClass.php:70; index_archivos/embarques/SolicitudesClass.php:104 |
| `dav_aerolineas` | 3 | 0 | index_archivos/embarques/EmbarqueClass.php:92; index_archivos/embarques/EmbarqueClass.php:417; index_archivos/embarques/SolicitudesClass.php:606 |
| `dav_casos` | 6 | 0 | index_archivos/embarques/CostosClass.php:569; index_archivos/embarques/SolicitudesClass.php:354; index_archivos/embarques/SolicitudesClass.php:395 |
| `dav_casosprevios` | 8 | 3 | index_archivos/embarques/CostosClass.php:572; index_archivos/embarques/SolicitudesClass.php:37; index_archivos/embarques/SolicitudesClass.php:723 |
| `dav_ciudad` | 21 | 0 | index_archivos/embarques/CostosClass.php:134; index_archivos/embarques/CotizacionClass.php:585; index_archivos/embarques/CotizacionClass.php:648 |
| `dav_cliente` | 44 | 0 | index_archivos/controllers/GlobalClass.php:95; index_archivos/controllers/GlobalClass.php:134; index_archivos/embarques/CostosClass.php:29 |
| `dav_clientealmacen` | 4 | 0 | index_archivos/embarques/CostosClass.php:226; index_archivos/embarques/CotizacionClass.php:538; index_archivos/reportes/reportecontroladquery.php:192 |
| `dav_clientelineas` | 30 | 0 | index_archivos/controllers/GlobalClass.php:76; index_archivos/embarques/CostosClass.php:145; index_archivos/embarques/CotizacionClass.php:434 |
| `dav_clientereportescliente` | 1 | 0 | index_archivos/controllers/GlobalClass.php:61 |
| `dav_clientetipoproducto` | 1 | 0 | index_archivos/embarques/SolicitudesClass.php:618 |
| `dav_clientetransportista` | 16 | 0 | index_archivos/controllers/GlobalClass.php:133; index_archivos/embarques/CostosClass.php:126; index_archivos/embarques/CotizacionClass.php:950 |
| `dav_clienteusuarios` | 4 | 0 | index_archivos/embarques/CostosClass.php:602; index_archivos/embarques/componentes/estado-pedidos/controllers/EstadoPedidosClass.php:42; index_archivos/embarques/componentes/estado-pedidos/controllers/EstadoPedidosClass.php:142 |
| `dav_codigos_2fa` | 1 | 3 | index_archivos/2fa/TwoFaClass.php:142; index_archivos/2fa/TwoFaClass.php:136; index_archivos/2fa/TwoFaClass.php:150 |
| `dav_contadorreportesclientes` | 0 | 1 | index_archivos/reporteexcel/reporteexcelNew.php:11 |
| `dav_dam` | 3 | 0 | index_archivos/embarques/SolicitudesClass.php:171; index_archivos/embarques/SolicitudesClass.php:231; index_archivos/embarques/SolicitudesClass.php:292 |
| `dav_damitems` | 3 | 0 | index_archivos/embarques/SolicitudesClass.php:170; index_archivos/embarques/SolicitudesClass.php:230; index_archivos/embarques/SolicitudesClass.php:291 |
| `dav_divisa` | 2 | 0 | index_archivos/embarques/CostosClass.php:455; index_archivos/embarques/CostosClass.php:570 |
| `dav_documentosprevios` | 2 | 2 | index_archivos/embarques/SolicitudesClass.php:744; index_archivos/embarques/SolicitudesClass.php:745; index_archivos/embarques/SolicitudesClass.php:743 |
| `dav_facturacomercial` | 1 | 0 | index_archivos/tracking/ajax/buscar-partida.php:11 |
| `dav_localidad` | 10 | 0 | index_archivos/controllers/GlobalClass.php:116; index_archivos/embarques/CostosClass.php:210; index_archivos/embarques/CostosClass.php:220 |
| `dav_meses` | 4 | 0 | index_archivos/js/formularios.php:756; index_archivos/js/formulariosA.php:734; index_archivos/js/formulariosB.php:750 |
| `dav_modotransporte` | 5 | 0 | index_archivos/embarques/EmbarqueClass.php:416; index_archivos/embarques/SolicitudesClass.php:42; index_archivos/embarques/SolicitudesClass.php:570 |
| `dav_modotransportedocumento` | 1 | 0 | index_archivos/embarques/SolicitudesClass.php:744 |
| `dav_navieras` | 2 | 0 | index_archivos/embarques/EmbarqueClass.php:418; index_archivos/embarques/SolicitudesClass.php:594 |
| `dav_otrosdocumentosprevios` | 5 | 9 | index_archivos/versolicituddetalle.php:66; index_archivos/versolicituddetalle.php:95; index_archivos/versolicituddetalle.php:140 |
| `dav_pais` | 25 | 0 | index_archivos/embarques/CostosClass.php:133; index_archivos/embarques/CostosClass.php:137; index_archivos/embarques/CostosClass.php:138 |
| `dav_partidas` | 1 | 0 | index_archivos/tracking/ajax/buscar-partida.php:12 |
| `dav_proveedor` | 37 | 0 | index_archivos/controllers/GlobalClass.php:102; index_archivos/embarques/CostosClass.php:132; index_archivos/embarques/CotizacionClass.php:353 |
| `dav_puerto` | 7 | 0 | index_archivos/embarques/CostosClass.php:135; index_archivos/embarques/CostosClass.php:211; index_archivos/embarques/CostosClass.php:221 |
| `dav_rating` | 1 | 1 | index_archivos/rating/RatingClass.php:27; index_archivos/rating/RatingClass.php:10 |
| `dav_regimen` | 5 | 0 | index_archivos/embarques/SolicitudesClass.php:40; index_archivos/embarques/SolicitudesClass.php:506; index_archivos/embarques/SolicitudesClass.php:534 |
| `dav_region` | 11 | 0 | index_archivos/embarques/CostosClass.php:222; index_archivos/embarques/CostosClass.php:234; index_archivos/embarques/CotizacionClass.php:1149 |
| `dav_reseteos_passswords_proveedores` | 2 | 2 | index_archivos/resetpassword/ResetPassword.php:47; index_archivos/resetpassword/ResetPassword.php:78; index_archivos/resetpassword/ResetPassword.php:20 |
| `dav_tipodeclaracion` | 5 | 0 | index_archivos/embarques/SolicitudesClass.php:546; index_archivos/reportes/reportecontroladquery.php:227; index_archivos/reportes/reportecontrololquery.php:106 |
| `dav_tipodocumento` | 1 | 0 | index_archivos/embarques/SolicitudesClass.php:744 |
| `dav_tipomercancia` | 2 | 0 | index_archivos/tracking/TrackingClass.php:270; index_archivos/tracking/TrackingClass.php:642 |
| `dav_tramites` | 1 | 1 | index_archivos/embarques/EmbarqueClass.php:688; index_archivos/embarques/SolicitudesClass.php:800 |
| `dav_transportista` | 12 | 0 | index_archivos/embarques/CostosClass.php:114; index_archivos/embarques/CotizacionClass.php:556; index_archivos/embarques/CotizacionClass.php:1028 |
| `dav_transportistamail` | 1 | 0 | index_archivos/versolicituddetalle.php:277 |
| `dav_unidad` | 8 | 0 | index_archivos/embarques/CostosClass.php:155; index_archivos/embarques/CotizacionClass.php:572; index_archivos/embarques/datoscaso.php:16 |
| `dav_usuario` | 9 | 0 | index_archivos/controllers/GlobalClass.php:88; index_archivos/embarques/SolicitudesClass.php:359; index_archivos/embarques/SolicitudesClass.php:400 |
| `dav_vehiculosprevios` | 5 | 1 | index_archivos/embarques/SolicitudesClass.php:169; index_archivos/embarques/SolicitudesClass.php:229; index_archivos/embarques/SolicitudesClass.php:290 |
| `dex_suma` | 1 | 8 | index_archivos/reportes/exportaciones/ajax/RecepcionFisicaMICs.php:94; index_archivos/reportes/exportaciones/ajax/ActualizarMICs.php:31; index_archivos/reportes/exportaciones/ajax/ActualizarMICs.php:33 |
| `dex_suma_estado_historial` | 0 | 1 | index_archivos/reportes/exportaciones/ajax/ActualizarMICs.php:18 |
| `failed` | 0 | 1 | index_archivos/data.php:8 |
| `ges_gestores_transporte` | 5 | 0 | index_archivos/embarques/CostosClass.php:146; index_archivos/embarques/SolicitudesClass.php:109; index_archivos/embarques/SolicitudesClass.php:233 |
| `intercambiodocumental` | 1 | 0 | index_archivos/reportes/reportecontroladquery.php:229 |
| `log_asgard_cloud` | 0 | 1 | index_archivos/logAsgard.php:15 |
| `logis_aeropuertos` | 3 | 0 | index_archivos/embarques/CotizacionClass.php:39; index_archivos/embarques/CotizacionClass.php:47; index_archivos/embarques/CotizacionClass.php:64 |
| `logis_categorias_costos` | 2 | 0 | index_archivos/embarques/CostosClass.php:342; index_archivos/embarques/CostosClass.php:401 |
| `logis_contenedor` | 9 | 0 | index_archivos/embarques/CostosClass.php:170; index_archivos/embarques/CostosClass.php:171; index_archivos/embarques/CotizacionClass.php:598 |
| `logis_costos` | 5 | 3 | index_archivos/embarques/CostosClass.php:445; index_archivos/embarques/CostosClass.php:509; index_archivos/embarques/CostosClass.php:583 |
| `logis_costos_concepto` | 2 | 0 | index_archivos/embarques/CostosClass.php:485; index_archivos/embarques/CostosClass.php:567 |
| `logis_costos_detalle` | 8 | 3 | index_archivos/embarques/CostosClass.php:426; index_archivos/embarques/CostosClass.php:548; index_archivos/reportes/reportecontroladquery.php:232 |
| `logis_costosconcepto` | 3 | 0 | index_archivos/embarques/CostosClass.php:36; index_archivos/embarques/CostosClass.php:251; index_archivos/embarques/costos.php:16 |
| `logis_costosdetalles` | 1 | 3 | index_archivos/embarques/costos.php:20; index_archivos/embarques/CostosClass.php:273; index_archivos/embarques/CostosClass.php:292 |
| `logis_cotizacion` | 3 | 0 | index_archivos/embarques/costos.php:14; index_archivos/embarques/datoscaso.php:14; index_archivos/embarques/datoscaso.php:16 |
| `logis_cotizacionoperador` | 1 | 0 | index_archivos/embarques/costos.php:18 |
| `logis_edp` | 58 | 3 | index_archivos/reportes/reportecontroladquery.php:193; index_archivos/reportes/reportecontroladquery.php:194; index_archivos/reportes/reportecontroladquery.php:195 |
| `logis_embarquereferencias` | 1 | 0 | index_archivos/embarques/CotizacionClass.php:1316 |
| `logis_embarques` | 48 | 8 | index_archivos/embarques/CostosClass.php:20; index_archivos/embarques/CostosClass.php:319; index_archivos/embarques/CostosClass.php:571 |
| `logis_embarquescontenedor` | 0 | 4 | index_archivos/embarques/CotizacionClass.php:726; index_archivos/embarques/CotizacionClass.php:1050; index_archivos/embarques/CotizacionClass.php:1227 |
| `logis_embarquesdatos` | 4 | 1 | index_archivos/embarques/CostosClass.php:113; index_archivos/embarques/CotizacionClass.php:819; index_archivos/tracking/TrackingNewClass.php:631 |
| `logis_embarquesdocumentos` | 4 | 5 | index_archivos/embarques/CostosClass.php:196; index_archivos/embarques/CotizacionClass.php:865; index_archivos/embarques/CotizacionClass.php:966 |
| `logis_embarquesmagnitudes` | 5 | 4 | index_archivos/embarques/CotizacionClass.php:826; index_archivos/embarques/CotizacionClass.php:1047; index_archivos/embarques/CotizacionClass.php:1224 |
| `logis_embarquesoperador` | 9 | 8 | index_archivos/controllers/GlobalClass.php:132; index_archivos/embarques/CostosClass.php:189; index_archivos/embarques/CotizacionClass.php:91 |
| `logis_embarquesrutas` | 0 | 2 | index_archivos/embarques/EmbarqueClass.php:434; index_archivos/embarques/EmbarqueClass.php:471 |
| `logis_estados` | 5 | 0 | index_archivos/embarques/CotizacionClass.php:179; index_archivos/embarques/EmbarqueClass.php:22; index_archivos/reportes/filtros/logis_estados.php:8 |
| `logis_estados_edp` | 6 | 0 | index_archivos/embarques/componentes/estado-pedidos/controllers/EstadoPedidosClass.php:40; index_archivos/embarques/componentes/estado-pedidos/controllers/EstadoPedidosClass.php:67; index_archivos/reportes/reportecontroladquery.php:260 |
| `logis_incoterms` | 6 | 0 | index_archivos/embarques/CostosClass.php:127; index_archivos/embarques/CostosClass.php:571; index_archivos/embarques/CotizacionClass.php:106 |
| `logis_libroventas` | 1 | 1 | index_archivos/cargarlibroventas_ajax.php:94; index_archivos/cargarlibroventas_ajax.php:107 |
| `logis_pedidos` | 2 | 1 | index_archivos/embarques/CostosClass.php:147; index_archivos/embarques/CotizacionClass.php:1343; index_archivos/embarques/CotizacionClass.php:1291 |
| `logis_pedidos_detalle` | 1 | 3 | index_archivos/embarques/CotizacionClass.php:1356; index_archivos/embarques/CotizacionClass.php:1300; index_archivos/embarques/CotizacionClass.php:1359 |
| `logis_tipocarga` | 14 | 0 | index_archivos/embarques/CostosClass.php:136; index_archivos/embarques/CostosClass.php:140; index_archivos/embarques/CostosClass.php:214 |
| `logis_tipoembarque` | 14 | 0 | index_archivos/embarques/CostosClass.php:128; index_archivos/embarques/CotizacionClass.php:161; index_archivos/embarques/EmbarqueClass.php:194 |
| `logis_tipomercancia` | 3 | 0 | index_archivos/embarques/CostosClass.php:129; index_archivos/embarques/CotizacionClass.php:217; index_archivos/tracking/TrackingNewClass.php:341 |
| `logis_tipomercanciaclase` | 3 | 0 | index_archivos/embarques/CostosClass.php:130; index_archivos/embarques/CotizacionClass.php:229; index_archivos/tracking/TrackingNewClass.php:372 |
| `logis_tipomercanciaun` | 3 | 0 | index_archivos/embarques/CostosClass.php:131; index_archivos/embarques/CotizacionClass.php:241; index_archivos/tracking/TrackingNewClass.php:388 |
| `logis_tipoviaje` | 13 | 0 | index_archivos/embarques/CostosClass.php:141; index_archivos/embarques/CotizacionClass.php:820; index_archivos/embarques/EmbarqueClass.php:193 |
| `logis_tramos` | 12 | 3 | index_archivos/embarques/EmbarqueClass.php:201; index_archivos/embarques/EmbarqueClass.php:216; index_archivos/embarques/EmbarqueClass.php:230 |
| `master_pass` | 1 | 0 | index_archivos/veriflogin.php:53 |
| `prov_clientes_proveedores` | 9 | 4 | index_archivos/embarques/CotizacionClass.php:1330; index_archivos/parametros/clientes/ClienteProveedorClass.php:47; index_archivos/parametros/ubicaciones/Ubicacion.php:42 |
| `prov_proveedorusuariospermisos` | 2 | 0 | index_archivos/MenuClass.php:17; index_archivos/MenuClass.php:33 |
| `prov_tipoproveedor` | 2 | 0 | index_archivos/veriflogin.php:75; src/core/users/application/Find/UserFind.php:30 |
| `prov_usuarioaccesoproveedor` | 15 | 3 | index_archivos/controllers/GlobalClass.php:109; index_archivos/embarques/CostosClass.php:608; index_archivos/embarques/CotizacionClass.php:1331 |
| `tck_aduanasrutasplazos` | 0 | 1 | index_archivos/tracking/TrackingClass.php:736 |
| `tck_asignacion_viaje` | 10 | 7 | index_archivos/embarques/EmbarqueClass.php:199; index_archivos/embarques/EmbarqueClass.php:214; index_archivos/reportes/reportecontroladquery.php:162 |
| `tck_asignacionesviajes` | 0 | 1 | index_archivos/tracking/TrackingClass.php:666 |
| `tck_capacidadestransporte` | 1 | 0 | index_archivos/tracking/TrackingClass.php:504 |
| `tck_carga` | 4 | 4 | index_archivos/reportes/reportetrackingnacionallocalquery.php:114; index_archivos/tracking/ListaViajesClass.php:67; index_archivos/tracking/ListaViajesClass.php:364 |
| `tck_choferoperador` | 4 | 3 | index_archivos/tracking/CommonsClass.php:15; index_archivos/tracking/TrackingClass.php:169; index_archivos/tracking/TrackingNewClass.php:22 |
| `tck_documentos_soporte_lista` | 1 | 0 | index_archivos/tracking/TrackingNewClass.php:494 |
| `tck_documentosoperadortransporte` | 2 | 3 | index_archivos/tracking/TrackingClass.php:68; index_archivos/tracking/TrackingClass.php:410; index_archivos/tracking/TrackingClass.php:80 |
| `tck_documentossoporte` | 1 | 3 | index_archivos/tracking/TrackingNewClass.php:1453; index_archivos/tracking/TrackingClass.php:765; index_archivos/tracking/TrackingNewClass.php:1351 |
| `tck_empresa_transporte` | 7 | 3 | index_archivos/embarques/ViajesClass.php:23; index_archivos/reportes/reportetrackingnacionallocalquery.php:117; index_archivos/tracking/ListaViajesClass.php:56 |
| `tck_eventos` | 4 | 0 | index_archivos/tracking/ListaViajesClass.php:195; index_archivos/tracking/ListaViajesClass.php:401; index_archivos/tracking/ReporteViajesClass.php:149 |
| `tck_imagenes` | 6 | 1 | index_archivos/tracking/ListaViajesClass.php:70; index_archivos/tracking/ListaViajesClass.php:75; index_archivos/tracking/ListaViajesClass.php:80 |
| `tck_items_localizaciones` | 1 | 4 | index_archivos/reportes/reportetrackingnacionallocalquery.php:169; index_archivos/tracking/TrackingNewClass.php:1317; index_archivos/tracking/controllers/CargaMasiva.php:490 |
| `tck_localizaciones` | 7 | 8 | index_archivos/reportes/reportetrackingnacionallocalquery.php:112; index_archivos/reportes/reportetrackingnacionallocalquery.php:156; index_archivos/tracking/CommonsClass.php:62 |
| `tck_location` | 4 | 6 | index_archivos/parametros/clientes/ClienteProveedorClass.php:98; index_archivos/tracking/ListaViajesClass.php:304; index_archivos/tracking/controllers/CargaMasiva.php:154 |
| `tck_lugaresentregacarga` | 8 | 0 | index_archivos/embarques/CostosClass.php:139; index_archivos/embarques/CostosClass.php:213; index_archivos/embarques/CostosClass.php:224 |
| `tck_operadorestransporte` | 6 | 3 | index_archivos/tracking/ListaViajesClass.php:59; index_archivos/tracking/ListaViajesClass.php:135; index_archivos/tracking/ListaViajesClass.php:260 |
| `tck_orden_viaje` | 1 | 2 | index_archivos/tracking/TrackingNewClass.php:1393; index_archivos/tracking/TrackingNewClass.php:1111; index_archivos/tracking/TrackingNewClass.php:1527 |
| `tck_programacionembarques` | 0 | 1 | index_archivos/tracking/TrackingClass.php:681 |
| `tck_registrareventos` | 10 | 0 | index_archivos/reportes/reportetrackingnacionallocalquery.php:75; index_archivos/reportes/reportetrackingnacionallocalquery.php:88; index_archivos/reportes/reportetrackingnacionallocalquery.php:100 |
| `tck_registrarincidentes` | 1 | 0 | index_archivos/tracking/ListaViajesClass.php:397 |
| `tck_registros_entregas_recojos` | 1 | 0 | index_archivos/tracking/ListaViajesClass.php:429 |
| `tck_rutas` | 2 | 0 | index_archivos/tracking/TrackingClass.php:654; index_archivos/tracking/TrackingNewClass.php:511 |
| `tck_rutasautorizadas` | 2 | 2 | index_archivos/tracking/TrackingNewClass.php:1081; index_archivos/tracking/TrackingNewClass.php:1617; index_archivos/tracking/TrackingNewClass.php:1340 |
| `tck_tiposcarguios` | 1 | 0 | index_archivos/tracking/TrackingClass.php:290 |
| `tck_tiposunidades` | 1 | 0 | index_archivos/tracking/TrackingClass.php:492 |
| `tck_tipoubicaciones` | 5 | 0 | index_archivos/parametros/ubicaciones/Ubicacion.php:43; index_archivos/parametros/ubicaciones/Ubicacion.php:55; index_archivos/tracking/controllers/CargaMasiva.php:155 |
| `tck_tmpcargamasiva` | 5 | 8 | index_archivos/tracking/controllers/CargaMasiva.php:88; index_archivos/tracking/controllers/CargaMasiva.php:113; index_archivos/tracking/controllers/CargaMasiva.php:121 |
| `tck_trackeo` | 3 | 0 | index_archivos/tracking/ListaViajesClass.php:66; index_archivos/tracking/ListaViajesClass.php:142; index_archivos/tracking/ListaViajesClass.php:267 |
| `tck_transporte` | 0 | 1 | index_archivos/tracking/TrackingClass.php:793 |
| `tck_transportista` | 11 | 3 | index_archivos/embarques/ViajesClass.php:22; index_archivos/reportes/reportetrackingnacionallocalquery.php:118; index_archivos/tracking/CommonsClass.php:78 |
| `tck_transportistausuario` | 3 | 2 | index_archivos/tracking/CommonsClass.php:11; index_archivos/tracking/CommonsClass.php:45; index_archivos/tracking/TrackingClass.php:444 |
| `tck_ubicaciones` | 2 | 2 | index_archivos/tracking/TrackingClass.php:327; index_archivos/tracking/TrackingClass.php:609; index_archivos/tracking/TrackingClass.php:242 |
| `tck_unidadestransporte` | 6 | 3 | index_archivos/tracking/CommonsClass.php:108; index_archivos/tracking/TrackingClass.php:112; index_archivos/tracking/TrackingClass.php:427 |
| `the` | 0 | 7 | index_archivos/js/datatables.js:1364; index_archivos/js/datatables.js:2879; index_archivos/js/datatables.js:5351 |
| `tmp_casosdampendientes` | 3 | 3 | index_archivos/embarques/SolicitudesClass.php:204; index_archivos/embarques/SolicitudesClass.php:264; index_archivos/embarques/SolicitudesClass.php:323 |
| `tmp_estadoEmbarque` | 2 | 4 | index_archivos/reportes/reportecontroladquery.php:186; index_archivos/reportes/reportecontrololquery.php:66; index_archivos/reportes/reportecontroladquery.php:253 |
| `tmp_eventos` | 1 | 1 | index_archivos/reportes/reportetrackingnacionallocalquery.php:119; index_archivos/reportes/reportetrackingnacionallocalquery.php:137 |
| `tmp_logisoperadorubicaciones` | 1 | 1 | index_archivos/parametros/ubicaciones/Ubicacion.php:254; index_archivos/parametros/ubicaciones/Ubicacion.php:243 |
| `v_tck_infoviajecliente` | 1 | 0 | index_archivos/tracking/ListaViajesClass.php:378 |

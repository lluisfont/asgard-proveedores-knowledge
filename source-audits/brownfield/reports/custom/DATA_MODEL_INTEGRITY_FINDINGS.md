# Data Model Integrity Findings - augmented pass

Status: REVIEW_REQUIRED

This pass inspects Brownfield's data dictionary for security and integrity gaps that the baseline leaves unclassified.

## Summary

- Sensitive-name columns: 1119
- FK-like columns without declared relation: 2509
- FK-like columns without declared relation in USED tables: 1310
- Table-level integrity findings: 844
- Critical tables without declared relations: 6

## Sensitive field flags

| Flag | Count |
| --- | ---: |
| `SENSITIVITY_UNKNOWN` | 1119 |
| `SENSITIVE_FIELD_NULLABLE` | 939 |
| `NO_INDEX_ON_AUTH_OR_TOKEN_FIELD` | 191 |

## Table flags

| Flag | Count |
| --- | ---: |
| `NO_CODE_USAGE_FOUND` | 519 |
| `TEMP_COPY_OR_BACKUP_TABLE` | 341 |
| `CRITICAL_TABLE_WITHOUT_DECLARED_RELATIONS` | 6 |

## Critical tables without declared relations

| Table | Usage | Read refs | Write refs |
| --- | --- | ---: | ---: |
| `dav_codigos_2fa` | `USED` | 1 | 0 |
| `dav_reseteos_passswords_proveedores` | `USED` | 1 | 1 |
| `master_pass` | `USED` | 1 | 0 |
| `prov_usuarioaccesoproveedor` | `USED` | 8 | 1 |
| `tck_asignacion_viaje` | `USED` | 8 | 5 |
| `tck_location` | `USED` | 5 | 3 |

## Highest density sensitive tables

| Table | Sensitive columns |
| --- | ---: |
| `dav_casos` | 50 |
| `dav_partidas` | 19 |
| `dav_davvehiculos` | 18 |
| `dav_dav` | 17 |
| `dav_damitems` | 15 |
| `dav_ciudad` | 13 |
| `dav_facturaplanilla` | 13 |
| `dav_casosprevios` | 11 |
| `dav_clienteusuarios` | 11 |
| `dav_casos_copy` | 10 |
| `dav_solicitudesprevias` | 10 |
| `dav_cliente` | 9 |
| `dav_proveedor` | 9 |
| `dav_reporte_transportistas_iasa` | 9 |
| `dav_tmp_proveedor` | 9 |
| `dav_usuario` | 9 |
| `logis_embarques` | 9 |
| `tmp_partidas` | 9 |
| `tmp_regularizacion` | 9 |
| `dav_clientetransportista` | 8 |
| `dav_demisitems` | 8 |
| `tmp_cotizaciones` | 8 |
| `tmp_cobrosdesglosado` | 8 |
| `dav_productosproveedor` | 7 |
| `prov_usuarioaccesoproveedor` | 7 |
| `rnc_noconformidad` | 7 |
| `tck_programacionembarques` | 7 |
| `tck_tmpcargamasiva` | 7 |
| `dav_subcliente` | 6 |
| `log_asgard_cloud` | 6 |
| `log_asgard_interno` | 6 |
| `tmp_solicitudes` | 6 |
| `tmp_liquidacion` | 6 |
| `ada_agentesaduana` | 5 |
| `ads_agenteseguro` | 5 |
| `dav_demissolicitud` | 5 |
| `dav_documentossumacampos` | 5 |
| `dav_tipodocumento` | 5 |
| `ges_gestores_transporte` | 5 |
| `log_ovp` | 5 |

## USED tables with FK-like gaps

| Table | Column | Indexed | Line |
| --- | --- | --- | ---: |
| `ada_agentesaduana` | `idcliente` | `false` | 26 |
| `ada_agentesaduana` | `idpais` | `false` | 27 |
| `ada_agentesaduana` | `created_by` | `false` | 45 |
| `ada_agentesaduana` | `updated_by` | `false` | 46 |
| `ada_agentesaduana` | `deleted_by` | `false` | 47 |
| `ada_clienteagenteaduana` | `idcliente` | `false` | 97 |
| `ada_clienteagenteaduana` | `idagenteaduana` | `false` | 98 |
| `adaprov_agenteproveedor` | `idpais` | `false` | 120 |
| `adaprov_agenteproveedor` | `created_by` | `false` | 123 |
| `adaprov_agenteproveedor` | `updated_by` | `false` | 125 |
| `adaprov_agenteproveedor` | `deleted_by` | `false` | 127 |
| `adaprov_agenteproveedormercancia` | `idagenteproveedor` | `false` | 155 |
| `adaprov_agenteproveedormercancia` | `idproveedor` | `false` | 156 |
| `adaprov_agenteproveedormercancia` | `created_by` | `false` | 157 |
| `adaprov_agenteproveedormercancia` | `updated_by` | `false` | 159 |
| `ads_agenteseguro` | `idcliente` | `false` | 181 |
| `ads_agenteseguro` | `idpais` | `false` | 182 |
| `ads_agenteseguro` | `created_by` | `false` | 199 |
| `ads_agenteseguro` | `updated_by` | `false` | 200 |
| `ads_agenteseguro` | `deleted_by` | `false` | 201 |
| `ages_asesoria_gestion_carpetas` | `solicitud_asesoria_gestion_id` | `false` | 288 |
| `ages_asesoria_gestion_carpetas` | `idciudad` | `false` | 293 |
| `ages_asesoria_gestion_carpetas` | `idcliente` | `false` | 294 |
| `ages_asesoria_gestion_carpetas` | `idaduana` | `false` | 298 |
| `ages_asesoria_gestion_carpetas` | `idtipodeclaracion` | `false` | 299 |
| `ages_asesoria_gestion_carpetas` | `idestado` | `false` | 300 |
| `ages_asesoria_gestion_carpetas` | `created_by` | `false` | 310 |
| `ages_asesoria_gestion_carpetas` | `updated_by` | `false` | 312 |
| `ages_asesoria_gestion_carpetas` | `deleted_by` | `false` | 314 |
| `ages_solicitudes_asesoria_gestion` | `solicitante_id` | `false` | 390 |
| `ages_solicitudes_asesoria_gestion` | `cliente_interno_id` | `false` | 391 |
| `ages_solicitudes_asesoria_gestion` | `cliente_id` | `false` | 392 |
| `ages_solicitudes_asesoria_gestion` | `casos_id` | `false` | 393 |
| `ages_solicitudes_asesoria_gestion` | `casos_extra_id` | `false` | 394 |
| `ages_solicitudes_asesoria_gestion` | `casos_previos_id` | `false` | 395 |
| `ages_solicitudes_asesoria_gestion` | `embarque_id` | `true` | 396 |
| `ages_solicitudes_asesoria_gestion` | `linea_id` | `false` | 397 |
| `ages_solicitudes_asesoria_gestion` | `ciudad_id` | `false` | 400 |
| `ages_solicitudes_asesoria_gestion` | `exchange_id` | `false` | 406 |
| `ages_solicitudes_asesoria_gestion` | `responsable_cierre_id` | `false` | 412 |
| `ages_solicitudes_asesoria_gestion` | `created_by` | `false` | 417 |
| `ages_solicitudes_asesoria_gestion` | `updated_by` | `false` | 419 |
| `ages_solicitudes_asesoria_gestion` | `deleted_by` | `false` | 423 |
| `cc_registro_documentos` | `tipo_documento_id` | `false` | 652 |
| `cc_registro_documentos` | `created_by` | `false` | 674 |
| `cc_registro_documentos` | `created_by_user` | `false` | 675 |
| `cc_registro_documentos` | `updated_by` | `false` | 677 |
| `cn_clienteconcesionario` | `idcliente` | `false` | 703 |
| `cn_clienteconcesionario` | `idconcesionario` | `false` | 704 |
| `cn_concesionario` | `idcliente` | `false` | 714 |
| `cn_concesionario` | `idpais` | `false` | 715 |
| `cn_concesionario` | `created_by` | `false` | 718 |
| `cn_concesionario` | `updated_by` | `false` | 720 |
| `cn_concesionario` | `deleted_by` | `false` | 722 |
| `dav_aerolineas` | `idpais` | `false` | 878 |
| `dav_anticipos` | `idcliente` | `false` | 988 |
| `dav_anticipos` | `idciudad` | `false` | 989 |
| `dav_anticipos` | `idempresa` | `false` | 990 |
| `dav_anticipos` | `idbanco` | `false` | 993 |
| `dav_anticipos` | `idtipotransferencia` | `false` | 994 |

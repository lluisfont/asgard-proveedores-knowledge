# Referencia API y contratos candidatos

AS-IS estatico del commit `a8ce2c23dead8552d2c4699e4a9b9134f7a18707`, rama `master`. Los candidatos requieren verificar configuracion y despliegue.

La aplicacion usa scripts PHP directos y llamadas AJAX. El catalogo actual contiene 241 candidatos de exposicion y 20 candidatos de consumo externo. No son rutas probadas mediante un servidor HTTP. Las peticiones de fichero, includes y paginas HTML pueden aparecer como candidatos junto a handlers JSON.

La auditoria nativa ASGARD no se ejecuto: Windows Application Control bloqueo el lanzador instalado. El catalogo procede de los escaneres de ampliacion y del cruce con las evidencias de Brownfield. Los antiguos ceros nativos de Peru no describen master.

## Catalogos

- [Handlers, callers y tablas](../crosswalk/screens-endpoints-tables.md).
- [Campos de peticion observados](../../source-audits/master/2026-11-18/request-fields.csv).
- [Catalogo JSON provisional](../../source-audits/master/2026-11-18/brownfield/custom/asgard-api-audit-augmented/api-catalog.augmented.json).
- [OpenAPI provisional](../../source-audits/master/2026-11-18/brownfield/custom/asgard-api-audit-augmented/openapi.augmented.yaml).
- [Riesgos por endpoint](../../source-audits/master/2026-11-18/brownfield/custom/api-deep-iterative/endpoint_deep_risks.csv).

## Interpretacion de respuestas

Un campo JSON `code` no acredita que el servidor devuelva ese estado HTTP. Los metodos y parametros se infieren de accesos a superglobales y callers; los parametros calculados, sus tipos completos y las ramas dinamicas requieren revision del handler. La autenticacion puede depender de includes y de la configuracion web. Las senales locales de CSRF, sesion o ausencia de ellas no sustituyen esa comprobacion.

## Llamadas externas observadas

| Metodo candidato | Destino/configuracion | Fuente | Linea | Senales |
| --- | --- | --- | --- | --- |
| GET_OR_UNKNOWN | UNRESOLVED_CONST:TRACKING_URL | index_archivos/tracking/viajedetalle.php | 580 | UNRESOLVED_BASE_CONSTANT |
| GET_OR_UNKNOWN | UNRESOLVED_CONST:TRACKING_URL/event/journey | index_archivos/tracking/ListaViajesClass.php | 205 | TLS_VERIFY_DISABLED;UNRESOLVED_BASE_CONSTANT |
| GET_OR_UNKNOWN | UNRESOLVED_CONST:URL_API | index_archivos/embarques/frames/inventario.php | 77 | CREDENTIAL_OR_KEY_IN_CALL;UNRESOLVED_BASE_CONSTANT |
| GET_OR_UNKNOWN | UNRESOLVED_CONST:URL_API/inventario/proveedores/reportes/buscar-chasis | index_archivos/reportes/inventario-por-chasis.php | 71 | CREDENTIAL_OR_KEY_IN_CALL;UNRESOLVED_BASE_CONSTANT |
| GET_OR_UNKNOWN | UNRESOLVED_CONST:URL_API/inventario/proveedores/reportes/resumen-inventario | index_archivos/reportes/inventario-por-chasis.php | 93 | CREDENTIAL_OR_KEY_IN_CALL;UNRESOLVED_BASE_CONSTANT |
| GET_OR_UNKNOWN | http://181.188.187.222/sistemas/clientes | .env-example.php | 22 | PLAINTEXT_HTTP |
| GET_OR_UNKNOWN | http://api-documents-dev.kpogroup.bo | .env-example.php | 23 | PLAINTEXT_HTTP |
| GET_OR_UNKNOWN | http://ip-api.com/json/ | index_archivos/2fa/TwoFaClass.php | 55 | PLAINTEXT_HTTP |
| GET_OR_UNKNOWN | https://api-documents-dev.kpogroup.bo | .env-example.php | 24 | CREDENTIAL_OR_KEY_IN_CALL |
| GET_OR_UNKNOWN | https://api.mapbox.com/styles/v1/ | index_archivos/tracking/js/asignarviaje.js | 146 | CREDENTIAL_OR_KEY_IN_CALL |
| GET_OR_UNKNOWN | https://api.sendgrid.com/v3/mail/send | index_archivos/embarques/EmbarqueClass.php | 542 |  |
| GET_OR_UNKNOWN | https://asgard.kpogroup.bo/sistemas/clientes/index_archivos/logistica/embarquever.php?id= | index_archivos/tracking/ajaxAsignacion/guardar_asignacion.php | 120 | CREDENTIAL_OR_KEY_IN_CALL |
| GET_OR_UNKNOWN | https://developer1.kpogroup.bo:4431/asesoria-gestion/public/index.php | .env-example.php | 27 |  |
| GET_OR_UNKNOWN | https://files-documents-dev.kpogroup.bo | .env-example.php | 25 | CREDENTIAL_OR_KEY_IN_CALL |
| GET_OR_UNKNOWN | https://maps.googleapis.com/maps/api/geocode/json?key= | index_archivos/parametros/ubicaciones/js/mapaEventoViaje.js | 68 | CREDENTIAL_OR_KEY_IN_CALL |
| GET_OR_UNKNOWN | https://maps.googleapis.com/maps/api/geocode/json?key=$ | index_archivos/tracking/vue/components/location.component.js | 104 | CREDENTIAL_OR_KEY_IN_CALL |
| GET_OR_UNKNOWN | https://maps.googleapis.com/maps/api/js?key= | index_archivos/embarques/frames/rutas.php | 196 | CREDENTIAL_OR_KEY_IN_CALL |
| POST | UNRESOLVED_CONST:TRACKING_URL/event/journey | index_archivos/tracking/ListaViajesClass.php | 206 | TLS_VERIFY_DISABLED;UNRESOLVED_BASE_CONSTANT |
| POST | UNRESOLVED_CONST:URL_API/enviar-whatsapp | index_archivos/tracking/TrackingNewClass.php | 971 | CREDENTIAL_OR_KEY_IN_CALL;TLS_VERIFY_DISABLED;UNRESOLVED_BASE_CONSTANT |
| PUT | UNRESOLVED_CONST:URL_API | index_archivos/embarques/frames/items.php | 43 | UNRESOLVED_BASE_CONSTANT |

Las constantes UNRESOLVED_CONST permanecen sin valor. No se contactaron servicios ni se verificaron contratos externos. Las credenciales detectadas se redactan.

# Deltas de consistencia semántica y contratos

Base de conocimiento `3822900b6d54d99ccf854bec43005a208e2a9694`. M `a8ce2c23dead8552d2c4699e4a9b9134f7a18707`; P `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62`.

**Entrega:** 2 mejoras, 2 hallazgos nuevos y 3 controles negativos. No se editaron documentos canónicos. La coordinación principal integra y cuenta los pases; esta entrega no declara convergencia global.

Técnicas: contratos JavaScript ejecutados con transporte sustituido; extracción PHP con tokenizer nativo; matriz de tipos y 64 combinaciones de prioridades; trazado formulario–handler–método; igualdad de objetos Git y falsación de namespaces.

Validación: `python -B scripts/audit/contract_consistency_probes.py`. PHP 8.4.25 y Node v24.19.0. Sin bootstrap, red, BD, almacenamiento de sesión ni escrituras de aplicación. El SQL local permanece `LOCAL_SCHEMA_CANDIDATE_UNVERIFIED`.

Prueba estructurada: `source-audits/master/2026-11-18/iterative/contract-consistency-probes.json`.

## TEMP-C1 — Corregir método y destino efectivos del inventario y del detalle de pedido

**improvement · AS-IS / RISK**

Afirmación actual exacta:

`knowledge/general/api-reference.md`

> | GET_OR_UNKNOWN | UNRESOLVED_CONST:URL_API/inventario/proveedores/reportes/buscar-chasis | index_archivos/reportes/inventario-por-chasis.php | 71 | CREDENTIAL_OR_KEY_IN_CALL;UNRESOLVED_BASE_CONSTANT |
> | GET_OR_UNKNOWN | UNRESOLVED_CONST:URL_API/inventario/proveedores/reportes/resumen-inventario | index_archivos/reportes/inventario-por-chasis.php | 93 | CREDENTIAL_OR_KEY_IN_CALL;UNRESOLVED_BASE_CONSTANT |

`knowledge/general/api-reference.md`

> | PUT | UNRESOLVED_CONST:URL_API | index_archivos/embarques/frames/items.php | 43 | UNRESOLVED_BASE_CONSTANT |

Corrección propuesta: Los dos reportes de inventario son POST: buscar-chasis recibe chasis; resumen-inventario recibe chasis y tipo_inventario_id. La línea 43 de frames/items.php es configuración en un input oculto, no una llamada PUT a la raíz URL_API. Su cadena activa es frame → datosEmbarques.js → ver_detalle_posiciones_pedido → GET proveedores/detalle-pedido/{idpedido}, con Authorization. Retirar esa falsa pareja método/destino y enlazar el llamador real. No recalcular aquí los 20 candidatos globales ni tratar base desconocida como método desconocido.

Validación: Ejecutar callbacks JavaScript reales en vm sin transporte, y seguir input/configuración → import de script → función → $.ajax(settings). Dos POST capturados con sus cuerpos y un GET de detalle. Ninguna petición real.

Control negativo: Un input que contiene URL_API no se cuenta como llamada; el método procede de settings.method, no de texto próximo.

Alcance: M; corrección precisa de knowledge/general/api-reference.md y contrato candidato vinculado. Backend y despliegue no probados.

Deduplicación: No es calidad del catálogo SQL134 ni exportación de consultas/SEC-006. Es una atribución errónea de método/destino HTTP demostrada y un cruce de caller omitido.

Evidencia:

- `a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/reportes/inventario-por-chasis.php:L68-L101`
- `a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/embarques/frames/items.php:L42-L44`
- `a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/embarques/frames/items.php:L99-L107`
- `a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/embarques/js/datosEmbarques.js:L1-L17`
- `3822900b6d54d99ccf854bec43005a208e2a9694:knowledge/general/api-reference.md:L28-L29`
- `3822900b6d54d99ccf854bec43005a208e2a9694:knowledge/general/api-reference.md:L44-L44`

## TEMP-C2 — Precisar nombres de estado de viaje y representación de cero por tipo PHP

**improvement · AS-IS / RISK**

Afirmación actual exacta:

`knowledge/glossary/business-glossary.json#/entries/69/usage_and_relationships`

> No se ha confirmado el nombre de todos sus códigos; no traducir el código de creación a un estado de embarque.

`knowledge/general/business-rules.md`

> | RN-25 | Estados mostrados | Casos del switch: 0 «Rechazado», 1 «Aceptado», 2 «Interrumpido», 3 «Completado», 4 «Borrador»; rama exterior nula «Asignado». La comparación exterior usa `<> null`, por lo que debe comprobarse en el PHP real la presentación del valor cero; la tabla lógica no garantiza su render | `M:index_archivos/tracking/listaviajes.php:L203-L236` |

Corrección propuesta: El switch de las dos ramas sí aporta nombres locales: 0 Rechazado, 1 Aceptado, 2 Interrumpido, 3 Completado y 4 Borrador; la rama exterior muestra Asignado. Separar ese mapa de la representación efectiva: con PHP 8.4.25, NULL e int 0 muestran Asignado, mientras string "0" muestra Rechazado. Los códigos 1–4 conservan la etiqueta con tipo entero o cadena. Sustituir la incertidumbre absoluta del glosario por estos nombres observados y conservar la distinción estado-viaje/estado-embarque. La prueba no decide el tipo devuelto por el driver desplegado ni valida PHP 5.4.

Validación: Evaluación del fragmento real de plantilla de cada pin, sin bootstrap; matriz NULL/int/string y control exhaustivo independiente de las prioridades del resumen. 11 representaciones por rama; 32 combinaciones de campos de resumen por rama; igualdad M/P en ambas matrices.

Control negativo: El string "0" no comparte la salida del entero 0; códigos 1–4 no presentan esa divergencia.

Alcance: M/P. Mejorar entrada estado-viaje, RN-25 y explicación del manual, sin convertir prueba PHP8.4 en prueba del entorno Docker5.4.

Deduplicación: RN-25 ya detectaba <> null y pedía comprobar el cero: esto es cierre parcial de incertidumbre y mejora semántica, no un nuevo defecto ni equivalencia con fn_obtener_estado.

Evidencia:

- `a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/tracking/listaviajes.php:L203-L236`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/tracking/listaviajes.php:L203-L236`
- `a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/tracking/TrackingNewClass.php:L1099-L1107`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/tracking/TrackingNewClass.php:L1099-L1107`
- `3822900b6d54d99ccf854bec43005a208e2a9694:knowledge/glossary/business-glossary.json:L2356-L2356`
- `3822900b6d54d99ccf854bec43005a208e2a9694:knowledge/general/business-rules.md:L48-L48`

## TEMP-C3 — El contador de inventario y el filtro Pendiente no comparten el mismo contrato de tipos

**new_finding · AS-IS / RISK**

Afirmación actual exacta:

`knowledge/variants/peru.md`

> | Inventario nacional/local | Cambia de `inventario/proveedores/lista-inventarios-locales/{tipo}` a `proveedores/inventarios-nacionales-locales/{tipo}/{embarque}`, cambia el cuerpo a `busqueda`, agrega filtros por VIN/kit/gas/concesionario/fechas y cuenta completados segun `pendiente`. [M llamada, L86-L109](https://github.com/KPO-Group/proveedores/blob/a8ce2c23dead8552d2c4699e4a9b9134f7a18707/index_archivos/embarques/componentes/inventario-local/tabla-vehiculos.js#L86-L109); [P filtros y llamada, L118-L188](https://github.com/KPO-Group/proveedores/blob/95fe9a4c3b3cddd84be922cc0e1eb9c88603df62/index_archivos/embarques/componentes/inventario-local/tabla-vehiculos.js#L118-L188). |

Corrección propuesta: Precisar que Completados cuenta todos los vehículos recibidos cuyo parseInt(pendiente) !== 1; incluye null, campo ausente, true y 2. En cambio, botón y filtro Pendiente exigen pendiente === 1. Así, una respuesta con "1" no se cuenta como completada pero desaparece del filtro Pendiente. El badge usa el conjunto recibido y no vehiculosVisibles: filtrar una fila de dos conserva total=2. RISK de contrato de datos: hace falta dominio y normalización consistentes en los consumidores; no afirmar que el backend real devuelve valores mal tipados ni que un completado acredita inspección realizada.

Validación: Ejecutar opciones Vue del blob real en Node vm; mutar solo fixture en memoria entre número, cadena, null, ausencia, booleano y valor fuera del dominio. 1 numérico: filtro=true, completados=0. "1": filtro=false, completados=0. null/ausente/true/2: completados=1. Una fila visible de dos: badge 1 de 2.

Control negativo: 0 y "0" producen completado; con ámbito local no se emite el contador nacional.

Alcance: Solo P y la cadena inventario-local/tabla-vehiculos → conteoInventario → inventario-local/index. M no contiene ese contador. Resultado del consumidor, sin respuesta API real.

Deduplicación: No duplica el cambio de URL/cuerpo ya recogido en comparación ni la separación de namespaces de inventario. La nueva diferencia es dominio/tipo de pendiente y población del agregado.

Evidencia:

- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/embarques/componentes/inventario-local/tabla-vehiculos.js:L75-L87`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/embarques/componentes/inventario-local/tabla-vehiculos.js:L162-L207`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/embarques/componentes/inventario-local/index.js:L8-L16`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/embarques/componentes/inventario-local/index.js:L147-L149`
- `3822900b6d54d99ccf854bec43005a208e2a9694:knowledge/variants/peru.md:L21-L21`

## TEMP-C4 — La edición amplía chasis por un camino distinto del alta local y puede ocultar el fallo del detalle

**new_finding · AS-IS / RISK**

Afirmación actual exacta:

`knowledge/glossary/business-glossary.json#/entries/23/usage_and_relationships`

> La creación automática revisada depende de un cliente concreto y del alcance local; no extenderla a todos los clientes o embarques.

`knowledge/general/business-rules.md`

> | RN-15 | Alta local, cliente 417 | Llama a creación de pedido desde `descripcioncarga`. En el formulario, entidad de sesión 333 y alcance local cambian OC y pedido a selección múltiple obligatoria. Son personalizaciones por ID observadas, no regla general de todos los clientes | `M:index_archivos/embarques/CotizacionClass.php:L686-L688,L1288-L1309`; `M:index_archivos/embarques/componentes/embarques_datos.php:L11-L79` |

Corrección propuesta: Añadir la ampliación al editar como recorrido separado del alta: el formulario solo muestra Agregar nuevos chasis para cliente417/local, pero editarController acepta nuevoschasis y editarCotizacionCliente ejecuta getPedidos → crearPedidosDetalle ante cualquier valor no vacío, sin volver a comprobar cliente/alcance. getPedidos toma el primer pedido sin ORDER BY ni filtro deleted_at; no crea cabecera si no existe. El método de detalle no retorna éxito ni propaga fallos de INSERT. Con retornos SQL false, la cabecera/descripcion pueden seguir actualizándose y la función superior devuelve code200. Documentar el alcance y la consistencia de esta edición; no describirla como creación de pedido nuevo ni extender la restricción de UI al servidor.

Validación: Extractor nativo token_get_all de tres métodos por pin; ejecución de los cuerpos reales con sustitutos mysql/mysqli en memoria y llamadas hijas de magnitudes/tramos neutralizadas. Cruce manual del form, include y POST. Cliente999/alcance1 con nuevoschasis sí alcanza INSERT de detalle en ambas ramas; vacío no lo alcanza. Pedido ausente e INSERT simulado false: devuelve code200 y alcanza UPDATE de descripción.

Control negativo: Cliente417/alcance3 también sigue la cadena; nuevoschasis vacío conserva solo actualización de cabecera.

Alcance: M/P. Distinción ausente en glosario/RN-15/flujos: alta condicionada versus ampliación de un pedido existente durante edición. AS-IS/RISK, sin explotación ni fallo de producción afirmados.

Deduplicación: No es el riesgo genérico de escrituras hijas del alta RN-14, ni el desajuste de aridad de CargaMasiva RN-34, ni un nuevo hallazgo de inyección SQL. La cadena nueva comienza en editarController y termina en crearPedidosDetalle.

Evidencia:

- `a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/embarques/editar.php:L110-L122`
- `a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/embarques/componentes/embarques_mercancia.php:L4-L23`
- `a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/embarques/editarController.php:L25-L33`
- `a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/embarques/editarController.php:L54-L56`
- `a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/embarques/CotizacionClass.php:L1195-L1206`
- `a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/embarques/CotizacionClass.php:L1342-L1367`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/embarques/editarController.php:L27-L38`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/embarques/editarController.php:L59-L63`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/embarques/CotizacionClass.php:L1209-L1223`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/embarques/CotizacionClass.php:L1397-L1422`
- `3822900b6d54d99ccf854bec43005a208e2a9694:knowledge/glossary/business-glossary.json:L889-L889`
- `3822900b6d54d99ccf854bec43005a208e2a9694:knowledge/general/business-rules.md:L33-L33`

## TEMP-C5 — Las siete igualdades de blob publicadas resisten el contraste independiente

**duplicate_or_rejected · AS-IS / CONTROL NEGATIVO**

Afirmación actual exacta:

`knowledge/variants/comparison.md`

> Se compararon los IDs de blob en los dos pins. Ejemplos de igualdad exacta:

Corrección propuesta: Sin corrección: los siete IDs de blob coinciden. Conservar la distinción ya publicada entre igualdad de archivo e igualdad de dependencias/configuración/despliegue.

Validación: git rev-parse pin:ruta para cada una de siete rutas y ambos pins. 7/7 iguales por objeto Git.

Control negativo: La igualdad del controlador no se extrapola a CotizacionClass ni a sus escrituras.

Alcance: Solo igualdad de los siete archivos de la tabla. No mide equivalencia funcional global.

Deduplicación: Control negativo de una afirmación existente; cero delta integrable.

Evidencia:

- `a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/embarques/embarquesController.php:L9-L20`
- `3822900b6d54d99ccf854bec43005a208e2a9694:knowledge/variants/comparison.md:L27-L39`

## TEMP-C6 — Los números compartidos de inventario pertenecen a namespaces distintos ya documentados

**duplicate_or_rejected · AS-IS / CONTROL NEGATIVO**

Afirmación actual exacta:

`knowledge/general/data-model.md`

> En inventarios P, VIN, kit, gas, destino, fechas, `pendiente`, `reportado` y estado llegan en respuestas API. Las vistas son evidencia de campos consumidos, no de tablas/columnas de su backend. Los inventarios preembarque 1/2/3 y los nacionales/locales 1/2/3/4/5 tienen contextos y parametros diferentes; compartir un numero no establece equivalencia ([P lista local, L118-L188](https://github.com/KPO-Group/proveedores/blob/95fe9a4c3b3cddd84be922cc0e1eb9c88603df62/index_archivos/embarques/componentes/inventario-local/tabla-vehiculos.js#L118-L188); [P tipos locales, L119-L126](https://github.com/KPO-Group/proveedores/blob/95fe9a4c3b3cddd84be922cc0e1eb9c88603df62/index_archivos/embarques/frames/inventario_local.php#L119-L126); [P preembarque, L443-L504](https://github.com/KPO-Group/proveedores/blob/95fe9a4c3b3cddd84be922cc0e1eb9c88603df62/index_archivos/preembarques/js/datosPreembarques.js#L443-L504)).

Corrección propuesta: Sin corrección: 1 significa DESPACHO NACIONAL en nacional/local y PRE EMBARQUE en preembarque. Los mapas locales1..5 sí coinciden entre M/P; eso no identifica los dos namespaces API. No crear una nueva equivalencia ni un nuevo hallazgo por ese solapamiento numérico.

Validación: Extracción independiente de asignación título→id en los frames reales de ambos pins. Mapas M/P locales iguales; preembarque1/2/3 con títulos distintos.

Control negativo: Igualdad numérica1 no supera la prueba de igualdad de etiqueta/contexto.

Alcance: Namespaces nacional/local versus preembarques, no catálogo del backend.

Deduplicación: Ya cubierto expresamente por data-model.md y variants/peru.md. Cero delta integrable.

Evidencia:

- `a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/embarques/frames/inventario_local.php:L33-L41`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/embarques/frames/inventario_local.php:L119-L127`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/preembarques/frames/inventario.php:L158-L166`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/preembarques/frames/inventario.php:L235-L245`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/preembarques/frames/inventario.php:L314-L324`
- `3822900b6d54d99ccf854bec43005a208e2a9694:knowledge/general/data-model.md:L43-L43`

## TEMP-C7 — El perfil SQL candidato no resuelve etiquetas de estado ni país

**duplicate_or_rejected · CANDIDATO / CONTROL NEGATIVO**

Afirmación actual exacta:

`source-audits/local-schema-candidate/2026-11-18/summary.json`

>   "status": "LOCAL_SCHEMA_CANDIDATE_UNVERIFIED",
>   "country": "unknown",
>   "matches_master_deployment": "not_verified",

Corrección propuesta: Sin corrección de autoridad. El candidato declara estado como int y cotizacion como tinyint(1); esos tipos no definen un enum de negocio ni prueban que tinyint(1) acepte solo0/1. Los nombres de columnas coincidentes no prueban país o despliegue. Para TEMP-C2/C3 se usa el consumidor real, sin sustituirlo por el candidato.

Validación: Contraste de nueve declaraciones de columnas candidatas con usos de código; lectura exclusiva del export estructural. 9 columnas presentes; país unknown, deployment not_verified. No lectura de datos ni cuerpos de rutinas.

Control negativo: No se asignan etiquetas de viaje, valores de company_type o identidad territorial a partir de INT/TINYINT/nombre de tabla.

Alcance: Solo declaraciones de source-audits/local-schema-candidate; no validar autoridad ni añadir restricciones físicas supuestas.

Deduplicación: Límite ya publicado; control negativo, sin repetirlo como hallazgo primario ni invadir el cruce SQLglot del proceso principal.

Evidencia:

- `3822900b6d54d99ccf854bec43005a208e2a9694:source-audits/local-schema-candidate/2026-11-18/columns.csv:L9756-L9756`
- `a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/tracking/TrackingNewClass.php:L1099-L1107`
- `a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/tracking/listaviajes.php:L203-L236`

## Integración y límites

TEMP-C1 corrige método/destino; TEMP-C2 amplía nombres y cierra parcialmente una incertidumbre conocida; TEMP-C3 añade un riesgo específico del contrato de respuesta; TEMP-C4 añade el camino de ampliación durante edición. Los demás registros son controles negativos y no deben incrementar el contador de novedades.

La prueba de retorno false de TEMP-C4 no predice si un driver desplegado lanzará una excepción. Las respuestas API son sintéticas; no se afirma que el backend real envíe null/cadenas/booleanos. La prueba de PHP8.4 no valida PHP5.4. El trabajo principal sobre SQLglot y exportación de consultas queda fuera de esta entrega.

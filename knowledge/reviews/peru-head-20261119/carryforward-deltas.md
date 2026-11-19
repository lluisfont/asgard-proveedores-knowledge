# Matriz de revalidacion de conocimiento Peru HEAD

Fecha cliente: **19-11-2026, Europe/Madrid**. Revision estatica lateral; no canonica.

| Fuente | Commit |
| --- | --- |
| P95 | `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` |
| HEAD | `2a179e2e6472d5705d031665ecbc90c3d806edec` |
| M_historical | `a8ce2c23dead8552d2c4699e4a9b9134f7a18707` |
| KB_baseline | `0c4bb99f076d6a8c18ae98375d6e154da6319922` |

## Cobertura y limite de las conclusiones

Arbol P95/HEAD: 10685/10685 entradas; 10682 identicas por modo/tipo/OID y tres paths cambiados. **Cero revisiones semanticas se atribuyen a esa igualdad global.**

Matriz: 103 registros; 81 glosario, nueve OPS, ocho mejoras operativas, cuatro BR y VAR-001. 175 citas P en Markdown, 115 rangos distintos. 62 documentos inventariados. Las pruebas detalladas estan en el JSON de auditoria.

Se preserva el significado y confianza del registro historico, sin repetir probes ni declarar aprobacion de negocio. Los rangos M se comparan separadamente; no acreditan por si solos conocimiento Peru. Citas de historia y prosa sin pin/rango no se promueven. Los 20 candidatos API raw siguen siendo candidatos.

Pruebas P95: {'IDENTICAL_RANGE': 615}. Comparacion historica M/HEAD: {'REQUIRES_RANGE_REVIEW': 85, 'IDENTICAL_RANGE': 66}. Los rangos M no coincidentes requieren otra revision si se pretende atribuirles comportamiento Peru; no son regresiones nuevas entre P95 y HEAD.

## Paths cambiados

| Path | Blob P95 | Blob HEAD | Tratamiento |
| --- | --- | --- | --- |
| `index_archivos/embarques/js/datosEmbarques.js` | `284278ae8b3de226b9a9326ff499f9a44d08bc86` | `8bfe0a4a253ce8f7401b4ae5ee2ee40e395fc4ed` | BOUNDED_BUSINESS_REQUEST_METADATA |
| `index_archivos/reportes/reportepreembarquenacional.php` | `a3b947856751f2e97ceca4eec056f636583d8bac` | `510ad3740fab4da9a4c711a18245f943f613f596` | DELEGATED_METADATA_ONLY |
| `index_archivos/reportes/reportepreembarquenacionalquery.php` | `189d9cba0c329e070c2b8618e7b93cba52e9d412` | `64d9e27cf0acae2bc21ead3c9d64603289f7e4c6` | DELEGATED_METADATA_ONLY |

## Precisiones propuestas

### TEMP-CF001 — El blob JS cambia; cinco solicitudes de negocio conservan rangos exactos

En HEAD los cinco contratos de solicitud acotados siguen identicos: detalle GET/Authorization, creacion POST JSON y tres catalogos GET. Creacion P95 L416-L421 pasa a HEAD L409-L414; detalle P95 L510-L521 pasa a HEAD L505-L516. Configuracion del frame y cuatro handlers locales conservan blob. Solo se arrastra esta evidencia de solicitud; callbacks, resultados, recarga y navegacion siguen excluidos.

**Deduplicacion:** IMP-C1 ya identifica el GET correcto en M; no se reabre como API nueva. Lo nuevo es la prueba P95/HEAD y sus rangos desplazados en el blob cambiado.

### TEMP-CF002 — Distinguir evidencia local estable de dependencia directa modificada

La matriz identifica por registro los frames/pantallas con referencias directas al JS cambiado. Sus blobs y citas pueden conservarse, pero esa igualdad no acredita el comportamiento compuesto. Las referencias a los reportes se inventarian sin leer sus cuerpos; sus cambios semanticos quedan en la tarea del otro agente. Los tres paths cambiados y sus vecinos no se convierten en una revision de todo el arbol.

**Deduplicacion:** La observacion remota de tres paths ya era conocida; aporta ahora propagacion directa por registro y pruebas de blobs/rangos en HEAD, no un nuevo hallazgo de frescura.

### TEMP-CF003 — La revalidacion Peru conserva la procedencia de las mejoras citadas solo en M

De 81 conceptos, 80 tienen evidencia P95; parte-recepcion solo M. Las nueve OPS, VAR-001 y cuatro BR tienen evidencia P. 6 de ocho mejoras operativas solo citan M: IMP-T008, IMP-T009, IMP-T010, CLR-IMP-001, RPR-IMP-001, RPR-IMP-002. Se registran coincidencias M/HEAD por rango cuando existen; no se promocionan a Peru ni se reutilizan lineas M como P. Las mejoras restantes con evidencia P conservan sus pins propios. Cualquier apoyo indirecto por un OPS/BR relacionado se mantiene separado del registro original.

**Deduplicacion:** No altera los mecanismos conocidos ni abre OPS nuevas; documenta la cobertura y procedencia del traslado al HEAD solicitado.

## Solicitudes de negocio acotadas en datosEmbarques.js

| ID | Metodo / destino | Rangos P95 → HEAD (pruebas) |
| --- | --- | --- |
| API-CF-001 | GET `UNRESOLVED_CONST:URL_API/proveedores/detalle-pedido/{idpedido}` | R0370: `index_archivos/embarques/js/datosEmbarques.js` L510-521 → L505-516; R0371: `index_archivos/embarques/frames/items.php` L57-57 → L57-57 |
| API-CF-002 | POST `index_archivos/embarques/ajax/crear-viaje-desde-items.php` | R0372: `index_archivos/embarques/js/datosEmbarques.js` L397-405 → L390-398; R0373: `index_archivos/embarques/js/datosEmbarques.js` L416-421 → L409-414; R0374: `index_archivos/embarques/frames/items.php` L238-238 → L238-238 |
| API-CF-003 | GET `index_archivos/tracking/ajaxAsignacion/transporte.php` | R0375: `index_archivos/embarques/js/datosEmbarques.js` L258-258 → L258-258; R0376: `index_archivos/embarques/frames/items.php` L239-239 → L239-239 |
| API-CF-004 | GET `index_archivos/tracking/ajaxAsignacion/origen.php` | R0377: `index_archivos/embarques/js/datosEmbarques.js` L265-265 → L265-265; R0378: `index_archivos/embarques/js/datosEmbarques.js` L269-269 → L269-269; R0379: `index_archivos/embarques/frames/items.php` L236-236 → L236-236 |
| API-CF-005 | GET `index_archivos/tracking/ajaxAsignacion/conductores.php?carrier_id={carrierBusinessId}` | R0380: `index_archivos/embarques/js/datosEmbarques.js` L303-303 → L303-303; R0381: `index_archivos/embarques/frames/items.php` L240-240 → L240-240 |

Los rangos anteriores contienen solo configuracion, parametros y solicitudes. No prueban respuesta, persistencia o servicio externo. No se analizan callbacks, salidas ni recarga. El catalogo documental API incluye filas de configuracion y atribuciones raw rechazadas: su numero no es un total de APIs validadas.

## Matriz por registro

C = evidencia P95 conservada por identidad; M = sin evidencia P original, sin promocion. D = referencia directa a path cambiado: requiere revision separada de esa frontera, sin invalidar automaticamente la cita local. Los IDs R apuntan a objetos Git, rangos inclusivos y SHA256 del JSON.

| Grupo | ID / titulo | Estado | Pruebas P / M |
| --- | --- | --- | --- |
| glossary | cliente-logistico — Cliente de la operación logística | C | R0001, R0002, R0003, R0004 |
| glossary | cliente-del-operador — Cliente propio del operador | C | R0005, R0006 |
| glossary | proveedor-mercancia — Proveedor de mercancía | C | R0007, R0008, R0009, R0010 |
| glossary | operador-logistico — Operador logístico | C | R0011, R0012, R0013, R0014 |
| glossary | empresa-transporte — Empresa de transporte del viaje | C | R0015, R0016 |
| glossary | conductor — Conductor | C | R0017, R0018, R0019, R0020 |
| glossary | conductor-relevo — Conductor de relevo | C | R0021, R0022 |
| glossary | gestor-transporte — Gestor de transporte | C | R0023, R0024 |
| glossary | agente-aduana — Agente de aduana | C | R0025, R0026, R0027, R0028 |
| glossary | agente-seguro — Agente de seguro | C | R0029, R0030 |
| glossary | agente-proveedor — Agente del proveedor de mercancía | C | R0031, R0032 |
| glossary | declarante — Declarante del cliente | C | R0033, R0034 |
| glossary | cotizacion — Cotización logística | C | R0035, R0036, R0037, R0038 |
| glossary | embarque — Embarque | C | R0037, R0038, R0039, R0040, R0041, R0042, R0043, R0044 |
| glossary | viaje — Viaje | C | R0045, R0046, R0043, R0044 |
| glossary | alcance-viaje — Alcance del viaje | C+D | R0047, R0048, R0049, R0050, R0051, R0052, R0053, R0054 |
| glossary | sentido-viaje — Sentido del viaje | C | R0055, R0056 |
| glossary | modalidad-transporte — Modalidad de transporte | C | R0057, R0058, R0059, R0060 |
| glossary | tramo — Tramo del embarque | C | R0061, R0062 |
| glossary | ruta-embarque — Ruta del embarque | C | R0063, R0064 |
| glossary | origen-destino — Origen y destino del viaje | C | R0065, R0066, R0067, R0068 |
| glossary | orden-compra — Orden de compra de referencia | C | R0069, R0070 |
| glossary | pedido-referencia — Pedido de referencia | C | R0069, R0070 |
| glossary | pedido-operativo — Pedido operativo | C | R0071, R0072, R0073, R0074 |
| glossary | item-posicion — Ítem o posición del pedido | C+D | R0075, R0076, R0077, R0078 |
| glossary | bulto — Bulto y tipo de bulto | C | R0079, R0080, R0081, R0082 |
| glossary | tipo-carga — Tipo de carga o carguío | C | R0083, R0084, R0085, R0086 |
| glossary | tipo-mercancia — Tipo de mercancía | C | R0087, R0088, R0085, R0086 |
| glossary | clase-mercancia — Clase de mercancía | C | R0089, R0090 |
| glossary | codigo-un — Código UN de mercancía | C | R0091, R0092, R0085, R0086 |
| glossary | incoterm — Incoterm seleccionado | C | R0093, R0094, R0095, R0096 |
| glossary | magnitudes-carga — Magnitudes de la carga | C | R0097, R0098 |
| glossary | contenedor — Contenedor | C | R0099, R0100, R0101, R0102, R0085, R0086 |
| glossary | peso-carga — Peso y peso bruto de la carga | C | R0081, R0082, R0103, R0104 |
| glossary | volumen-carga — Volumen de la carga | C | R0103, R0104 |
| glossary | almacen-cliente — Almacén del cliente | C | R0105, R0106 |
| glossary | propuesta-costos — Propuesta de costos del operador | C | R0107, R0108 |
| glossary | aceptacion-cotizacion — Aceptación de la cotización del operador | C | R0037, R0038 |
| glossary | revision-cotizacion — Revisión de cotización | C | R0109, R0110 |
| glossary | concepto-costo — Concepto de costo | C | R0111, R0112, R0113, R0114 |
| glossary | categoria-costo — Categoría de costo | C | R0115, R0116, R0117, R0118 |
| glossary | moneda-costo — Moneda del costo | C | R0119, R0120, R0121, R0122 |
| glossary | documento-adjunto — Documento adjunto del embarque | C | R0123, R0124 |
| glossary | documento-soporte-viaje — Documento de soporte del viaje | C | R0125, R0126 |
| glossary | solicitud-aduanera — Solicitud de gestión aduanera | C | R0127, R0128, R0129, R0130 |
| glossary | documento-previo — Documento previo de la solicitud | C | R0131, R0132 |
| glossary | caso-aduanero — Caso aduanero | C | R0133, R0134 |
| glossary | carpeta — Carpeta del caso | C | R0135, R0136, R0137, R0138 |
| glossary | tramite — Trámite de una solicitud | C | R0127, R0128 |
| glossary | regimen-aduanero — Régimen de la solicitud | C | R0139, R0140, R0141, R0142 |
| glossary | tipo-declaracion — Tipo de declaración | C | R0143, R0144, R0141, R0142 |
| glossary | aduana — Aduana seleccionada | C | R0145, R0146, R0147, R0148 |
| glossary | ruta-autorizada — Ruta autorizada del viaje | C | R0149, R0150 |
| glossary | cierre-transito — Fecha límite de cierre de tránsito | C | R0149, R0150 |
| glossary | dam — DAM en el control de solicitudes | C | R0151, R0152 |
| glossary | dui — DUI en la clasificación de despacho | C | R0153, R0154, R0155, R0156 |
| glossary | inventario-vehicular — Inventario del vehículo | C | R0157, R0158, R0159, R0160 |
| glossary | inventario-puerto — Inventario en puerto de carga | C | R0159, R0160 |
| glossary | inventario-deposito — Inventario de depósito transitorio | C | R0159, R0160 |
| glossary | inventario-post-nacionalizacion — Inventario post nacionalización | C | R0159, R0160 |
| glossary | inventario-nacional-local — Inventario de despacho y recepción | C | R0051, R0052 |
| glossary | chasis — Chasis como identificador de vehículo | C | R0157, R0158, R0075, R0076 |
| glossary | partida-inventario — Partida del inventario | C | R0161, R0162 |
| glossary | parte-recepcion — Parte de recepción | M | R0163 |
| glossary | desperfecto — Desperfecto del vehículo | C | R0164, R0165 |
| glossary | contaminacion — Contaminación en la revisión del vehículo | C | R0166, R0167 |
| glossary | accesorio — Accesorio inventariado | C | R0168, R0169 |
| glossary | estado-catalogo-embarque — Estado del catálogo de embarques | C | R0170, R0171 |
| glossary | edp — Estado de pedidos (EDP) | C | R0172, R0173 |
| glossary | estado-viaje — Estado de la asignación de viaje | C | R0049, R0050, R0174, R0175 |
| glossary | estado-resumen — Estado resumen calculado del embarque | C | R0137, R0138 |
| glossary | pendiente-resumen — Pendiente en el resumen del embarque | C | R0137, R0138 |
| glossary | enviado-resumen — Enviado en el resumen del embarque | C | R0137, R0138 |
| glossary | aceptado-resumen — Aceptado en el resumen del embarque | C | R0137, R0138 |
| glossary | en-proceso-resumen — En proceso en el resumen del embarque | C | R0137, R0138 |
| glossary | finalizado-resumen — Finalizado en el resumen del embarque | C+D | R0137, R0138, R0176, R0177 |
| glossary | estados-solicitud-aduanera — Estados de las listas de solicitudes aduaneras | C | R0178, R0179, R0180, R0181, R0182, R0183, R0184, R0185, R0186, R0187 |
| glossary | concesionario-cliente — Concesionario asociado al cliente | C | R0188 |
| glossary | viaje-desde-vin — Creación de viaje desde VIN seleccionados | C+D | R0189, R0190, R0191 |
| glossary | registro-kilometraje-imagen — Registro de kilometraje con imagen | C | R0192, R0193 |
| glossary | fotografias-360 — Fotografías 360° del inventario | C | R0194, R0195 |
| OPS | OPS-001 — El guardado de costos puede insertar detalles o borrar el maestro de otra petición | C | R0196, R0113, R0197, R0198 |
| OPS | OPS-002 — El resultado de localizaciones oculta fallos según su posición | C | R0199, R0067, R0200, R0201, R0202 |
| OPS | OPS-003 — La edición borra la carga y llama a su reemplazo con un argumento ausente | C | R0203, R0204, R0205, R0206, R0207, R0208, R0209 |
| OPS | OPS-004 — Crear un viaje marca como procesados todos los grupos del lote | C | R0210, R0211, R0212, R0213, R0214 |
| OPS | OPS-005 — La mezcla por posición puede duplicar u omitir eventos pendientes | C | R0215, R0216, R0217, R0218 |
| OPS | OPS-006 — La excepción del evento 26 falla si aparece en la primera posición | C | R0219, R0220 |
| OPS | OPS-007 — El servidor acepta un total de costos distinto de la suma de conceptos | C | R0221, R0222, R0223, R0224, R0225, R0226 |
| OPS | OPS-008 — La edición amplía chasis de un pedido existente sin verificar su selección y puede confirmar una actualización incompleta | C | R0227, R0228, R0229, R0230, R0231, R0232, R0233, R0234, R0235, R0236, R0237, R0238, R0239 |
| OPS | OPS-009 — La acción mostrartabla llama al listado de embarques sin el argumento logistica obligatorio | C | R0240, R0241, R0242, R0243, R0207, R0244, R0245 |
| operational_improvement | IMP-T008 — Precisar qué escrituras del viaje se comprueban y cuáles pueden fallar sin error | M | R0246, R0149, R0247, R0248 |
| operational_improvement | IMP-T009 — Distinguir fecha de modificación, interrupción y transición válida de estado | M | R0249, R0250, R0251, R0252, R0253, R0254 |
| operational_improvement | IMP-T010 — La conversión de fechas no valida el calendario ni acepta ISO | M | R0255, R0256, R0257 |
| operational_improvement | CLR-IMP-001 — El éxito del DELETE no demuestra filas borradas ni pérdida de carga | M | R0204, R0258 |
| operational_improvement | CLR-IMP-002 — La primera coincidencia26 en índice0 oculta también repeticiones posteriores | C | R0259, R0220 |
| operational_improvement | CLR-IMP-003 — Comprobar un retorno booleano inexistente también rechazaría adiciones exitosas | C | R0231, R0232, R0239, R0236 |
| operational_improvement | RPR-IMP-001 — El retorno de actualización debe separar filas coincidentes, cambios y una operación sin cambios permitida | M | R0251, R0250, R0249 |
| operational_improvement | RPR-IMP-002 — La reparación de pertenencia debe conservar IDs numéricos válidos recibidos como string | M | R0259, R0216 |
| branch_precision | BR-IMP-001 — Distinguir el intento automático de EDP de carga masiva M y P95 | C | R0211, R0260, R0261, R0262, R0248, R0263, R0264 |
| branch_precision | BR-IMP-002 — Fecharegistro frente a created_at puede cambiar la guardia26 con las mismas filas | C | R0216, R0265, R0215, R0218, R0217, R0266 |
| branch_precision | BR-IMP-003 — La referencia de lugar restringe la resolución en P95 pero no en M | C | R0267, R0268, R0269, R0270, R0271, R0272, R0273, R0274 |
| branch_precision | BR-IMP-004 — Acotar a M la sustitución incondicional de fecha/hora en el temporal masivo | C | R0275, R0276, R0277, R0278, R0279, R0280, R0281 |
| VAR | VAR-001 — El contador de inventario y el filtro Pendiente no comparten el mismo contrato de tipos | C | R0282, R0283, R0284, R0285 |

## Citas P por documento

| Documento | Ocurrencias |
| --- | --- |
| `knowledge/general/actors-and-permissions.md` | 2 |
| `knowledge/general/architecture.md` | 10 |
| `knowledge/general/business-rules.md` | 5 |
| `knowledge/general/data-model.md` | 11 |
| `knowledge/general/integrations.md` | 19 |
| `knowledge/general/operational-findings.md` | 16 |
| `knowledge/general/requirements-guide.md` | 3 |
| `knowledge/general/workflows.md` | 5 |
| `knowledge/reviews/iterative-20261118/closure-contracts.md` | 3 |
| `knowledge/reviews/iterative-20261118/closure-transactions.md` | 2 |
| `knowledge/reviews/iterative-20261118/contracts-delta.md` | 4 |
| `knowledge/reviews/iterative-20261118/transactions-delta.md` | 9 |
| `knowledge/variants/bolivia.md` | 4 |
| `knowledge/variants/comparison.md` | 28 |
| `knowledge/variants/peru.md` | 54 |

## Dependencias directas y exclusiones

389 aristas estaticas de un salto; 12 referencias lexicales a paths cambiados. Los includes literales y scripts tienen identidad propia y del destino; las referencias lexicales no prueban ejecucion. Includes dinamicos quedan sin resolver; no hay cierre transitivo. Las dependencias del servicio externo y gitlinks siguen fuera de verificacion.

- Dos PHP de reportes: solo blobs, modos y paths; semantica delegada a otro agente.
- Navegador, navegacion, salidas y JS de recarga: excluidos; no reintentados.
- datosEmbarques.js: solo hashes, rangos y solicitudes de negocio acotadas; sin callbacks de respuesta.
- Sin ejecucion PHP/JS, aplicacion, red, BD, submodulos, instalacion ni auditor nativo.
- Igualdad Git de todo el arbol no se cuenta como revision semantica de sus archivos.

Master remoto a44 queda fuera de alcance. No se modifica fuente, documentos finales o manifest; no hay commit ni push.

## Propuesta de cierre tras integrar novedades

Este pase construye identidad adelante P95->HEAD y dependencias de un salto. El cierre parte de cada afirmacion documental integrada, reconstruye su soporte hacia atras con git cat-file --batch, y desafia su suficiencia con mutaciones de metadatos.

**Precondicion:** Coordinador integra novedades aceptadas y aporta sidecar del otro agente para los dos reportes; no ampliar exclusiones.

1. Fijar el commit o snapshot documental integrado y su digest, H/P95/K/M; no consultar master remoto a44.
2. Para cada afirmacion integrada reconstruir claim->registro->rango->objeto Git usando un verificador independiente de este script y git cat-file --batch; calcular SHA256 otra vez, sin ejecutar PHP/JS.
3. Controles negativos en memoria: desplazar una linea, cambiar un OID, asignar pin M a P, eliminar una dependencia al JS y marcar como verificado un callback excluido. Deben fallar o quedar fuera de alcance, nunca pasar silenciosamente.
4. Control positivo: rangos reubicados de solicitudes (416-421->409-414 y510-521->505-516) conservan SHA256 y se aceptan solo como identidad acotada.
5. Contrastar por separado el sidecar delegado de reportes contra sus OIDs HEAD, sin reabrir cuerpos ni navegacion; ausencia de resultado impide cerrar ese dominio.
6. Registrar solo nuevas precisiones materiales o contradicciones con los IDs existentes; integrar cada novedad y reiniciar el conteo de pases sin delta que lleve el coordinador.

**Aceptacion:** Todos los registros y citas integrados trazables; controles negativos detectados; procedencia M/P correcta; dependencias cambiadas o excluidas visibles; cero deltas materiales en este pase independiente. No prueba runtime, red, BD, politica empresarial ni cierre global automatico.

**Estado:** propuesta pendiente; este trabajo no declara cierre global ni pases posteriores a la integracion.

## Reproduccion

`python -B scripts/audit/peru_head_carryforward.py --check` compara en memoria los tres sidecars con los objetos fijados. Sin `--check`, solo escribe los tres sidecars autorizados. El script solo usa stdlib y comandos Git de lectura; no carga el auditor bloqueado.

# Obligaciones diferenciales M / P95

**PASADA POSITIVA: 0 hallazgos independientes y 4 mejoras materiales aceptadas.** El principal aceptó BR-IMP-001..004 en la pasada9 y conserva el control del streak; esta no es una pasada sin delta.

M `a8ce2c23dead8552d2c4699e4a9b9134f7a18707`; P `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62`. Posterior a aceptación deCLR-IMP-001..003,RPR-IMP-001..002eIMP-SCOPE-001.

Differential obligation/data-lineage audit: follow triggers through producer predicates, parameter binding, ordered effects, consumer guards and returns in fixed M/P95. Compare the UPDATED operational registry. Relational candidate-set and crossed-timestamp witnesses; not blob equality, VM or a repeated type decision table.

## Alcance y registro actualizado

Se leyó [la observación remota](../../../source-audits/master/2026-11-18/iterative/remote-refs-observation.json), no el código2a. Todas las evidencias semánticas sonM/P95. Elaviso conocidoIMP-SCOPE-001está integrado alprincipio dePeru.md,sindelta adicional.

Se releyó operational-findings.json antes del veredicto:9OPS ylas3CLR vinculadas aOPS-003/006/008. No se modificó registro operativo oledger. Laaceptación deRPRporusuario prevalece sobre el estado propuesto anterior de su artefacto.

## Comparación de obligaciones

| ID | M | P95 | Conclusión |
| --- | --- | --- | --- |
| OPS-001 | SELECT último maestro por embarque/entidad alimenta detalle y DELETE si detalle=false. | Conserva claves de selección y dependencia del ID seleccionado; mysql no agrega identidad de petición. | Obligación no satisfecha en ambas; no equivale a runtime o persistencia iguales. |
| OPS-002 | statusSave se reemplaza solo tras INSERT favorable; save/edit consultan su retorno. | Mismos puntos de asignación y llamadas a subItems; no hay conjunción que abarque cada resultado. | Se mantiene la obligación en ambos pins; el comportamiento de excepciones SQL no se supone equivalente. |
| OPS-003 | DELETE favorable precede llamada4/5; filtros viaje/operador/embarque. | Conserva llamada4/5 y filtros; ninguna comprobación nueva de filas afectadas. | Falta de enlace común; CLR-IMP-001 limita pérdida en ambas. No se extrapola PHP8a5.4. |
| OPS-004 | Estado del lote por lote/cuenta; luego WhatsApp, intento EDP y success. | Mismo marcado de lote/cuenta; ruta masiva retorna tras WhatsApp sin registrarEdp. | OPS-004 se conserva. BR-IMP-001/003/004 precisan efectos y obligaciones de entradas que difieren entre variantes. |
| OPS-005 | Sobrescritura posicional; historial de fecharegistro. | Sobrescritura posicional; historial de created_at. | Causa posicional compartida, productor de orden distinto: BR-IMP-002. |
| OPS-006 | Primera coincidencia como condición sobre orden fecharegistro. | Misma condición, con orden created_at que puede cambiar índice inicial. | CLR-IMP-002 yRPR-IMP-002 se conservan; BR-IMP-002 añade productor de posición. |
| OPS-007 | totalCategory llega al maestro yamount a detalles sin reconciliación. | Los mismos campos llegan separados y no se observa suma nueva que limite el maestro. | No hay delta de país en esta obligación; no se infieren precisión monetaria ni constraints. |
| OPS-008 | Tras cabecera/magnitudes/tramos, nuevoschasis truthy activa getPedidos LIMIT1 y helper sin return; padre code200. | Agrega cabecera de concesionario para tipo1 y edición de operador para tipo7 antes de la cadena de chasis. Helper sigue sin return. | CLR-IMP-003 permanece. El registro actualizado ya aclara esos pasos P; no se declara igualdad de todos los efectos. |
| OPS-009 | Caller1formal contra2obligatorios; AJAX separado pasa5/2. | Caller1formal contra2obligatorios con firma enL173; AJAX separado pasa5/2. | Mismo sitio causal, sin exclusividad de país ni reparación observada. |
| VAR-001 | Inventario con controles de reportado pero sin evento conteoInventario. | Contador emitido solo en contexto nacional y filtro Pendiente distinto. | Atribución P/nacional se mantiene; sin repetir matriz de tipos ni VM. |
| CLR-IMP-001 | editLoad comprueba éxito de sentencia sin conteo. | Su homólogo mysql conserva esa puerta sin conteo. | Precisión aceptada compartida, sin delta. |
| CLR-IMP-002 | Primera coincidencia sobre fecha operativa. | Primera coincidencia sobre creación de registro. | Precisión de repetidos válida; diferencia aguas arriba enBR-IMP-002. |
| CLR-IMP-003 | Helper termina trasUPDATEsin return. | Mismo final sin return; concesionario previo no lo convierte enbooleano. | Precisión aceptada retenida en ambos; no se altera el código ni se ejecuta. |
| RPR-IMP-001 | Interrupción/editInfo no ofrecen ese resultado rico. | La variante mysql tampoco lo implementa. | TO-BE compartido; no se presume que mysql/mysqli cuenten cambios o coincidencias igual. |
| RPR-IMP-002 | IDdelSELECTse añade sin normalización antes de búsqueda no estricta. | También sin normalización, con orden SQL distinto. | Precisión aceptada se aplica aP95; no se atribuye a tipos reales de drivers o código2a. |
| IMP-SCOPE-001 | a8ceauditado coincide con observación remota. | 95fees comparación fijada;2asolo aparece en metadatos, sin leer sus3archivos. | Aviso conocido integrado al inicio dePeru.md; no agrega delta. |

## BR-IMP-001 — Distinguir el intento automático de EDP de carga masiva M y P95

**Precisión material propuesta; no nueva entradaOPS.**

Contexto actual: {"type": "missing_branch_distinction", "path": "knowledge/variants/peru.md", "claim": "Valida embarque nacional, bulto, unidad, conductor, origen y cobertura de destinos; reutiliza la carga masiva para crear el viaje.", "registry_comparison": "P aplica el mismo UPDATE de lote completo en590-591."}

El marcado de lote es común, pero M llama registrarEdp trasWhatsAppantes de éxito yP95no lo llama encrearViajede carga masiva. El helper existe en ambas ysaveordinario sí lo llama bajo asignación. Acotar EDPpor ruta/pin; el callerVINPusa la vía masiva, no saveordinario. No afirmar ausencia de EDPenproducción: otras rutas, triggers y éxito previo no se probaron.

Validación por trazado/predicados: {"path_M": ["batch_state_update", "sendWhatsapp", "registrarEdp_attempt", "success"], "path_P95": ["batch_state_update", "sendWhatsapp", "success"], "helper_conditions": ["cliente_resuelto", "sin_EDP129_activo"]}

Control negativo: Helper disponible ysaveordinario enPimpiden concluir que todoPerú carece de registro automático.

Evidencia:

- `a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/tracking/controllers/CargaMasiva.php:L574-L588`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/tracking/controllers/CargaMasiva.php:L590-L603`
- `a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/tracking/TrackingNewClass.php:L222-L224`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/tracking/TrackingNewClass.php:L222-L224`
- `a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/tracking/TrackingNewClass.php:L1635-L1648`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/tracking/TrackingNewClass.php:L1635-L1648`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/embarques/ajax/crear-viaje-desde-items.php:L256-L283`

## BR-IMP-002 — Fecharegistro frente a created_at puede cambiar la guardia26 con las mismas filas

**Precisión material propuesta; no nueva entradaOPS.**

Contexto actual: {"type": "scope_precision", "path": "knowledge/general/operational-findings.json#/findings/OPS-005/observed_behavior", "claim": "Se sobrescriben posiciones del catálogo con filas ordenadas por fecharegistro sin reconciliar IDs. Remotos[3,5,7] y detalle[5] producen[5,5,7]: desaparece pendiente3 y se duplica5. Detalle[3,3] produce[3,3,7], omitiendo5. El defecto demostrado es de representación, no modificación del historial SQL.", "comparison": "P conserva el ensamblado posicional en157-190."}

Acotar aMla descripción de detalle ordenado porfecharegistro: P95ordena por tck_registrareventos.created_at. El mismo consumidor posicional/primera coincidencia puede recibir otro orden. Corregir pertenencia/tipos no decide qué fecha debe gobernar el orden de negocio. Añadir distinción aOPS-005/006/variantes, sin inventar la fecha correcta ni significado de26.

Validación por trazado/predicados: {"same_rows": [{"event_id": 26, "fecharegistro": "2026-11-18 10:00:00", "created_at": "2026-11-18 12:00:00"}, {"event_id": 3, "fecharegistro": "2026-11-18 11:00:00", "created_at": "2026-11-18 09:00:00"}], "M_order": [26, 3], "P95_order": [3, 26], "first26_index_M": 0, "first26_index_P95": 1, "consequence": "Guardiaactual no retorna por26enMysíenP95; deducción de fuente, sinPHP/SQL."}

Control negativo: Si ambos timestamps inducen el mismo orden, no cambia la secuencia por este motivo. No se probaron empates ni datos reales.

Evidencia:

- `a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/tracking/ListaViajesClass.php:L387-L409`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/tracking/ListaViajesClass.php:L386-L408`
- `a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/tracking/ListaViajesClass.php:L157-L190`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/tracking/ListaViajesClass.php:L157-L190`
- `a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/tracking/viajedetalle.php:L89-L90`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/tracking/viajedetalle.php:L89-L90`

## BR-IMP-003 — La referencia de lugar restringe la resolución en P95 pero no en M

**Precisión material propuesta; no nueva entradaOPS.**

Contexto actual: {"type": "missing_branch_distinction", "path": "knowledge/variants/comparison.md", "claim": "VIN seleccionados → validacion → filas de carga masiva → crear viaje; filtra soft deletes y viajes existentes."}

Documentar queP95pasa referencia en callers de validación/carga ysuhelper inserta nombre/dirección o nombre/latitud/longitud si haytres segmentos. Mconstruye una condición pero no la interpola enSELECTyvarios callers solo pasan código/cuenta. Ambos usanLIMIT1: el filtroPno demuestra unicidad ni geografía correcta. No portar como contrato equivalente de código+referencia.

Validación por trazado/predicados: {"same_provider_code_locations": [{"id": 101, "provider": 11, "code": "C-01", "name": "ALFA"}, {"id": 102, "provider": 11, "code": "C-01", "name": "BETA"}], "reference": "BETA", "candidate_ids_M": [101, 102], "candidate_ids_P95": [102], "selected_first_row": "not_predicted_without_order"}

Control negativo: SinreferenciaPno agrega esa restricción. El ejemplo compara conjuntos candidatos, no filas realmente seleccionadas enSQL.

Evidencia:

- `a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/tracking/controllers/CargaMasiva.php:L132-L161`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/tracking/controllers/CargaMasiva.php:L134-L178`
- `a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/tracking/controllers/CargaMasiva.php:L438-L439`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/tracking/controllers/CargaMasiva.php:L454-L455`
- `a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/tracking/controllers/CargaMasiva.php:L518-L518`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/tracking/controllers/CargaMasiva.php:L534-L534`
- `a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/tracking/controllers/CargaMasiva.php:L632-L632`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/tracking/controllers/CargaMasiva.php:L647-L647`

## BR-IMP-004 — Acotar a M la sustitución incondicional de fecha/hora en el temporal masivo

**Precisión material propuesta; no nueva entradaOPS.**

Contexto actual: {"type": "missing_branch_distinction", "path": "knowledge/general/business-rules.md", "claim": "Inserta fecha/hora actuales, aunque O/P se hayan leído del Excel", "scope": "RN-31: evidenciaM, no regla común"}

MantenerRN-31comoMyañadirP95: el helper del temporal usa fechacarguio/horacarguio recibidos si no están vacíos, yCURRENT_DATE/TIMEsolo como fallback. O/Pdel lector yla rutaVINentregan esos campos. Acotar a expresiones preparadas para temporal: no confirma calendario, timezone, formato SQL aceptado ni toda programación delviaje.

Validación por trazado/predicados: {"nonempty_input": {"fechacarguio": "2030-12-01", "horacarguio": "14:30:00"}, "M_expression": ["CURRENT_DATE()", "CURRENT_TIME()"], "P95_expression": ["input_fechacarguio", "input_horacarguio"], "empty_P95": ["CURRENT_DATE()", "CURRENT_TIME()"]}

Control negativo: Concampos vacíosPtambién usa actuales. No se declara reparadocastDate ni persistencia de fechas.

Evidencia:

- `a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/tracking/controllers/CargaMasiva.php:L64-L80`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/tracking/controllers/CargaMasiva.php:L47-L48`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/tracking/controllers/CargaMasiva.php:L64-L82`
- `a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/tracking/ajax/uploadExcelCargaMasiva.php:L61-L73`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/tracking/ajax/uploadExcelCargaMasiva.php:L61-L73`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/embarques/ajax/crear-viaje-desde-items.php:L124-L138`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/embarques/ajax/crear-viaje-desde-items.php:L256-L258`

## Límites

- SoloM a8ceyP95fepara semántica; remoto2aes actualidad registrada, no fuente auditada. No se leen sus3archivos ni se declaralatestPerúrevisado.
- Sin ejecución de aplicación,VM,PHP/JSde negocio,SQL,BD,red,submódulos,navegador/navegación. Los modelos de orden yconjuntos ilustran predicados leídos.
- Predicados compartidos no prueban mismos efectos desplegados; mysql/mysqli,excepciones,configuración,triggersydatos noverificados.
- BR-IMPson propuestas documentales de ruta/variante, no nuevosOPS. No se modifica registro operativo,ledger,fingerprintsniotrasdocs.
- CLR/RPRson conocidas yaceptadas por elusuario;TO-BEnoes código implantado ni política empresarial aprobada.
- No se nombra26o129por número; no se infiere pérdida dequerytrue ni inexistencia de0cambios.
- Elprincipal decide aceptación ystreak. Hay4mejoras propuestas, no unpase global sindelta ni cierre de riesgos de producción.

Los16checks son`completed`: ejecución de esta revisión acotada, noPASSfuncional ni aceptación de sus propuestas. [Registro estructurado](closure-branch-obligations.json).

Aceptación posterior: las cuatro propuestas se integraron en [branch-obligations.json](branch-obligations.json). Esta evidencia conserva su naturaleza de pasada positiva con cuatro mejoras.

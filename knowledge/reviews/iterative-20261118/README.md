# Revisión iterativa: cambios frente a la auditoría anterior

Fecha: 18-11-2026. Knowledge 0.3.0. Comparación con la [auditoría anterior](https://github.com/lluisfont/asgard-proveedores-knowledge/commit/3822900b6d54d99ccf854bec43005a208e2a9694).

El código fuente sigue en master `a8ce2c23dead8552d2c4699e4a9b9134f7a18707`; contraste Perú `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62`. No hay cambios de aplicación ni correcciones desplegadas. Se amplía el conocimiento del mismo código.

**Delta aceptado: 11 hallazgos nuevos y 16 mejoras sustantivas de documentación.** Diez hallazgos se refieren a master (uno de seguridad y nueve operativos); uno corresponde específicamente al consumidor de inventario de Perú. Las coincidencias con Perú no certifican iguales datos/configuración.

**Cierre alcanzado:** las pasadas 10 y 11 no aportan nuevos hallazgos ni mejoras; mantienen la misma huella semántica que la versión 9.

El cierre se limita al alcance estático y los contratos aislados revisados. No certifica ausencia de defectos ni cierra los riesgos de producción.

## Qué ha cambiado

| ID | Cambio frente al informe anterior |
| --- | --- |
| SEC-015 | El exportador acepta operaciones SQL completas del cliente |
| IMP-AST-001 | Separar nombres léxicos, tablas en AST y esquema físico |
| OPS-001 | El guardado de costos puede insertar detalles o borrar el maestro de otra petición |
| OPS-002 | El resultado de localizaciones oculta fallos según su posición |
| OPS-003 | La edición borra la carga y llama a su reemplazo con un argumento ausente |
| OPS-004 | Crear un viaje marca como procesados todos los grupos del lote |
| OPS-005 | La mezcla por posición puede duplicar u omitir eventos pendientes |
| OPS-006 | La excepción del evento 26 falla si aparece en la primera posición |
| OPS-007 | El servidor acepta un total de costos distinto de la suma de conceptos |
| IMP-T008 | Precisar qué escrituras del viaje se comprueban y cuáles pueden fallar sin error |
| IMP-T009 | Distinguir fecha de modificación, interrupción y transición válida de estado |
| IMP-T010 | La conversión de fechas no valida el calendario ni acepta ISO |
| IMP-C1 | Corregir método y destino efectivos del inventario y del detalle de pedido |
| IMP-C2 | Precisar nombres de estado de viaje y representación de cero por tipo PHP |
| VAR-001 | El contador de inventario y el filtro Pendiente no comparten el mismo contrato de tipos |
| OPS-008 | La edición amplía chasis por un camino distinto del alta local y puede ocultar el fallo del detalle |
| OPS-009 | La rama mostrartabla omite un argumento obligatorio del listado |
| CLR-IMP-001 | El éxito del DELETE no demuestra filas borradas ni pérdida de carga |
| CLR-IMP-002 | La primera coincidencia26 en índice0 oculta también repeticiones posteriores |
| CLR-IMP-003 | Comprobar un retorno booleano inexistente también rechazaría adiciones exitosas |
| IMP-SCOPE-001 | Distinguir la comparación Perú fijada del nuevo HEAD remoto |
| RPR-IMP-001 | El retorno de actualización debe separar filas coincidentes, cambios y una operación sin cambios permitida |
| RPR-IMP-002 | La reparación de pertenencia debe conservar IDs numéricos válidos recibidos como string |
| BR-IMP-001 | Distinguir el intento automático de EDP de carga masiva M y P95 |
| BR-IMP-002 | Fecharegistro frente a created_at puede cambiar la guardia26 con las mismas filas |
| BR-IMP-003 | La referencia de lugar restringe la resolución en P95 pero no en M |
| BR-IMP-004 | Acotar a M la sustitución incondicional de fecha/hora en el temporal masivo |

Los hallazgos se sustentan en [aceptaciones estructuradas](accepted-deltas.json), [registro operativo](../../general/operational-findings.md), [SEC-015](report-query-contract.md), [contratos API revisados](../../general/api-reference.md), [variante Perú](../../variants/peru.md) y [glosario](../../glossary/business-glossary.md). Las propuestas iniciales conservan sus IDs temporales para poder revisar deduplicación y rechazos; su aceptación está registrada en [transacciones](transaction-integration.json) y [contratos](contract-integration.json).

Seguridad pasa de 14 a 15 hallazgos (ocho P1, siete P2); los nueve operativos se mantienen en un registro separado (dos P1, siete P2). No se suman marcas automáticas como vulnerabilidades. Se mantienen 81 conceptos de negocio, ahora con el estado de viaje mejor descrito y evidencias adicionales; no se inflan los recuentos con sinónimos o códigos.

El modelo de datos diferencia 134 nombres léxicos históricos, 100 nombres en AST MySQL y el esquema físico aún no verificado. De 394 fragmentos, 227 se interpretan y 167 quedan sin resolver. Cinco nombres AST no estaban en el inventario léxico. Los 39 no reproducidos no se eliminan como inexistentes. Los 20 candidatos raw de consumo API se conservan como historial; los POST reales y el falso PUT se corrigen mediante un overlay revisado.

Las reglas, procesos, manual, pruebas e índices enlazan las ampliaciones. Bolivia/master, Perú y el SQL local candidato siguen separados. El DDL histórico de Perú no se convierte en esquema general.

**Actualidad de ramas:** la verificación remota confirma master en el pin auditado, pero Perú avanzó a `2a179e2e6472d5705d031665ecbc90c3d806edec` durante el trabajo. Tres archivos difieren respecto al pin de comparación. [Observación reproducible de referencias](../../../source-audits/master/2026-11-18/iterative/remote-refs-observation.json). No se presenta este informe como auditoría de ese nuevo HEAD de Perú. Esta precisión de procedencia es IMP-SCOPE-001 y constituye la versión 7 con mejora.

## Pasadas y criterio de parada

| Versión | Técnica adicional | Nuevos | Mejoras |
| --- | --- | ---: | ---: |
| 1 | Contratos de consulta completa con despacho aislado | 1 | 0 |
| 2 | AST MySQL contrastado con inventario léxico y controles negativos | 0 | 1 |
| 3 | Inyección de fallos, intercalado sintético y permutaciones de invariantes | 7 | 3 |
| 4 | Diferencial de contratos M/P, callbacks sin transporte y matrices de representación | 2 | 2 |
| 5 | Censo de llamadas/firma mediante tokens PHP y fronteras de aridad | 1 | 0 |
| 6 | pinned-source def-use/postcondition review + finite relational selection + bounded metamorphic data models; no query fault injection | 0 | 3 |
| 7 | Verificación remota de referencias y diferencia de árbol para actualidad del alcance | 0 | 1 |
| 8 | counterfactual repair-obligation/discriminating success witnesses; Hoare-style postconditions on proposed TO-BE contracts | 0 | 2 |
| 9 | Differential obligation/data-lineage audit: follow triggers through producer predicates, parameter binding, ordered effects, consumer guards and returns in fixed M/P95. Compare the UPDATED operational registry. Relational candidate-set and crossed-timestamp witnesses; not blob equality, VM or a repeated type decision table. | 0 | 4 |
| 10 | Semantic mutation testing of pinned documentary claims: change country, timestamp, caller, conditional default or epistemic qualifier; positive and legitimate-equivalence controls. | 0 | 0 |
| 11 | Entailment-boundary audit: for each integrated accepted assertion, trace the source observation, reject its stronger counterassertion, and verify that qualification survives in the integrated text. Uses source slices, caller guards, candidate/selection distinctions and persistence/absence boundaries; no VM, repeated type matrix or blob-only validation. | 0 | 0 |

El [registro completo](iterations.json) conserva las huellas antes/después y los [snapshots acumulativos de cada versión](versions/audit-v01.json). Se compara el conjunto acumulado de afirmaciones aceptadas y sus evidencias, sin fechas ni nuevos archivos de log. Los últimos snapshots sin delta tienen el mismo contenido y hash de archivo. Repetir un test o reformular un riesgo conocido no cuenta como mejora. Cualquier delta sustantivo reinicia el contador.

Las técnicas combinan contrato de consulta completa, AST SQL, fallos programados, intercalado sintético, permutaciones de eventos, diferencias M/P, tipos PHP/JavaScript y un censo de aridad por tokens PHP. El último detectó OPS-009 y reinició el contador. Después, la revisión por modelos relacionales, postcondiciones y contraejemplos aportó tres precisiones más: DELETE correcto no garantiza filas borradas; importa la primera coincidencia del evento 26; y el detalle de pedidos devuelve NULL incluso en éxito. Es la versión 6 con novedades y reinicia otra vez el contador. Los cierres posteriores contrastan obligaciones entre ramas y la suficiencia lógica de las recomendaciones.

La versión 8 detecta dos mejoras de las recomendaciones: separar actualizaciones efectivas, no-op permitido y ausencia de coincidencia; y conservar IDs numéricos válidos recibidos como texto al corregir pertenencia. Son TO-BE condicionadas, sin convertirlas en política aprobada ni otro defecto. También reinician el contador. La revisión final usa contraste entre ramas y análisis abstracto de contratos, posterior a esas aceptaciones.

La versión 9 añade cuatro diferencias por rama: intento de registro EDP en la ruta masiva; fecha que ordena el historial; uso de referencia al resolver lugar; y origen de fecha/hora del temporal. Se integran en el [registro de obligaciones entre ramas](branch-obligations.md). La revisión abstracta anterior dio cero deltas, pero se descarta para el cierre final porque precede a estas cuatro precisiones. Tras integrarlas, el contador vuelve a cero y se realizan mutaciones semánticas documentales y una auditoría de límites de inferencia.

## Evidencia y comprobaciones

- [Reportes](../../../source-audits/master/2026-11-18/iterative/report-contract-probes.json): 3/3 contratos reproducidos sin DB.
- [Transacciones](../../../source-audits/master/2026-11-18/iterative/transaction-probes.json): 34/34 comportamientos reproducidos, incluidos 15 controles negativos.
- [Contratos](../../../source-audits/master/2026-11-18/iterative/contract-consistency-probes.json): tipos, callbacks registrados sin transporte, 32 combinaciones de resumen y 11 representaciones por rama.
- [Aridad estática](../../../source-audits/master/2026-11-18/iterative/static-arity-review.json): 279 PHP, 460 declaraciones, 542 llamadas resueltas, tres candidatos; dos ya conocidos y OPS-009 nuevo. Tres controles del analizador.
- [Firma aislada](../../../source-audits/master/2026-11-18/iterative/arity-contract-probes.json): 3/3; cuerpo sustituido por un centinela. No prueba el cuerpo real ni el PHP 5.4 declarado.
- [AST SQL](../../../source-audits/master/2026-11-18/iterative/sql-ast-summary.json): tres controles negativos. No se guarda SQL literal ni se ejecutan consultas.
- Cierres sin delta posteriores a todas las precisiones: [mutaciones semánticas documentales](closure-semantic-mutations.md), [límites de inferencia](closure-inference-boundaries.md).
- [Revisión por postcondiciones y modelos relacionales](closure-transactions.md): nueve comprobaciones; aporta CLR-IMP-001..003. La [revisión auxiliar de contratos y tipos](closure-contracts.md) se conserva como apoyo y no se usa como cierre posterior a esas precisiones.
- [Obligaciones de reparación frente a éxitos válidos](closure-repair-obligations.md): aporta RPR-IMP-001/002; tampoco se usa como pasada sin novedades.
- [Obligaciones diferenciales entre ramas](closure-branch-obligations.md): aporta BR-IMP-001..004. [Revisión abstracta auxiliar](closure-abstract-contracts.md): cero deltas antes de las cuatro precisiones de rama; no cuenta en el cierre posterior.
- [Validación actual](../../snapshots/current/knowledge-validation.json), [integridad de transferencia histórica](../../snapshots/current/transfer-validation.json) y [receta de reproducción](../../operations/reproduce-audit.md).

Las pruebas que reproducen un defecto pasan cuando confirman el comportamiento esperado por la auditoría; esto no aprueba ese comportamiento para negocio. No hubo bootstrap de aplicación, peticiones de aplicación, sesiones persistentes, datos reales, SQL ni mutaciones de fuente.

## Límites y revisión excluida

El estado global continúa **PARTIAL**: faltan correspondencia del DDL con el despliegue, privilegios y datos, runtime real, submódulos, autorización por entorno, concurrencia real y aprobación de negocio. El esquema local candidato conserva procedencia/país sin confirmar. Los efectos persistentes de fallos dependen de autocommit, restricciones y manejo de errores no comprobados.

La revisión delegada de salidas al navegador/navegación fue rechazada por la revisión automática de seguridad por posible riesgo de ciberseguridad antes de completarse. Sus artefactos parciales no se publican, no se integran y no cuentan como pasada sin novedades. El auditor nativo ASGARD sigue bloqueado por AppControl; no se eludió el bloqueo.

# Guía para analizar requisitos a partir del comportamiento actual

La [ampliación iterativa](../reviews/iterative-20261118/README.md) y sus [hallazgos operativos](operational-findings.md) añaden contraejemplos que deben entrar en cualquier propuesta de cambio: identidad del maestro de costos, alcance del lote, éxito parcial, composición de eventos y contratos de retorno. Las recomendaciones TO-BE permanecen pendientes de diseño y aprobación; documentar el defecto no lo convierte en requisito aceptable ni en corrección implementada.

Esta guía organiza el análisis de cambios; **no contiene requisitos de negocio validados**. Parte de observaciones de código del 18-11-2026 y propone preguntas y pruebas pendientes, diferenciadas de lo implementado.

Base `M`: `master` **a8ce2c23dead8552d2c4699e4a9b9134f7a18707**, inspeccionado en `C:/repos/proveedores-github-review-20261118`. Contraste `P`: `origin/master_peru` **95fe9a4c3b3cddd84be922cc0e1eb9c88603df62**, leído mediante `git show`. `M:ruta:Lx-Ly` y `P:ruta:Lx-Ly` fijan commit, ruta y líneas. Los IDs RN/F/A/U enlazan evidencias locales de las páginas citadas, no decisiones aprobadas del negocio.

Puntos de partida: [reglas implementadas](business-rules.md), [flujos](workflows.md), [actores y permisos](actors-and-permissions.md), [manual](user-manual.md), [Bolivia/master](../variants/bolivia.md) y [Perú](../variants/peru.md). Los documentos históricos de `knowledge/product/` y los artefactos Brownfield son antecedentes; no deben copiarse como especificaciones terminadas.

## Estados de una afirmación

| Estado | Cómo utilizarlo | Ejemplo de esta auditoría |
|---|---|---|
| **AS-IS observado en fuente** | Describir condición, entrada, acción y localización exacta | Guardar borrador inserta estado 4; asignar inserta NULL (`M:index_archivos/tracking/TrackingNewClass.php:L1099-L1107`) |
| **Inferido** | Explicar la interpretación y qué evidencia falta | Conviene revisar lista antes de reintentar porque hay persistencia por pasos; no se afirma duplicación ocurrida |
| **RISK** | Identificar una cadena concreta y un posible impacto | Catch de alta borra cabecera sin demostrar reversión de todos los hijos (`M:index_archivos/tracking/TrackingNewClass.php:L181-L235`) |
| **KNOWN DEFECT** | Reservar para fallo confirmado bajo condiciones reproducibles y registradas | No etiquetar automáticamente como defecto de producción un desajuste encontrado por inspección |
| **❓ Desconocido en ejecución** | Mantener abierta la verificación; no rellenar con comportamiento deseado | Qué copia `tck_duplicar_viaje` sin definición SQL ni ejecución (`M:index_archivos/tracking/TrackingNewClass.php:L947-L964`) |
| **TO-BE propuesto** | Registrar cambio solicitado y su alcance; no confundirlo con contrato actual | Que un borrador no genere comunicación sería un cambio frente a la llamada actual a WhatsApp, sujeto a decisión (`M:index_archivos/tracking/TrackingNewClass.php:L217-L224`) |
| **Validado por negocio** | Solo con decisión explícita, responsable, fecha y alcance documentados | Ninguna regla de estas cinco páginas tiene este estado por el solo hecho de estar escrita |

Una pantalla, un mensaje o una propuesta OpenSpec muestran intención de interfaz/diseño. Para acreditar persistencia hay que seguir controlador, método, SQL o contrato externo y respuesta. Un comentario/TODO no prueba una función operativa.

## Ficha mínima para cada solicitud de cambio

Complete una ficha por comportamiento y por variante afectada. Los elementos siguientes son campos de análisis, no una lista de requisitos ya aprobada:

| Campo | Contenido que debe quedar concreto |
|---|---|
| Identificador y problema | Tarea observable que necesita resolver el usuario, con ejemplo de entrada y resultado |
| Actor | Tipo de proveedor, cuenta frente a entidad, relación con cliente/operador y permiso de módulo |
| Variante y versión | Commit base, país/cliente y condición por ID si aplica; alcance compartido verificado |
| Disparador visible | Pantalla, etiqueta del botón y endpoint realmente utilizado |
| Entradas | Campos, tipos, unidades, formato de fecha, obligatorios de UI y obligatorios del servidor por separado |
| Precondiciones | Sesión, estado del registro, pertenencia de datos, catálogos y servicios necesarios |
| AS-IS | Secuencia leída, tablas o API afectadas, efectos secundarios y resultado devuelto |
| Cambio propuesto | Diferencia concreta respecto de AS-IS; decisiones aún no tomadas |
| Validación | Comprobación en UI, acción/controlador, método y base/API; indicar en qué capa se observó |
| Excepciones | Datos vacíos, estado no permitido, otro proveedor, inexistente, fallo SQL/API/correo, reintento y concurrencia |
| Consistencia | Qué queda escrito si falla un paso; si hay compensación y qué alcance real tiene |
| Evidencia | Commit/ruta/líneas, evidencia de llamada y persistencia, o contrato externo identificado |
| Criterios candidatos | Casos positivos/negativos expresados como propuestas de prueba, con oráculo verificable |
| Decisión/validación | Responsable, fecha, alcance y evidencia de aprobación; dejar pendiente si faltan |

No equiparar condición de menú con permiso de servidor. `MenuClass` construye opciones por cuenta, mientras `permisos.php` comprueba presencia de identidad y emite HTML de retorno; eso exige analizar cada acción completa (`M:index_archivos/MenuClass.php:L11-L44`; `M:index_archivos/permisos.php:L1-L27`). No inferir ausencia de controles con un único grep: leer inclusiones, función llamada y controles externos conocidos.

## Tres ejemplos trabajados, pendientes de decisión

### Ejemplo A: guardar un borrador de viaje

**AS-IS:** «Guardar Borrador» envía `isAssignment=0`; «GUARDAR Y ASIGNAR» envía 1 después de validación nativa. Guardar crea varias entidades y llama WhatsApp; EDP 129 solo se intenta al asignar. Evidencia: `M:index_archivos/tracking/vue/journey.page.js:L73-L95,L183-L188`; `M:index_archivos/tracking/TrackingNewClass.php:L181-L235,L1099-L1107,L1635-L1648` (RN-19–RN-23).

**❓ Decisiones pendientes:** si borrador debe comunicar al conductor; si sus campos mínimos son los mismos que al asignar; quién puede editarlo; qué hacer si guarda datos pero falla notificación. No se ha establecido que «borrador» signifique ausencia de efectos externos.

**Criterios candidatos de verificación, no ejecutados:** guardar y recuperar un borrador conserva estado 4; asignar conserva identidad del operador y produce estado NULL; fallo en escritura hija deja un estado recuperable definido; prueba con dos operadores comprueba aislamiento; comunicaciones se contrastan con un servicio simulado. Si negocio decide cambiar comunicaciones, actualizar tanto alta individual como carga masiva y edición según alcance acordado.

### Ejemplo B: resultado fiable de carga masiva

**AS-IS:** lector Excel2007 desde fila 3, descarta A/B vacías, crea temporal y valida referencias; modo viajes agrupa por B y anuncia éxito sin comprobar todos los códigos de creación. La inserción temporal usa fecha/hora actuales aunque lea O/P. Evidencia: `M:index_archivos/tracking/ajax/uploadExcelCargaMasiva.php:L29-L73,L203-L238`; `M:index_archivos/tracking/controllers/CargaMasiva.php:L23-L84,L279-L358` (RN-30–RN-34).

**Inferido:** una respuesta agregada puede ocultar fallos por grupo y un reintento puede duplicar grupos exitosos. No se ha observado un caso real ni se ha demostrado una estrategia de idempotencia global.

**❓ Decisiones pendientes:** política de todo-o-nada frente a éxito parcial; identificador estable para reintentos; tratamiento de fecha/hora del fichero; aislamiento de dos cargas simultáneas de la misma cuenta. El ID de lote por máximo+1 es un detalle técnico observado, no una numeración de negocio aprobada.

**Criterios candidatos:** un Excel sin filas útiles devuelve el error esperado; referencias inexistentes no se silencian; un lote con dos grupos y fallo simulado del segundo identifica exactamente cuál persistió; reintento de ese lote tiene resultado definido; valores importados se comparan con plantilla y datos guardados. No se han enviado cargas contra servicios reales.

### Ejemplo C: interpretar «entrega» en un reporte

**AS-IS:** Reporte OL calcula etapa con máximo `orden_etapa`, usa cliente fijo 429 y liga la columna «ENTREGA EN ALMACENCES DESTINO» al campo `inicio_transito_cbn`. Evidencia: `M:index_archivos/reportes/reportecontrololquery.php:L18-L21,L122-L145` (RN-44–RN-45).

**RISK:** el lector puede interpretar ese dato como entrega cuando el campo usado corresponde a otro hito. Es una discrepancia fuente/rótulo; ❓ su efecto en reportes reales depende de datos y uso.

**❓ Decisiones pendientes:** qué hito debe representar la columna, si el reporte sigue siendo específico del cliente 429 y qué calendario se considera en los KPI aduaneros. Las fórmulas fiscales y el umbral del 5% leídos en AD no son requisitos fiscales validados (`M:index_archivos/reportes/reportecontroladquery.php:L85-L133`).

**Criterios candidatos:** caso con inicio de tránsito y entrega en fechas distintas; comparar pantalla y Excel; verificar exclusiones por cliente/operador; dejar claro si Excel representa la consulta actual o una instantánea. El exportador actual vuelve a ejecutar consultas (`M:index_archivos/reporteexcel/reporteexcel.php:L13-L25,L50-L58`).

## Preguntas y evidencia necesaria por dominio

| Dominio | Base demostrada | Qué falta antes de validar un cambio |
|---|---|---|
| Identidad y permisos | Tipos 1–6, rama especial 99; mapeos de `UserFinder`; menú por cuenta | Catálogo real, valores de constantes de submódulo, significado del tipo 4 y comprobación de aislamiento; [actores](actors-and-permissions.md) A01–A17 |
| Sesión/MFA | Código de verificación separado de autenticación, caducidad y bloqueo | Enlace seguro entre pasos, controles de servidor/proxy, cuenta y canal usados, prueba de cookie efectiva; RN-01–RN-08 |
| Embarques | Campos, tramos, referencias, restricciones de listas y caso 417/local | Datos maestros y autoridad de cliente/operador; función SQL de estado; reglas sobre finalización; RN-09–RN-18 |
| Viajes | Borrador/asignación, escritura por pasos, acciones según estado | Definiciones SQL de copia/borrado, transición externa aceptado/completado, atomicidad y entrega de avisos; RN-19–RN-29 |
| Importaciones | Layouts y validaciones distintas para viajes y clientes propios | Plantilla realmente desplegada, errores de archivo, concurrencia, fecha/hora y recuperación; RN-30–RN-35 |
| Aduanas/documentos | Alta parcial admitida, metadatos/archivo y envío clásico | Ciclo operativo vigente, submódulos, alias de controlador y reglas de titularidad; RN-36–RN-39 |
| Costos | Categorías, reemplazo lógico, maestro/detalle y notificación | Reconciliar categorías con tipo de actor, moneda y total, aprobación real si se solicita; RN-40–RN-41 |
| Rating | INSERT y consulta para invitación a 30 días | Identidad del autor, rango/periodicidad de servidor, política de edición; RN-42–RN-43 |
| Reportes | Filtros, campos, fórmulas y reejecución en Excel | Semántica de hitos, calendario laboral, cliente fijo, resultados con datos controlados; RN-44–RN-47 |
| Inventario y Perú | Pantalla por chasis de M consume API; P añade otros módulos | Contrato/versionado y autorización del backend externo; no deducir persistencia de frontend; [Perú](../variants/peru.md) |

## Cómo decidir si algo es compartido o específico

1. Fijar ambos commits antes de comparar. Misma ruta no garantiza mismo comportamiento; un gitlink puede cambiar sin mostrar archivos internos.
2. Contrastar pantalla, botón, caller, handler y SQL/API; si solo se comparte el objeto versionado, afirmar igualdad de fuente, no igualdad de datos/despliegue.
3. Mantener separadas condición por país, por tipo de proveedor y por cliente/operador concreto. M ya usa IDs 417/429/333 y contiene inventario/pedidos internos; esos términos no bastan para clasificar un módulo como peruano.
4. Comprobar presencia/ausencia con el árbol Git completo y después leer el contenido. P aporta pantalla dedicada de pedidos, preembarques, tipo 7, creación desde ítems y vídeo. Referenciar [variantes](../variants/README.md), sin copiar todas sus reglas a la guía general.

Ejemplos de contraste directo: `M:index_archivos/embarques/CotizacionClass.php:L686-L688`; `M:index_archivos/embarques/embarquever.php:L252-L284`; `P:index_archivos/menu_b4.php:L148-L172`; `P:src/core/users/application/Find/UserFind.php:L25-L63`; `P:index_archivos/embarques/ajax/crear-viaje-desde-items.php:L1-L7`.

## Evidencia y validación que esta revisión no aporta

Los conteos comunicados en la coordinación de esta auditoría son cobertura instrumental: inventario master de 1.317 archivos y 1.091 evidencias (762 consultas SQL, 112 transiciones, 35 transacciones, 7 permisos y 175 candidatos de secretos); ampliación de 241 candidatos a endpoint, 87 referencias caller, 55 handlers con referencias y 15 no emparejados; grafo AST sobre 545 archivos seleccionados, con 319 sin símbolos. **No equivalen a 1.091 reglas correctas, siete controles totales, transacciones efectivas ni cobertura de runtime.** Los candidatos de secretos no se copian a documentación.

No se dispone de esquema SQL de aplicación con autoridad verificada en este inventario: cero tablas/columnas físicas extraídas no significa cero tablas usadas. Tampoco valida el dump histórico de Perú como modelo compartido. Las consultas revisadas son evidencia de uso, no garantía de restricciones o definición física.

No se utiliza el glosario genérico de tres términos autogenerado como glosario terminado. Los significados del dominio deben contrastarse con campos, pantallas y responsables. No se trasladan propuestas históricas a estado «implementado» sin seguir sus llamadas.

Asgard nativo **no ejecutado** por bloqueo de Windows App Control comunicado en la revisión. Se realizó inspección estática alternativa de interfaz/controladores/contratos API. El lint puntual con PHP CLI 8.4.25 de cuatro archivos no es prueba funcional ni compatibilidad con el PHP 5.4 declarado por `M:Dockerfile:L1-L6`; ese archivo y `M:index_archivos/cnfdb105.php:L11` fijan zona La Paz en la configuración leída.

Para cerrar una futura validación, registrar entorno y versiones reales, datos de prueba autorizados, resultados observados, evidencias de persistencia y decisión de negocio por alcance. Hasta entonces: documentación fuente verificable, riesgos y pendientes explícitos; **sin PASS funcional, sin aprobación de requisitos y sin promoción canónica**.

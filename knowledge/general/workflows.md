# Flujos funcionales reconstruidos desde código

Revisión del 18-11-2026, **AS-IS observado en fuente**. No se ejecutaron recorridos contra una aplicación o base de datos. Las secuencias de esta página reconstruyen llamadas reales; **❓ resultado en ejecución desconocido** cuando intervienen datos, servicios externos o dependencias no disponibles. Las consecuencias operativas recomendadas se identifican como inferencias, no como requisitos empresariales validados.

`M` = `master` **a8ce2c23dead8552d2c4699e4a9b9134f7a18707**, checkout `C:/repos/proveedores-github-review-20261118`; `P` = `origin/master_peru` **95fe9a4c3b3cddd84be922cc0e1eb9c88603df62**, contrastado con `git show`. Cada referencia `M:ruta:Lx-Ly` fija commit/ruta/líneas. Los IDs `F-*` son evidencia local de esta reconstrucción.

Consultar [actores y permisos](actors-and-permissions.md) antes de interpretar «puede acceder»; [reglas](business-rules.md) para condiciones y SQL; [manual](user-manual.md) para recorridos de usuario; [Bolivia/master](../variants/bolivia.md) y [Perú](../variants/peru.md) para diferencias de país.

## F-01. Acceder, renovar contraseña y cerrar sesión

**Actor/entradas:** cuenta de proveedor; nombre de usuario, contraseña, token CSRF y, opcionalmente, URL anterior. Precondiciones: sesión PHP, conexión y cuenta configuradas. [F01a]

1. Login crea token y lo envía al verificador.
2. El verificador consume token válido, valida formato/longitud, consulta cuenta y contraste de contraseña; verifica actividad y antigüedad de contraseña.
3. Si contraseña alcanza 90 días, deriva a cambio. Si requiere MFA, deriva al formulario que envía código al correo configurado. En caso normal, regenera ID de sesión, guarda entidad/cuenta/tipo/metadatos, genera JWT e intenta registrar acceso.
4. MFA verifica código y después la interfaz llama a autenticación. En el código revisado son dos endpoints; no se demuestra un vínculo de servidor entre ambas llamadas. **RISK de autenticación**, detallado en actores y permisos.
5. El menú ofrece «Perfil», «Volver a Ingresar» y «Salir». Perfil contrasta contraseña antigua y distinta; Salir destruye sesión. [F01a–F01c]

**Errores:** token inválido termina con 403; contraseña incorrecta, usuario inexistente, datos vacíos o cuenta inactiva se corresponden con errores 1–4. Las ramas iniciales de formato/longitud terminan antes del reenvío. Código MFA caduca tras 600 segundos; al superar tres fallos acumulados se inactiva la cuenta decodificada. ❓ No se probó entrega de correo ni cookie efectiva. [F01a, F01b]

**Control compartido:** pantallas y acciones suelen incluir `permisos.php`, que devuelve HTML de retorno si falta `idtransportista`; no termina la ejecución ni comprueba módulo. El guardián específico de descargas sí termina con 403. Esta diferencia es parte del flujo, no una conclusión global sobre todas las rutas. [F01d]

**Recuperación distinta de MFA:** «olvidé mi contraseña» abre tres pasos: nombre/apellido/usuario o correo → «Siguiente» y generación de solicitud/correo; código → «Siguiente» y verificación/consumo; contraseña/confirmación → «Finalizar» y actualización. Falla por usuario no comprobado, registro o correo; verificación puede informar token expirado. La caducidad se calcula con inicio del día actual, no diez minutos. **RISK:** el paso final usa el identificador devuelto sin volver a verificar token/antigüedad en la cadena leída; ❓ seguridad efectiva y entrega no probadas. [F01e]

## F-02. Localizar un embarque y abrir sus áreas

**Entradas/precondiciones:** entidad/tipo en sesión y permisos de menú; alcance internacional/nacional/local. El subenlace preciso procede del catálogo, no está fijado por la etiqueta del grupo. [F02a]

1. «Logística» → «Embarques» abre listado del alcance. `ajax/listaEmbarques.php` convierte alcance a 1/2/3 y pasa entidad de sesión a `EmbarqueClass`.
2. SQL aplica relación por tipo de proveedor, alcance y borrado lógico. Tipo 1 combina participación aceptada y propiedad; los tipos 2–6 usan columnas de relación diferentes.
3. Línea y rango de creación se aplican en servidor; las búsquedas de DataTables se incorporan a la consulta. Se construyen resumen de viajes, estado y botones por fila.
4. «Ver» abre `embarquever.php?id=...&t=...`; obtiene datos del ID y permisos del grupo 6. Carga áreas mediante iframes, algunos al seleccionar pestaña: «Gestión Logistica», «Gestión Aduanera», «Costos», «Documentos», «Tracking», «Inventario», «Crear Viaje», «Descripción de Items» y «Estado de Pedidos», con condiciones de tipo y contenido. Crear Viaje exige además que el embarque no tenga fecha de finalización. No todas son visibles en todos los casos. [F02b, F02c]

**Alternativa:** lupa del menú, si existe permiso `#buscador_global`; etiqueta «Pedido/FC/Embarque», «Buscar» y resultado «Abrir». Navegador pide al menos cuatro caracteres, trata vacío y error de red. [F02d]

**Efectos:** consulta; no se demuestra cambio de estado por abrir un detalle. **❓** La función SQL `fn_obtener_estado` no tiene definición verificada en el inventario de esta auditoría. La restricción del listado no prueba por sí misma que cada vista y acción vuelva a validar propiedad. [F02b, F02c]

## F-03. Crear un embarque desde el formulario

**Actor/precondición UI:** tipo 1; «Crear Embarque» se ofrece si alcance distinto de nacional. El formulario admite alcance y carga catálogos; algunas opciones están particularizadas por cliente/operador. [F03a]

**Entradas observadas:** Solicitante (`idcliente`), OC (`ordencompraini`), Pedido (`ordencompra`), modalidad (`idtipoembarque`), Incoterm para internacional, descripción, tipo de mercancía, clase/UN o temperatura, magnitudes/bultos y tramos. Solicitante/modalidad e Incoterm internacional llevan `required`; no afirmar obligatoriedad universal del resto. [F03b]

1. «Crear Embarque» abre `embarquecrear.php?v=...`.
2. Selección de mercancía muestra/oculta clase/UN/temperatura; modalidad elige componentes de tramos. Para operador 333 en local, OC/Pedido se convierten en selección múltiple obligatoria.
3. «Guardar» deshabilita botón, aplica `checkValidity()` y envía formulario multipart a `embarquesController.php`. Si falla navegador, muestra `reportValidity()` y rehabilita botón.
4. Controlador toma entidad de sesión, construye campos (arrays de referencias unidos por `;`, Incoterm por defecto 12 si falta), marca `cotizacion=0` y llama a `guardarCotizacionCliente`.
5. Método inserta cabecera, magnitudes y tramos; en cliente 417/local llama además a creación de pedido. Controlador redirige al listado del alcance. [F03a–F03d]

**Efectos:** `logis_embarques`, `logis_embarquesmagnitudes`, contenedores si corresponde, `logis_tramos` y pedido específico. **RISK:** método devuelve ID de cabecera sin comprobar retornos de magnitudes/tramos; redirección al listado no acredita alta íntegra. No se demuestra una transacción común en esta cadena leída. Inferencia operativa: confirmar el registro y sus datos antes de repetir el alta tras un error. [F03c, F03d]

**Variante de importación:** en local aparece «IMPORTAR EXCEL». El flujo carga temporal y devuelve datos al formulario; al guardar, el controlador intenta generar viaje. Existe desajuste de aridad (dos argumentos frente a tres declarados en `crearViaje`); ❓ no está validado en runtime. No se ofrece como recorrido fiable hasta comprobarlo. [F05a, F05c]

## F-04. Preparar, asignar y consultar un viaje

**Entradas/precondiciones:** entidad operadora de sesión, embarque o modo de viaje independiente del formulario; datos de alcance/modalidad/pedido/referencia, proveedor/mercancía/peso, empresa/placa/unidad, conductor y relevo, carga, origen(es), destino(s), documentos y rutas. No se presume que tipo 6 tenga idéntica UI que tipo 1. [F04a, F04b]

1. `crear-viaje.php` presenta «SELECCION DE EMBARQUE» y selección de fila cuando corresponde. El campo anuncia búsqueda por pedido/cliente, pero su filtro compara número y pedido y limita a diez resultados.
2. Componente carga datos y parámetros desde endpoints, permite completar transporte/conductor/localizaciones/carga.
3. «Guardar Borrador» envía `isAssignment=0`; «GUARDAR Y ASIGNAR» envía 1. Ambos aplican validación nativa del formulario y POST JSON a `ajaxAsignacion/guardar_asignacion.php?id=embarque`.
4. El endpoint usa entidad de sesión y transforma el JSON a objetos de dominio. `TrackingNewClass::save` escribe información, orden, empresa, conductor, carga, localizaciones y documentos; luego rutas/relevo/ubicaciones.
5. Cabecera queda estado 4 (borrador) o NULL (asignado). La función llama a WhatsApp para el conductor en ambos caminos; solo al asignar intenta añadir EDP 129 si no existe. Después el endpoint intenta correo/notificación/Pusher.
6. Interfaz muestra número y «Viaje Creado correctamente»; «Lista de Viajes» conduce al listado filtrado por operador. [F04a–F04d]

**Errores/consistencia:** fallos comprobados de los pasos principales lanzan excepción; catch borra cabecera por ID y devuelve 100. No es evidencia de rollback de todos los hijos. Error de `save` se convierte en HTTP 400; éxito atraviesa además integraciones antes de responder. **RISK:** persistencia y notificación no son un único resultado garantizado; un error de red no prueba que el viaje no exista. Edición tiene actualizaciones parciales y no hace limpieza en catch. [F04c, F04d]

**Seguimiento:** lista/detalle usan registros locales, última posición y consulta externa de eventos; documentos se asocian a eventos concretos. Si la consulta remota devuelve vacío, el ensamblador conserva detalle previo. ❓ No se han verificado actualización en vivo, reloj, aceptación/completado desde otra aplicación ni veracidad física de los hitos. [F04e]

## F-05. Cargar viajes por Excel y mantener prerrequisitos

**Precondiciones:** códigos de clientes propios y ubicaciones, origen, placa, conductor relacionado y tipo de bulto existentes. Sesión de proveedor y fichero compatible con lector Excel2007. La pantalla enlaza plantilla `FormatoCargaMasivaViajes.xlsx`. [F05a, F05b]

1. Seleccionar «Archivo» y pulsar «Cargar Archivo». El POST multipart va a `tracking/ajax/uploadExcelCargaMasiva.php`.
2. Lector recorre hoja activa desde fila 3; solo acepta filas con A y B no vacías. Lee A–V, incluyendo número de viaje, códigos, origen, placa, conductor y carga.
3. Se borran temporales no procesados de la cuenta; se obtiene lote por máximo+1 y se insertan filas en `tck_tmpcargamasiva`. Aunque Excel contiene fecha/hora O/P, esta inserción usa fecha/hora actuales.
4. Validador resuelve datos maestros y acumula observaciones por fila. La respuesta colorea filas, explica mensajes y, sin observaciones, agrupa por número de viaje.
5. En modo viajes llama a creación por cada grupo y devuelve números creados; **no hay un segundo botón de confirmación de creación en este camino**. En modo embarque, «Importar datos al embarque» devuelve datos al formulario padre para su guardado posterior. [F05a–F05c]

**Errores:** status 100 por observaciones o ausencia de filas; no hay garantía de que el lector gestione como JSON todos los errores de formato. El agregador no comprueba cada código de creación antes de anunciar status 200. **Inferencia operativa:** tras una carga, revisar IDs y contenido en lista antes de reintentar, para evitar duplicación. [F05a]

**Preparación de catálogos:** importación de clientes propios usa primera hoja desde fila 2, A–G; el código de ciudad se compara con `dav_ciudad.iddav`; ciudad desconocida se convierte en SQL NULL. No es el mismo layout que los viajes. [F05d]

## F-06. Consultar gestión aduanera y documentos de solicitud

**Precondiciones:** embarque internacional con pestaña habilitada, solicitud y relaciones con agente/gestor. `frames/aduanas.php` selecciona consultas distintas para tipo 6, tipo 5 y resto. Algunos caminos de creación dependen además de `idcliente` en sesión; ❓ su disponibilidad en todos los accesos no se ha probado. [F06a]

1. Abrir «Gestión Aduanera»; la página muestra «Pendientes» y «Enviados», y algunos encabezados adicionales según agente configurado.
2. La columna «Ver» abre solicitud `SOL-...` dentro del frame; hay secciones históricas de Revisión documental/En Proceso/Despacho cuyo contenido está comentado. No reconstruir un ciclo completo solo con esos rótulos.
3. Alta técnica de gestión toma declaración/régimen/aduana, fechas, transporte, solicitante, mercancía y vínculos con embarque; inserta caso previo y documentos por modo de transporte más documento tipo 9.
4. El método informa éxito incluso si falló inserción de documentos, con mensaje específico «pero sin documentos». Edición y eliminación tienen reglas independientes; eliminación física encadena tablas sin comprobar cada resultado. [F06a, F06b]

**Recorrido clásico alternativo:** `versolicitud.php` lista solicitudes aprobadas/no anuladas/no liquidadas de la entidad; detalle permite documentos complementarios y «Enviar Documentos». El envío intenta correo y cambia documentos de transportista 0/3 a `enviado=1, estado=1`. No confundir envío de archivos con aprobación aduanera. [F06c]

**RISK y dependencia:** en `versolicituddetalle.php` la inclusión inicial de `permisos.php` está comentada; también integra una ruta del sistema de clientes para intercambio documental. Su mera presencia en el repositorio no acredita disponibilidad autónoma ni acceso seguro. ❓ Validar política y rutas en un despliegue aislado. [F06c]

## F-07. Adjuntar documentación de embarque

**Entradas:** archivo y IDs de embarque/cliente; sesión y almacenamiento configurado. [F07a]

1. «Documentos» carga el frame. Si los datos incluyen `idExchange`, delega en `intercambioDocumental/lista_intercambios_documentales.php`; si no, presenta formulario clásico.
2. Formulario clásico: «Seleccionar Archivo» → «Agregar documento». Nombre de archivo en tabla enlaza descarga; papelera tiene título «Eliminar».
3. Guardado técnico mueve archivo al directorio de cliente/embarque y escribe metadatos; controlador intenta correo de nueva documentación.
4. Descarga pasa por guardián de sesión y parámetros; si falta archivo devuelve «El archivo no existe !!». Eliminación intenta borrar archivo y registro. [F07a, F07b]

**RISK de ruta observable:** el manejador de submit del frame usa `index_archivos/logistica/embarquesController.php`, mientras el controlador inspeccionado está en `index_archivos/embarques/embarquesController.php`. ❓ Un alias/rewrite externo podría resolverlo, pero no se comprobó. Por ello el formulario visible no se presenta como carga end-to-end demostrada. El submódulo de intercambio tampoco se materializó. [F07a]

## F-08. Registrar costos y calificar operación

**Costos:** pestaña «Costos» monta componentes que cargan categorías/conceptos y presentan Moneda, Concepto, Monto y «Guardar», condicionado a una bandera de visibilidad. El navegador revisa duplicados y montos indefinidos; POST JSON lleva categorías/conceptos/importes a `guardar-costos.php?id=...`. El servidor exige conceptos en primera categoría, borra lógicamente datos previos de esa categoría y crea maestro/detalle; notifica durante la escritura. Fallo de detalle elimina el nuevo maestro, sin garantizar que la respuesta superior sea error. **Inferencia operativa:** verificar persistencia después de guardar; no entenderlo como aprobación de una factura o pago. [F08a]

**Rating:** componente muestra «Califica tu operación en ASGARD», estrellas en incrementos de 0,5, «Comentario» y «Enviar» o icono de envío. Pide confirmación y POST; cuerpo `code=200` muestra «Calificación Enviada». Invitación mensual consulta fecha + 30 días para misma combinación de entidades; «Decidir la proxima vez» cierra modal. El INSERT no aplica esa periodicidad y recibe el autor de POST. Es una opinión registrada, no acreditación de servicio ni validación de negocio. [F08b]

## F-09. Generar y exportar reportes

**Entradas/precondiciones:** permisos del catálogo para encontrar la opción; sesión, relaciones y funciones SQL requeridas. [F09a]

1. Abrir «Reporte de Control OL» o «Reporte de Control AD», si la opción está asignada.
2. OL: seleccionar Cliente, Proveedor y Estado; «Generar» envía POST con `accion=ge`; `data.php` ejecuta consultas auxiliares para etapas y principal para filas. AD añade filtros/cálculos propios y acota por agente de sesión.
3. Leer tabla y pulsar «Excel». El formulario envía consultas y configuración de columnas; exportador las vuelve a ejecutar y produce tabla HTML con extensión `.xls`.

**Límites:** OL contiene cliente fijo 429 para relación de operador/cálculo de etapa; entrega en destino está enlazada al campo de inicio de tránsito. AD contiene fórmulas de previsión/KPI que no están validadas por negocio ni fiscalmente. Las tablas temporales del reporte no son una actualización del estado operativo del embarque. ❓ SQL de funciones almacenadas, permisos de conexión y resultado exportado no ejecutados. [F09a, F09b]

## Frontera compartida y variantes

**Consulta de inventario por chasis (AS-IS):** con permiso del grupo 7, abrir «Inventario por Chasis», introducir «Chasis» y pulsar «Buscar». El frontend hace POST a `inventario/proveedores/informacion` con chasis, embarque/partida nulos y autorización de sesión. La respuesta se distribuye a inventario en puerto, depósito transitorio y post nacionalización. Se oculta el indicador de carga al finalizar; el error tiene una rama específica para código 300, sin demostrar una gestión completa del caso vacío. ❓ Persistencia, fotos, exactitud física y autorizaciones del backend externo no verificadas. [F12]

M ya contiene inventario, estado de pedidos y creación de pedidos particularizada; no se debe inferir que cualquier concepto «pedido» es exclusivo de Perú. Lo específico contrastado en P es la pantalla `embarques/pedidos.php`, el módulo `preembarques`, concesionario/tipo 7, creación desde ítems y soporte de vídeo. Presencia/exclusividad se contrastó mediante árboles Git, no mediante nombres del grafo. [F10]

M fija zona La Paz y contiene ruta Tambo Quemado–Patacamaya y selecciones geográficas del país ID 31. Son particularidades de esta base, no reglas mundiales. Dockerfile declara PHP 5.4. El lint local con PHP 8.4 no equivale a ejecutar ese entorno. [F11]

## Índice de evidencia

| ID | Commit, ruta y líneas |
|---|---|
| F01a | `M:index_archivos/login.php:L1-L13,L27-L38,L90-L94`; `M:index_archivos/veriflogin.php:L16-L146` |
| F01b | `M:index_archivos/2fa.php:L10-L14,L61-L80`; `M:index_archivos/2fa/TwoFaClass.php:L134-L218`; `M:index_archivos/2fa/ajax/autenticar.php:L1-L6` |
| F01c | `M:index_archivos/menu_b4.php:L265-L277`; `M:index_archivos/usuario/UsuarioClass.php:L12-L43`; `M:index_archivos/logout.php:L10-L17` |
| F01d | `M:index_archivos/permisos.php:L1-L27`; `M:index_archivos/guardia_descargas_rel.php:L1-L5` |
| F01e | `M:index_archivos/login.php:L136-L137`; `M:index_archivos/resetpassword/js/firstStep.js:L5-L14,L34-L40`; `M:index_archivos/resetpassword/js/secondStep.js:L6-L9,L25-L37`; `M:index_archivos/resetpassword/js/thridStep.js:L5-L11,L29-L33`; `M:index_archivos/resetpassword/ResetPassword.php:L11-L99`; `M:index_archivos/resetpassword/ajax/sendCredentials.php:L1-L13`; `M:index_archivos/resetpassword/ajax/resetPassword.php:L1-L13` |
| F02a | `M:index_archivos/MenuClass.php:L11-L44`; `M:index_archivos/menu_b4.php:L98-L201` |
| F02b | `M:index_archivos/embarques/ajax/listaEmbarques.php:L16-L56,L130-L178`; `M:index_archivos/embarques/EmbarqueClass.php:L135-L306` |
| F02c | `M:index_archivos/embarques/embarquever.php:L18-L30,L128-L144,L224-L284,L292-L391` |
| F02d | `M:index_archivos/menu_b4.php:L218-L255,L280-L353` |
| F03a | `M:index_archivos/embarques/index.php:L50-L62`; `M:index_archivos/embarques/embarquecrear.php:L8-L33,L159-L218,L368-L378` |
| F03b | `M:index_archivos/embarques/componentes/embarques_datos.php:L1-L98`; `M:index_archivos/embarques/js/datosEmbarques.js:L87-L154` |
| F03c | `M:index_archivos/embarques/embarquesController.php:L45-L115` |
| F03d | `M:index_archivos/embarques/CotizacionClass.php:L655-L777,L1288-L1309` |
| F04a | `M:index_archivos/tracking/crear-viaje.php:L27-L80,L159-L179`; `M:index_archivos/tracking/vue/journey.page.js:L64-L95,L183-L223` |
| F04b | `M:index_archivos/tracking/ajaxAsignacion/guardar_asignacion.php:L10-L72` |
| F04c | `M:index_archivos/tracking/TrackingNewClass.php:L181-L285,L1099-L1107,L1635-L1648` |
| F04d | `M:index_archivos/tracking/ajaxAsignacion/guardar_asignacion.php:L73-L155`; `M:index_archivos/tracking/TrackingNewClass.php:L967-L989` |
| F04e | `M:index_archivos/tracking/ListaViajesClass.php:L9-L100,L157-L231` |
| F05a | `M:index_archivos/tracking/carga-masiva.php:L39-L64`; `M:index_archivos/tracking/ajax/uploadExcelCargaMasiva.php:L18-L79,L118-L126,L157-L163,L203-L238` |
| F05b | `M:index_archivos/tracking/controllers/CargaMasiva.php:L23-L129,L132-L223,L279-L358` |
| F05c | `M:index_archivos/embarques/embarquesController.php:L101-L108`; `M:index_archivos/tracking/controllers/CargaMasiva.php:L361-L367` |
| F05d | `M:index_archivos/parametros/clientes/ClienteProveedorClass.php:L118-L160` |
| F06a | `M:index_archivos/embarques/frames/aduanas.php:L17-L57,L76-L81`; `M:index_archivos/embarques/componentes/embarques_ver_gestion_aduanera.php:L28-L35,L55-L68,L113-L138` |
| F06b | `M:index_archivos/embarques/SolicitudesClass.php:L672-L805`; `M:index_archivos/embarques/ajax/guardarGestionAduanera.php:L1-L30` |
| F06c | `M:index_archivos/versolicitud.php:L59-L103`; `M:index_archivos/versolicituddetalle.php:L1-L4,L284-L286,L357-L369,L381-L420,L474-L505` |
| F07a | `M:index_archivos/embarques/frames/documentos.php:L16-L49,L102-L136`; `M:index_archivos/embarques/componentes/embarques_documentacion.php:L1-L42` |
| F07b | `M:index_archivos/embarques/EmbarqueClass.php:L310-L389`; `M:index_archivos/embarques/embarquesController.php:L118-L145`; `M:index_archivos/download.php:L1-L42`; `M:index_archivos/guardia_descargas_rel.php:L1-L5` |
| F08a | `M:index_archivos/embarques/componentes/costos/costos.js:L37-L54,L151-L195`; `M:index_archivos/embarques/ajax/guardar-costos.php:L1-L8`; `M:index_archivos/embarques/CostosClass.php:L355-L390,L443-L450,L576-L594` |
| F08b | `M:index_archivos/rating/rating.js:L1-L31,L120-L150`; `M:index_archivos/rating/rating-modal.js:L16-L31`; `M:index_archivos/rating/RatingClass.php:L8-L75`; `M:index_archivos/rating/rating.php:L1-L13` |
| F09a | `M:index_archivos/reportes/reportecontrolol.php:L72-L118`; `M:index_archivos/boton.php:L1`; `M:index_archivos/reportes/reportecontrololquery.php:L3-L21,L107-L145`; `M:index_archivos/reportes/reportecontroladquery.php:L23-L24,L85-L133` |
| F09b | `M:index_archivos/data.php:L1-L23`; `M:index_archivos/reporteexcel/reporteexcel.php:L1-L25,L50-L81` |
| F10 | `M:index_archivos/embarques/embarquever.php:L252-L284`; `M:index_archivos/embarques/CotizacionClass.php:L686-L688`; `P:index_archivos/menu_b4.php:L148-L172`; `P:src/core/users/application/Find/UserFind.php:L25-L63`; `P:index_archivos/preembarques/index.php:L1-L24`; `P:index_archivos/embarques/ajax/crear-viaje-desde-items.php:L1-L7`; `P:index_archivos/tracking/getVideo.php:L1-L20` |
| F11 | `M:Dockerfile:L1-L6`; `M:index_archivos/cnfdb105.php:L11`; `M:index_archivos/embarques/embarquecrear.php:L30-L33`; `M:index_archivos/tracking/vue/journey.page.js:L97-L115` |
| F12 | `M:index_archivos/menu_b4.php:L184-L190`; `M:index_archivos/logistica/inventario-chasis.php:L26-L49,L97-L138` |

## Brechas que impiden validar los recorridos

❓ Faltan esquema/rutinas SQL de aplicación, configuración efectiva de permisos y clientes, submódulos de documentos/notificaciones y comprobación de APIs de tracking/inventario. Asgard nativo no se ejecutó por bloqueo de Windows App Control comunicado en esta revisión; se realizó inspección estática alternativa. No se han confirmado pantallas en navegador, entrega de mensajes, concurrencia, aislamiento entre proveedores ni recuperación de fallos parciales. El conjunto queda como documentación fuente, sin promoción a especificación canónica ni PASS funcional.

# Manual de recorridos de proveedores

La [revisión iterativa](../reviews/iterative-20261118/README.md) incorpora advertencias nuevas sobre costos, edición de cargas/chasis, procesamiento de lotes y representación de eventos. Consulte los [defectos operativos](operational-findings.md) antes de interpretar una confirmación como persistencia completa. Las correcciones de documentación no corrigen la aplicación ni constituyen una validación operativa.

Edición del 18-11-2026, reconstruida desde **master a8ce2c23dead8552d2c4699e4a9b9134f7a18707**. Las etiquetas entre comillas se han leído en plantillas/componentes. **No se ha comprobado la aplicación en navegador ni con datos reales:** son instrucciones respaldadas por fuente, pendientes de validación operativa. Los resultados dependientes de configuración o servicios se indican como ❓.

La referencia abreviada `M:ruta:Lx-Ly` significa ese commit exacto, archivo y líneas. El contraste Perú usa `P` = **95fe9a4c3b3cddd84be922cc0e1eb9c88603df62**. Para elegir versión: [Bolivia/master](../variants/bolivia.md), [Perú](../variants/peru.md) y [comparación](../variants/README.md). Los menús de una cuenta dependen de sus permisos y del tipo de proveedor: no todas las opciones descritas aparecerán a todos los usuarios.

## Qué preparar

Tenga su cuenta, entidad representada y referencia del trabajo: número de embarque, pedido, factura comercial o viaje. Para crear viajes prepare transporte/placa, conductor, carga y lugares de recogida/entrega. Para cargas Excel, use la plantilla específica de la pantalla y compruebe previamente los catálogos de clientes/ubicaciones, unidades y conductores.

Aquí «usuario» es la cuenta individual; «operador/proveedor» es la entidad que representa. «Embarque» y «viaje» son registros diferentes: un embarque puede mostrar varios viajes. «Pedido» se conserva en `ordencompra` y «Orden de Compra» en `ordencompraini`; esta diferencia de nombres internos importa al comunicar un error al soporte. [U01, U03, U05]

## Entrar y salir

1. En login, complete «Nombre de Usuario» y «Contraseña» y pulse **«Iniciar sesión»**.
2. Si aparece la autenticación por correo, introduzca los seis dígitos en «Digitar código»; la verificación se dispara al completar seis. «Reenviar código» solicita otro. No acumule intentos con códigos dudosos: el código tiene ventana de diez minutos y el flujo puede bloquear la cuenta después de superar tres intentos fallidos.
3. Si se solicita cambiar contraseña por antigüedad, complete ese cambio antes de continuar. Desde el menú de usuario puede abrir «Perfil» para cambiarla; el método comprueba la anterior y que la nueva sea diferente.
4. Al terminar use **«Salir»**. «Volver a Ingresar» abre login, pero no ejecuta la misma destrucción de sesión que Salir. [U01]

| Mensaje/situación | Cómo continuar |
|---|---|
| «Contraseña incorrecta» | Revise la contraseña antes de reenviar |
| «El usuario no existe» | Revise el nombre de cuenta |
| «El usuario está inactivo» o bloqueo por intentos | Solicite revisión de la cuenta al responsable de accesos; este código no acredita un mecanismo de desbloqueo por el usuario |
| Token CSRF inválido | Abra de nuevo login y realice un intento con su formulario actual |
| Pantalla sin mensaje tras introducir formato/longitud fuera de lo permitido | La rama revisada termina antes del reenvío; comunique el problema sin incluir contraseñas |

Fuente: `M:index_archivos/login.php:L27-L38,L124-L137`; `M:index_archivos/veriflogin.php:L16-L49,L70-L126`; `M:index_archivos/2fa.php:L48-L80`; `M:index_archivos/2fa/TwoFaClass.php:L140-L175`; `M:index_archivos/usuario/UsuarioClass.php:L12-L43`; `M:index_archivos/menu_b4.php:L265-L277`; `M:index_archivos/logout.php:L10-L17` [U01]. La seguridad efectiva de MFA y sesión tiene observaciones pendientes en [actores y permisos](actors-and-permissions.md); no se valida por este recorrido.

**Si olvidó su contraseña:** el enlace **«olvidé mi contraseña»** abre un flujo separado. Complete Nombre, Apellido y Nombre de usuario o correo y pulse **«Siguiente»**; introduzca el código recibido y vuelva a pulsar **«Siguiente»**; complete **«Contraseña»** y **«Confirmar Contraseña»** y pulse **«Finalizar»**. Si informa fallo al comprobar usuario, enviar correo o token expirado, revise la cuenta y solicite asistencia sin compartir el código. La ventana de diez minutos descrita para MFA no corresponde a esta recuperación, que compara fecha de creación con inicio del día actual. ❓ Recorrido y seguridad entre pasos pendientes de validación operativa. Fuente: `M:index_archivos/resetpassword/js/firstStep.js:L5-L14`; `M:index_archivos/resetpassword/js/secondStep.js:L6-L9`; `M:index_archivos/resetpassword/js/thridStep.js:L5-L11`; `M:index_archivos/resetpassword/ResetPassword.php:L11-L94` [U13].

## Encontrar el embarque correcto

1. Abra **«Logística» → «Embarques»** y la opción del alcance que su cuenta tenga asignada. Los nombres del último submenú se cargan desde configuración.
2. Use «Linea», las fechas de creación o los filtros del listado para reducir resultados. Confirme cliente, pedido, OC, factura y descripción de carga.
3. Pulse el icono con título **«Ver»** en la fila correcta.
4. Dentro del embarque, seleccione la pestaña de su tarea. Entre las etiquetas leídas están «Gestión Logistica», «Gestión Aduanera», «Costos», «Documentos», «Tracking», «Inventario», «Crear Viaje», «Descripción de Items» y «Estado de Pedidos». Su visibilidad depende de permisos y condiciones del registro. [U02]

Si su menú tiene lupa, puede abrir «Buscar Embarques»: escriba al menos cuatro caracteres en **«Pedido/FC/Embarque»**, pulse **«Buscar»** y después **«Abrir»** en el resultado. El formulario distingue «No se encontraron resultados» de error al realizar búsqueda. [U02]

❓ Un listado vacío puede reflejar relación de la cuenta, alcance o filtros. No demuestra que el embarque no exista. Para soporte anote cuenta/entidad, alcance y filtros, sin compartir cookies ni tokens.

Fuente: `M:index_archivos/menu_b4.php:L147-L168,L218-L255,L280-L353`; `M:index_archivos/embarques/index.php:L75-L95`; `M:index_archivos/embarques/ajax/listaEmbarques.php:L16-L40,L162-L174`; `M:index_archivos/embarques/embarquever.php:L128,L219-L284` [U02].

## Crear un embarque

**Antes de empezar:** esta acción se ofrece en el listado a tipo 1 para alcances distintos de nacional. Necesita los datos del solicitante, mercancía, modalidad y tramos. No dé por hecho que otro perfil o país tendrá el mismo formulario. [U03]

1. Pulse **«Crear Embarque»**.
2. Seleccione **«Solicitante»** y **«Modalidad de Transporte»**. Complete **«Orden de Compra»** y **«Pedido»** con sus referencias correspondientes. En internacional, seleccione **«Incoterm»** y complete los datos de ciudad/país que solicite el formulario.
3. Complete mercancía y magnitudes. El tipo de mercancía puede mostrar clase y UN o temperatura. Complete los tramos y lugares que correspondan a la modalidad seleccionada.
4. Pulse **«Guardar»**. Si el navegador señala campos obligatorios, complételos y vuelva a guardar.
5. Al volver al listado, localice el nuevo embarque y abra «Ver» para confirmar referencias, magnitudes y tramos. [U03]

**Resultado previsto en el código:** alta de embarque y datos asociados. La cabecera puede haberse creado aunque alguna escritura posterior falle; volver al listado no garantiza que todo esté completo. Ante un error tras guardar, busque primero por sus referencias antes de repetir el alta.

Particularidades de M: para una entidad concreta (ID 333), en local, OC y Pedido son multiselecciones obligatorias; cliente 417/local activa creación de pedido asociada. Son ramas por ID, no una regla aplicable a todo usuario. La opción **«IMPORTAR EXCEL»** del formulario local dispone de un camino separado cuya creación posterior de viaje tiene un desajuste de argumentos observado; ❓ requiere validación antes de usarlo como procedimiento habitual.

Fuente: `M:index_archivos/embarques/index.php:L50-L62`; `M:index_archivos/embarques/embarquecrear.php:L130-L153,L159-L213,L368-L378`; `M:index_archivos/embarques/componentes/embarques_datos.php:L1-L98`; `M:index_archivos/embarques/js/datosEmbarques.js:L87-L149`; `M:index_archivos/embarques/embarquesController.php:L45-L115`; `M:index_archivos/embarques/CotizacionClass.php:L655-L696`; `M:index_archivos/tracking/controllers/CargaMasiva.php:L361` [U03].

## Preparar y asignar un viaje

**Antes:** compruebe embarque, alcance, modalidad, empresa de transporte, placa, conductor, carga, origen y destino. La pestaña **«Crear Viaje»** del embarque requiere permiso, tipo 1 y que no tenga `fecha_finalizacion`; la pantalla de viajes también puede estar enlazada desde menú según su configuración. [U04]

1. Si se muestra **«SELECCION DE EMBARQUE»**, busque la referencia y seleccione su fila. Aunque el campo anuncia «Buscar por número de pedido o cliente», el filtro leído de esta pantalla compara número y pedido, y presenta hasta diez resultados.
2. Revise información del embarque y complete orden/mercancía, transporte, conductor, carga, origen(es), destino(s), documentos y rutas según el formulario.
3. Para conservar preparación, pulse **«Guardar Borrador»**. Para asignar, pulse **«GUARDAR Y ASIGNAR»**. Son acciones distintas; el borrador se guarda con estado 4 y la asignación con estado nulo que se presenta como «Asignado».
4. Anote **«Número de Viaje»** en la confirmación y pulse **«Lista de Viajes»**. Compruebe que aparece el registro y que transporte/carga/localizaciones sean correctos. [U04]

**Si falla:** el guardado se hace en varios pasos y luego intenta comunicaciones. Un error de conexión o notificación puede aparecer después de escribir datos. Antes de repetir, revise lista por referencia y número. El código llama a WhatsApp también en la creación de borrador; guardar borrador no debe entenderse como garantía de que nadie será notificado. ❓ Entrega efectiva y aceptación del conductor no probadas.

Fuente: `M:index_archivos/embarques/embarquever.php:L254-L270`; `M:index_archivos/tracking/crear-viaje.php:L43-L80,L159-L179`; `M:index_archivos/tracking/vue/journey.page.js:L73-L95,L183-L223`; `M:index_archivos/tracking/TrackingNewClass.php:L181-L235,L1099-L1107`; `M:index_archivos/tracking/ajaxAsignacion/guardar_asignacion.php:L73-L155` [U04].

## Revisar seguimiento y actuar sobre viajes

1. Abra el listado de viajes disponible para su cuenta. Filtre por número, chofer/placa, alcance o ambas fechas de creación.
2. Revise estado, fecha, carga, documentos, frontera, descarga y última posición. Use **«Ver»** para detalle. Las fotos/documentos están vinculados a eventos; una columna «Arribado» no certifica por sí misma una ubicación física actual.
3. Utilice las acciones que presente la fila según su tarea. [U05]

| Acción visible | Condición de interfaz leída | Efecto a considerar |
|---|---|---|
| «Editar» | Borrador (4) | Actualiza datos del viaje; guardar puede dejar pasos parciales ante error |
| «Borrar» | Borrador (4) | Pide confirmación; llama a procedimiento SQL de borrado; contenido exacto del procedimiento desconocido |
| «Interrumpir» | Aceptado (1) o asignado nulo | Pide motivo; cambia a Interrumpido (2) y registra fecha/entidad |
| «Eliminar» | Interrumpido (2), local o nacional | Pide confirmación; marca borrado lógico para quitarlo de los listados que lo filtran |
| «Duplicar» | Botón construido en cada fila | Llama a procedimiento que devuelve nuevo número; ❓ qué elementos copia y estado inicial no verificados |

Las etiquetas de estado programadas son Rechazado 0, Aceptado 1, Interrumpido 2, Completado 3, Borrador 4 y Asignado para NULL. Hay una comparación exterior con nulo que exige verificar cómo se representa 0 en el PHP del despliegue. Este portal muestra esos estados; no se ha comprobado aquí el recorrido externo por el que conductor acepta o completa el viaje.

Fuente: `M:index_archivos/tracking/listaviajes.php:L7-L15,L172-L291`; `M:index_archivos/tracking/ListaViajesClass.php:L9-L100,L157-L231`; `M:index_archivos/tracking/js/listaviaje.js:L37-L120`; `M:index_archivos/tracking/HerramientasClass.php:L5-L47`; `M:index_archivos/tracking/TrackingNewClass.php:L947-L964` [U05].

## Crear viajes con una carga masiva

**«Cargar Archivo» puede crear viajes inmediatamente si no encuentra observaciones.** Prepare el archivo y sus referencias antes de pulsarlo; este camino no tiene una segunda confirmación de creación. [U06]

1. En la pantalla de carga masiva descargue el formato Excel desde **«aqui»**. Use esa plantilla; no la de clientes/proveedores.
2. Complete la hoja activa desde la fila 3 y conserve las columnas. El lector descarta filas si A o B están vacías.
3. Seleccione el fichero en **«Archivo»** y pulse **«Cargar Archivo»**.
4. Lea la tabla de resultados y su columna de mensajes. Corrija códigos/ubicaciones, origen, placa, conductor, bulto o referencia que no coincidan con los registros.
5. Si anuncia viajes creados, anote todos los números y use **«Volver a los viajes»** para comprobarlos. No repita todo el archivo solo porque falte parte del resultado: primero determine qué grupos se crearon. [U06]

| Columnas del formato leídas | Contenido |
|---|---|
| A / B | Agrupación de registros / número de viaje usado para agrupar la creación |
| C / D | Referencia / código de cliente propio |
| E–K | Nombre, dirección, tipo, país, ciudad, contacto, teléfono |
| L / M / N | Origen / placa / nombre de conductor |
| O / P | Fecha / hora leídas del fichero; el temporal usa fecha y hora actuales, por lo que no se garantiza conservarlas |
| Q / R / S | Descripción de ítem / tipo de bulto / otro |
| T / U / V | Cantidad / peso KG / volumen M3 |

**Atención al resultado:** status 200 del agregador no comprueba todos los códigos individuales de creación. «No se cargaron los viajes, revise el formato del archivo excel» indica ausencia de filas útiles. Una nueva carga elimina temporales pendientes previos de la misma cuenta. Estas observaciones justifican verificar los viajes antes de reintentar.

Fuente: `M:index_archivos/tracking/carga-masiva.php:L39-L64`; `M:index_archivos/tracking/ajax/uploadExcelCargaMasiva.php:L18-L73,L118-L128,L157-L163,L203-L238`; `M:index_archivos/tracking/controllers/CargaMasiva.php:L23-L84,L279-L358` [U06].

## Consultar aduanas y aportar documentos

**Aduanas:** en un embarque internacional con opción habilitada, abra **«Gestión Aduanera»**, seleccione **«Pendientes»** o **«Enviados»** y abra la columna **«Ver»** del `SOL-...` correcto. La interfaz contiene otros rótulos de etapas, pero parte de sus paneles históricos está comentada: no se puede prometer su operación completa. Si un alta de gestión informa **«Se registro la nueva gestion aduanera, pero sin documentos.»**, la solicitud existe y necesita revisar sus documentos; no repita automáticamente el alta. [U07]

**Documentos de embarque:** abra **«Documentos»**. Si aparece el formulario clásico, use **«Seleccionar Archivo»** y **«Agregar documento»**; compruebe después que figura en tabla y que el enlace de su nombre descarga el archivo. La papelera tiene título «Eliminar». Si hay intercambio documental asociado, esta pestaña delega en otro componente y su interfaz no ha podido verificarse en el checkout. [U08]

❓ La ruta AJAX del formulario clásico apunta a un controlador bajo `logistica/`, mientras el controlador leído está bajo `embarques/`. Su funcionamiento puede depender de configuración externa; ante carga sin respuesta registre pantalla y nombre del archivo y compruebe la tabla antes de repetir. Un error de correo tampoco prueba que no se guardara el archivo.

**Solicitudes clásicas:** cuando su cuenta tenga acceso a la lista «Solicitudes», abra el detalle. Las etiquetas leídas incluyen «Nuevo(s) Documento(s) Complementario(s)», «Editar Documentos Complementario», «Aceptar», «Cancelar» y **«Enviar Documentos»**. Esta última marca documentos para envío después de intentar correo; no equivale a aprobación del despacho. Este camino incluye dependencias del sistema de clientes y una observación de control de sesión: su disponibilidad debe validarse antes de adoptarlo como procedimiento. [U07]

Fuente aduanas: `M:index_archivos/embarques/frames/aduanas.php:L17-L57,L76-L81`; `M:index_archivos/embarques/componentes/embarques_ver_gestion_aduanera.php:L28-L35,L55-L68,L113-L138`; `M:index_archivos/embarques/SolicitudesClass.php:L743-L765`; `M:index_archivos/versolicitud.php:L88-L103`; `M:index_archivos/versolicituddetalle.php:L1-L4,L284-L286,L357-L369,L474-L505` [U07]. Fuente archivos: `M:index_archivos/embarques/frames/documentos.php:L43-L49,L102-L136`; `M:index_archivos/embarques/componentes/embarques_documentacion.php:L1-L42`; `M:index_archivos/embarques/EmbarqueClass.php:L310-L389`; `M:index_archivos/download.php:L16-L42` [U08].

## Registrar costos y dar una calificación

**Costos:** abra **«Costos»**, seleccione **«Moneda»**, complete conceptos e importes y pulse **«Guardar»**, si está disponible. Corrija mensajes de conceptos duplicados o montos sin definir. El botón depende de que el embarque no esté finalizado. El guardado sustituye lógicamente costos anteriores de la categoría: verifique importes guardados antes de volver a enviar. El mensaje de éxito no acredita pago, aprobación contable ni integridad de todas las escrituras. [U09]

**Calificación:** cuando aparezca **«Califica tu operación en ASGARD»**, seleccione estrellas, complete «Comentario» si lo desea y use **«Enviar»** o el icono de envío. La confirmación ofrece **«Cancelar»** y **«OK»**; el resultado esperado del componente es **«Calificación Enviada»**. En modal puede elegir **«Decidir la proxima vez»**. La interfaz anuncia que la calificación no podrá editarse y otra quedará disponible después de 30 días; el código usa ese plazo para invitar, pero no lo impone en el INSERT. No se afirma un compromiso de servicio derivado de ese aviso. [U10]

Fuente costos: `M:index_archivos/embarques/frames/costos.php:L51-L68`; `M:index_archivos/embarques/componentes/costos/costos.js:L37-L54,L151-L195`; `M:index_archivos/embarques/CostosClass.php:L355-L390,L443-L450,L576-L594` [U09]. Fuente rating: `M:index_archivos/rating/rating.js:L1-L31,L120-L149`; `M:index_archivos/rating/RatingClass.php:L8-L29,L46-L75`; `M:index_archivos/rating/rating-modal.js:L16-L31` [U10].

## Consultar inventario por chasis

Si tiene la opción **«Inventario por Chasis»**, abra la pantalla, introduzca **«Chasis»** y pulse **«Buscar»**. La pantalla prepara tres áreas: **«INVENTARIO EN PUERTO DE CARGA»**, **«INVENTARIO DEPÓSITO TRANSITORIO»** e **«INVENTARIO - POST NACIONALIZACIÓN»**. [U11]

❓ La búsqueda consume una API externa con la identidad de sesión. No se ha probado el caso sin coincidencias, carga de fotos ni edición. Un panel vacío no demuestra ausencia de inventario. Los inventarios y módulos de preembarques de Perú tienen otros contratos; consulte su [página específica](../variants/peru.md).

Fuente: `M:index_archivos/menu_b4.php:L184-L190`; `M:index_archivos/logistica/inventario-chasis.php:L26-L49,L97-L138` [U11].

## Generar un reporte y descargar Excel

1. Desde **«Reportes»**, abra la opción asignada. Los nombres finales de las opciones provienen de permisos de la cuenta.
2. En **«Reporte de Control OL»** complete Cliente, Proveedor y Estado según su consulta y pulse **«Generar»**.
3. Compruebe tabla y filtros. Pulse **«Excel»** si desea la exportación en una nueva pestaña. El fichero tiene extensión `.xls`, aunque se construye como tabla HTML; no es un libro XLSX nativo.
4. Para **«Reporte de Control AD»**, revise los filtros específicos y las magnitudes antes de interpretar indicadores. [U12]

**Interpretación:** OL contiene una selección fija del cliente 429 y un rótulo de entrega asociado al campo de inicio de tránsito; no use ese rótulo como prueba de entrega. AD contiene cálculos de previsión y tolerancias del código, pendientes de validación empresarial. Excel vuelve a consultar los datos: pueden diferir de una vista anterior si hubo cambios entre ambas acciones.

Fuente: `M:index_archivos/menu_b4.php:L123-L134`; `M:index_archivos/reportes/reportecontrolol.php:L72-L118`; `M:index_archivos/boton.php:L1`; `M:index_archivos/reportes/reportecontrololquery.php:L18-L21,L122-L145`; `M:index_archivos/reportes/reportecontroladquery.php:L23-L24,L85-L133`; `M:index_archivos/reporteexcel/reporteexcel.php:L1-L25,L50-L81` [U12].

## Límites de esta edición y ayuda al soporte

Las instrucciones principales corresponden a M con particularidades bolivianas. Perú añade las pantallas dedicadas de Pedidos y Pre Embarques, concesionario y creación de viajes desde ítems; no se han mezclado con el recorrido de M. M también tiene estado de pedidos e inventario: esos conceptos no son exclusivos de Perú. [Comparación de versiones](../variants/README.md).

Para comunicar un fallo incluya versión/país, opción y botón pulsados, número de embarque/viaje/solicitud, fecha y mensaje. Evite adjuntar contraseñas, JWT, cookies, configuraciones o documentos de terceros. Antes de repetir altas/importaciones, compruebe si quedaron registros creados.

❓ Pendiente de validación: permisos realmente cargados, funcionamiento de submódulos y APIs, comportamiento de errores y comunicaciones, estado efectivo de inventario y funciones SQL. Asgard nativo no ejecutado por bloqueo de Windows App Control comunicado en la revisión. El lint con PHP CLI 8.4.25 solo verificó sintaxis puntual; Dockerfile de M declara PHP 5.4 y `America/La_Paz` (`M:Dockerfile:L1-L6`). Este manual no certifica ese despliegue.

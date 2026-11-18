# Auditoría de seguridad dirigida — master

Fecha de auditoría: 18 de noviembre de 2026. Código analizado: C:/repos/proveedores-github-review-20261118. Commit auditado: a8ce2c23dead8552d2c4699e4a9b9134f7a18707. Referencia de comparación: origin/master_peru, resuelta a 95fe9a4c3b3cddd84be922cc0e1eb9c88603df62. Todas las ubicaciones de código citadas corresponden al commit auditado; los intervalos de líneas incluyen ambos extremos. El archivo security-findings.json contiene los hallazgos estructurados para su revisión.

## Evaluación y límites de la evidencia

Se documentan quince hallazgos acotados: ocho P1 y siete P2. La revisión iterativa añade [SEC-015: SQL completo elegido por el cliente en el exportador](../reviews/iterative-20261118/report-query-contract.md), con tres pruebas aisladas y precondiciones de acceso y privilegios. La prioridad expresa la urgencia de corregir el defecto bajo las precondiciones indicadas; no acredita que se haya explotado un despliegue. Las trazas más relevantes corresponden al restablecimiento de contraseña sin autorización comprobada en el servidor, la inyección SQL en determinados manejadores y la asignación de identidad desde datos del cliente en MFA. Las consecuencias de la contraseña maestra y de la guardia compartida requieren especial atención a la versión y configuración de PHP.

La clasificación distingue COMPORTAMIENTO ACTUAL, DEFECTO CONFIRMADO en el código, RIESGO condicionado y RECOMENDACIÓN. La accesibilidad de las rutas y su impacto en producción permanecen sin verificar (❓). El informe no constituye una aprobación de seguridad, una especificación canónica ni una evaluación exhaustiva de vulnerabilidades.

La evidencia combina lectura del código, comparación de objetos y diferencias de Git y pruebas aisladas mediante PHP CLI. No se ejecutaron puntos de entrada de la aplicación ni se realizaron solicitudes HTTP, DNS, de correo, a bases de datos o a otros servicios. El código de la aplicación permanece sin cambios.

## Restricciones de ejecución que condicionan la evaluación

- Dockerfile:1-6 declara php:5.4-apache, puerto 80, zona horaria America/La_Paz y extensiones mysql, mysqli y PDO; únicamente copia .htaccess. Esto no acredita la imagen realmente desplegada, el montaje de la aplicación, la configuración PHP, el proxy TLS ni la ubicación del almacenamiento. cnfdb105.php:11 también establece America/La_Paz.
- El intérprete local es PHP 8.4.25 CLI. El archivo source-audits/master/2026-11-18/php-lint.json recoge 279 archivos propios: 276 superan la comprobación y tres fallan, con short_open_tag activado. Los errores corresponden a ternarios anidados sin paréntesis, no admitidos por PHP 8.4, en index_archivos/embarques/componentes/cotizaciones/local/ferreo.php:57, index_archivos/embarques/componentes/cotizaciones/local/terrestre.php:57 e index_archivos/tracking/documentosempresatransporte.php:37. Son incompatibilidades sintácticas con PHP 8.4; no demuestran el comportamiento en producción ni se cuentan como hallazgos de seguridad adicionales. La comprobación sintáctica no evalúa la constante de permisos.php.
- cnfdb105.php:2-3 incluye .env.php y exige vendor/autoload.php. Ambos faltan en el entorno local y figuran en .gitignore:2-3. cnfdb105.php:14-25 puede abrir una conexión MySQL durante su inclusión en PHP 5.4; esas inclusiones no se ejecutaron. Los dos submódulos de Git tampoco están poblados localmente. No se han validado las constantes del entorno, las dependencias, el esquema, los permisos de base de datos ni la gestión de errores. La ausencia del cargador obligatorio impide ejecutar el manejador real en esta copia.
- permisos.php:21 contiene la constante sin definir datoconservar, dentro de la rama anónima y antes del cierre de PHP. PHP 8.4 genera Error al evaluarla; la rama autenticada no pasa por esa instrucción. PHP 5.4 normalmente interpreta una constante sin definir como una cadena y emite un aviso, por lo que la ausencia de exit resulta relevante. Un manejador de errores personalizado puede alterar ese comportamiento. No queda demostrada la explotación anónima de todos los manejadores que comparten esta guardia en PHP 8.4.
- veriflogin.php:57 utiliza password_verify(), que no existe de forma nativa en PHP 5.4. No se encontró una implementación de compatibilidad en el código propio inspeccionado; podría proporcionarla la dependencia vendor ausente. Si master_pass devuelve registros y no existe esa función, la llamada interrumpe la autenticación. Las consecuencias de la contraseña maestra descritas más adelante requieren un entorno en el que la función esté disponible.

## Hallazgos priorizados

### SEC-001 — P1: El restablecimiento de contraseña acepta un ID sin autorización de restablecimiento

Evidencia: index_archivos/resetpassword/ajax/resetPassword.php:2-11; index_archivos/resetpassword/ResetPassword.php:46-68,77-81; index_archivos/resetpassword/js/secondStep.js:25-37 y js/thridStep.js:28-34.

COMPORTAMIENTO ACTUAL / DEFECTO CONFIRMADO: El manejador público entrega únicamente los campos POST password e identifier a resetPasswordClient(). El método busca el registro de restablecimiento por ID y actualiza la cuenta asociada. No comprueba el token, la caducidad, deleted_at ni una autorización vinculada a la sesión. verifyToken() marca el registro como eliminado y devuelve su ID, pero esa operación independiente no es un requisito impuesto por el servidor al manejador final.

Activación y precondiciones: Deben funcionar el arranque y el acceso a base de datos; el atacante debe conocer o descubrir un ID existente asociado a la cuenta objetivo. Las inclusiones de esta ruta no exigen una sesión autenticada. El SELECT final no excluye registros utilizados o caducados.

RIESGO: Sustitución no autorizada de la contraseña de la cuenta asociada. El acceso posterior sigue dependiendo del estado activo y de los demás controles aplicables. RECOMENDACIÓN: Exigir una autorización aleatoria, con caducidad y de un solo uso, vinculada a la cuenta y a la verificación realizada; consumirla de forma atómica con el cambio de contraseña. Un ID secuencial no debe constituir autorización.

Confianza: alta; defecto confirmado en el código. Validación: trazado completo entre ruta, método y cliente, más una prueba aislada con sustitutos de base de datos en memoria. Se construyeron SELECT y UPDATE sin aportar token; no se consultaron ni modificaron filas reales. Comparación: el defecto de autorización permanece tras la conversión de mysql a mysqli.

### SEC-002 — P1: Inyección SQL en la verificación y el cambio final de contraseña

Evidencia: index_archivos/resetpassword/ajax/sendCredentials.php:2-11; ajax/resetPassword.php:2-11; index_archivos/resetpassword/ResetPassword.php:46-62,77-81.

COMPORTAMIENTO ACTUAL / DEFECTO CONFIRMADO: username y token se incorporan sin tratamiento al SELECT de verificación. identifier entra en una expresión de ID sin comillas; password se incorpora al argumento entre comillas de MD5() en el UPDATE. Estas rutas no enlazan parámetros ni escapan esos valores. El escape aplicado en ajax/generateToken.php:7-9 pertenece a otra ruta y no protege estas consultas.

Activación y precondiciones: Arranque correcto del punto de entrada, conexión utilizable y valores manipulados que alcancen los contextos SQL señalados. El UPDATE final requiere además seleccionar un registro de restablecimiento.

RIESGO: Alteración de la selección de registros, elusión de la verificación y modificación del UPDATE de la cuenta, dentro de los permisos del usuario de base de datos. No se acreditan consultas múltiples encadenadas, acceso universal a tablas, ejecución de comandos ni filas realmente afectadas. RECOMENDACIÓN: Parametrizar todos los valores, validar estrictamente los tipos de los identificadores y separar la autorización de restablecimiento de la construcción de SQL.

Confianza: alta; defecto confirmado en el código. Validación: trazado de entradas hasta las consultas completas; no se ejecutó ninguna inyección contra una base de datos. Comparación: la interpolación insegura se conserva en la migración a mysqli.

### SEC-003 — P1: La autenticación MFA confía en una identidad aportada por el cliente

Evidencia: index_archivos/2fa/ajax/autenticar.php:1-6; index_archivos/2fa/TwoFaClass.php:1-7,140-170,186-217; src/core/users/application/Find/UserFind.php:3-5; index_archivos/logAsgard.php:12-13,46-50.

COMPORTAMIENTO ACTUAL / DEFECTO CONFIRMADO: autenticar() decodifica el campo POST info como base64 y JSON y asigna a la sesión proveedor, usuario, tipo, tabla y campos de referencia. No comprueba contraseña, estado de cuenta, desafío OTP superado ni estado de autenticación pendiente firmado. La secuencia de verificar y después autenticar que ejecuta el navegador en index_archivos/2fa.php:64-78 no constituye un control de acceso del servidor. La consulta de verificación OTP de TwoFaClass.php:142 tampoco está limitada a una cuenta concreta.

Activación y precondiciones: La cadena de inclusiones debe alcanzar autenticar() y el solicitante debe aportar datos de identidad con la estructura esperada. UserFind.php se incluye anticipadamente e intenta incluir permisos.php mediante una ruta relativa; si esta se resuelve, puede interrumpir una solicitud anónima en PHP 8.4. Además, TwoFaClass.php:196 pasa al registro campos de una variable $row no definida. logAsgard::userInfo() puede construir entonces SQL inválido y fallar antes de generar el JWT. No se probó ni se presupone un inicio de sesión completo o la persistencia de la identidad tras el error.

RIESGO: Asignación de identidad de autenticación a la sesión sin comprobar ninguno de los factores, antes de posibles fallos posteriores de registro o JWT. RECOMENDACIÓN: Conservar en el servidor la identidad pendiente tras comprobar la contraseña; vincular y consumir el OTP validado para esa identidad antes de asignar campos de sesión autenticada; regenerar el ID de sesión y corregir el fallo de registro.

Confianza: alta para el defecto del código; explotación en producción sin verificar. Validación: trazado de inclusiones y llamadas, más una prueba del método aislado con un sustituto del registro que lanza deliberadamente una excepción. La identidad sintética ya estaba asignada en memoria antes de la excepción, sin aportar OTP. No se utilizó almacenamiento real de sesión, generación de JWT, base de datos ni red. Comparación: el defecto de confianza ya existía; master adelanta la inclusión de UserFind y sustituye los argumentos del registro por $row no definida, lo que añade las limitaciones de accesibilidad y ejecución descritas.

### SEC-004 — P1: La contraseña maestra sustituye a la contraseña individual de la cuenta

Evidencia: index_archivos/veriflogin.php:16-20,40-59,62-86,108-110.

COMPORTAMIENTO ACTUAL / DEFECTO CONFIRMADO: Una contraseña que coincida con cualquier resumen de master_pass activa la variable global isValid. La cuenta seleccionada supera entonces la decisión de contraseña mediante md5(password) === stored_hash OR isValid. La coincidencia no queda vinculada a ese usuario, a una sesión administradora ni a una operación de suplantación autorizada.

Activación y precondiciones: Token CSRF de acceso válido, nombre de usuario válido, conocimiento de una contraseña maestra aceptada, arranque y base de datos operativos y disponibilidad de password_verify(). Se sigue comprobando el estado activo; la rama normal mantiene MFA cuando está habilitada y la contraseña no ha caducado. PHP 5.4 nativo sin una función de compatibilidad puede detenerse en password_verify(), por lo que no se acredita la elusión en la imagen declarada.

RIESGO: El compromiso de una credencial compartida sustituye al primer factor en múltiples cuentas activas. La rama de contraseña caducada asigna identidad antes de mostrar el cambio de contraseña y antes de la rama normal de MFA; las capacidades resultantes requieren validación adicional. RECOMENDACIÓN: Eliminar la aceptación universal de contraseñas. Si se necesita suplantación operativa, implementarla de forma explícita, autorizada, temporal y con registro independiente.

Confianza: alta; flujo condicionado confirmado en el código. Validación: trazado del flujo de autenticación, sin utilizar credenciales maestras ni consultar datos reales. Comparación: presente en ambas referencias; no lo introduce el cambio de HSTS.

### SEC-005 — P1: La guardia compartida no termina las solicitudes denegadas cuando PHP antiguo continúa

Evidencia: index_archivos/permisos.php:1-27; index_archivos/tracking/ajax/borrarempresa.php:3-8; index_archivos/tracking/ajaxAsignacion/borrar_ubicacion.php:3-13.

COMPORTAMIENTO ACTUAL / DEFECTO CONFIRMADO: La guardia solo comprueba si idtransportista está definido. Cuando deniega, genera un formulario de envío automático en el navegador, pero no devuelve una respuesta 401/403 seguida de exit. Ignorar ese HTML no detiene el manejador que la incluye. Algunos puntos de entrada añaden comprobaciones propias; las consecuencias deben verificarse por ruta.

Activación y precondiciones: Entorno que continúe después de la constante de la línea 21, como el comportamiento habitual de PHP 5.4 o una definición previa de la constante; y un manejador con una operación SQL válida tras la inclusión. borrarempresa.php no incorpora otra comprobación ni depende de campos de sesión en su UPDATE. borrar_ubicacion.php utiliza deleted_by procedente de la sesión; su ausencia puede producir SQL inválido, por lo que no constituye evidencia anónima equivalente.

RIESGO: En el flujo de continuación antiguo, determinadas modificaciones protegidas pueden ejecutarse pese a la denegación. En PHP 8.4 local, la rama anónima genera Error; no se demuestra allí una modificación anónima mediante esta guardia. RECOMENDACIÓN: Exigir identidad y permisos de ruta en el servidor, devolver 401/403 y terminar con exit, eliminar la constante sobrante y comprobar las denegaciones de cada manejador.

Confianza: alta para la ausencia de terminación; impacto condicionado en PHP antiguo. Validación: pruebas aisladas con session_start sustituido en memoria para evitar archivos de sesión. La rama autenticada continuó en PHP 8.4 y la anónima generó Error. Definir la constante para simular exclusivamente la conversión antigua a cadena permitió continuar. No se ejecutó PHP 5.4. Comparación: master amplía las etiquetas cortas de apertura alrededor de la constante, pero no añade exit.

### SEC-006 — P1: Determinados manejadores de cuentas y negocio concatenan SQL controlado por la solicitud

Evidencia: index_archivos/tracking/ajax/borrarempresa.php:3-8; tracking/ajax/buscar-partida.php:2-18; index_archivos/embarques/ajax/saveDescripcionItems.php:2-9; index_archivos/usuario/ajax/update-password.php:2-10; usuario/UsuarioClass.php:12-33; index_archivos/HelperClass.php:1-3,20-28.

COMPORTAMIENTO ACTUAL / DEFECTO CONFIRMADO: El campo POST id forma la expresión WHERE del borrado lógico; partida del JSON entra en una expresión LIKE entre comillas; saveDescripcionItems obtiene la columna y el ID de componentes del nombre del campo POST e incorpora su valor sin tratamiento. El cambio de contraseña interpola identifier tanto en el SELECT de contraseña anterior como en el UPDATE final, sin vincularlo a la cuenta de la sesión. HelperClass ejecuta el SELECT recibido sin modificarlo.

Activación y precondiciones: Arranque y base de datos operativos. Como precondición común conservadora, se exige una sesión con idtransportista que supere permisos.php. La accesibilidad anónima depende de SEC-005 y de la versión de PHP.

RIESGO: La manipulación de predicados puede ampliar lecturas o modificaciones de negocio; la del identificador puede eludir la selección prevista para comprobar la contraseña anterior y ampliar cambios de cuentas. El daño depende de la sintaxis resultante y de los permisos de base de datos. No se acredita ejecución de consultas encadenadas ni compromiso de toda la base de datos. RECOMENDACIÓN: Consultas preparadas, identificadores enteros, lista explícita de columnas editables y comprobación de pertenencia de objetos y cuentas respecto de la sesión autenticada.

Confianza: alta; defecto confirmado en el código. Validación: cuatro trazas acotadas desde la entrada hasta la ejecución SQL, incluyendo guardia y HelperClass; no se ejecutó SQL. Comparación: la interpolación se conserva; sustituir mysql por mysqli no parametriza las consultas.

### SEC-007 — P2: Las contraseñas de usuario se almacenan y verifican mediante MD5 sin sal

Evidencia: index_archivos/veriflogin.php:83; index_archivos/resetpassword/ResetPassword.php:78-81; index_archivos/usuario/UsuarioClass.php:14-17,33.

COMPORTAMIENTO ACTUAL / DEFECTO CONFIRMADO: El acceso compara MD5; el restablecimiento escribe MD5() en SQL y el cambio de contraseña escribe md5() calculado por PHP. El resumen moderno usado para master_pass no migra las cuentas ordinarias.

Activación y precondiciones: Acceso a resúmenes de contraseñas, por ejemplo mediante una filtración de base de datos o copias de seguridad. RIESGO: Prueba rápida de contraseñas fuera de línea y compromiso por reutilización. MD5 por sí solo no demuestra una elusión remota del acceso. RECOMENDACIÓN: Migrar a una versión de PHP con soporte y a password_hash()/password_verify() con coste adecuado; actualizar todos los puntos de escritura y recalcular los valores antiguos tras una verificación correcta.

Confianza: alta; defecto confirmado en el código. Validación: trazado del acceso y de ambos mecanismos de escritura, sin recoger contraseñas. Comparación: el diseño antiguo permanece en master.

### SEC-008 — P2: La validación CSRF del acceso no protege determinadas modificaciones

Evidencia: index_archivos/login.php:2-6,92-93; veriflogin.php:16-20; index_archivos/permisos.php:7-27; tracking/ajax/borrarempresa.php:3-8; tracking/ajaxAsignacion/borrar_ubicacion.php:3-13; .htaccess:20-27.

COMPORTAMIENTO ACTUAL / DEFECTO CONFIRMADO: El acceso genera un token de sesión que veriflogin valida y elimina. Las dos rutas de modificación mediante formulario POST seleccionadas y su guardia común no comprueban token CSRF ni origen. Admiten campos de un formulario normal enviado desde otro sitio.

Activación y precondiciones: La víctima dispone de la sesión necesaria, el navegador envía la cookie en el POST entre sitios y la operación es accesible para esa identidad. Se desconocen la política SameSite real y los controles de origen anteriores a la aplicación. veriflogin.php:5 intenta configurar SameSite después de session_start(); PHP 5.4 nativo no admite esa opción. Esa instrucción no acredita una defensa general del despliegue.

RIESGO: Una página ajena puede inducir un borrado lógico autorizado con la identidad de la víctima cuando se cumple la precondición de envío de cookie. RECOMENDACIÓN: Validar tokens CSRF vinculados a la sesión en toda modificación, rechazar métodos y orígenes inapropiados y configurar las cookies antes de iniciar la sesión. Sustituir mt_rand() por un generador criptográficamente seguro para el token de acceso. No se demostró por separado una predicción de ese token.

Confianza: alta para la ausencia de protección en las rutas; explotación entre sitios condicionada. Validación: trazado completo de los formularios y de sus inclusiones compartidas, sin inferir vulnerabilidad a partir de recuentos de búsquedas. Comparación: la protección del acceso ya existía; las comprobaciones de negocio siguen ausentes.

### SEC-009 — P2: Las guardias de lectura comprueban la sesión, pero no la pertenencia del recurso

Evidencia: index_archivos/guardia_descargas_rel.php:1-5; download.php:2-10,16-40; index_archivos/tracking/guardia_imagen.php:1-5; tracking/getImage.php:2-17.

COMPORTAMIENTO ACTUAL / DEFECTO CONFIRMADO: Ambas guardias nuevas devuelven 403 y terminan si no reconocen ninguna identidad de sesión. La descarga rechaza referencias a directorios superiores y NUL en p y aplica basename() a f. La imagen rechaza f vacío, referencias a directorios superiores, NUL y barra inicial. Por tanto, la descripción anterior de acceso anónimo o recorrido de directorios no es válida para este master. Superadas las guardias, el archivo se lee mediante nombres relativos elegidos por el solicitante, sin comprobar su asociación con proveedor, viaje o cliente. La lista de extensiones de download.php se declara, pero no se aplica como control de tipos.

Activación y precondiciones: Identidad aceptada por la guardia, conocimiento o descubrimiento de un nombre relativo existente y legible y una regla de negocio que reserve ese recurso a otro proveedor o cliente. Se desconocen los permisos reales del almacenamiento y la política del despliegue.

RIESGO: Posible lectura de archivos de otra entidad dentro de la base de almacenamiento configurada. No se acredita lectura arbitraria de archivos del sistema ni una filtración real entre proveedores. RECOMENDACIÓN: Resolver identificadores opacos de documentos mediante una autorización de pertenencia en el servidor y limitar las rutas canónicas y los tipos admitidos como defensa adicional.

Confianza: alta para la ausencia de comprobación de pertenencia; media para el impacto, pendiente de las reglas de aislamiento. Validación: trazado del código, siete casos aislados reproducibles de guardias y las ocho pruebas de guardias de la auditoría general. No prueban el aislamiento entre proveedores. Comparación: las guardias de sesión y ruta son mejoras de master y se reconocen expresamente.

### SEC-010 — P2: Las subidas conservan tipos elegidos por el cliente antes de validar el contenido

Evidencia: index_archivos/tracking/ajax/cargar-imagenes-viaje.php:2-18; tracking/ajax/uploadExcelCargaMasiva.php:9-30; index_archivos/controllers/GlobalClass.php:16-33.

COMPORTAMIENTO ACTUAL / DEFECTO CONFIRMADO: El manejador de imágenes busca un evento de viaje y copia el contenido temporal multipart con un nombre cuya extensión procede del archivo recibido. No valida los bytes como imagen, el tipo MIME ni una lista de extensiones permitidas. La consulta del evento no se limita al proveedor de la sesión. El método de importación usa basename(), pero conserva cualquier extensión y mueve el archivo antes de que el llamador intente interpretarlo como Excel. La ruta inspeccionada no deshace ese movimiento si falla la lectura.

Activación y precondiciones: Sesión autenticada de proveedor, almacenamiento FILES_PATH escribible y, para imágenes, un evento coincidente con el viaje suministrado.

RIESGO: Almacenamiento de contenido no validado y posible asociación de archivos con el viaje de otro proveedor. La ejecución de código exigiría además que el almacenamiento se publicase con un manejador que ejecutase esas extensiones; esa configuración no se ha verificado, por lo que no se afirma ejecución remota. RECOMENDACIÓN: Autorizar primero el viaje, validar tamaño, tipo y contenido antes de mover el archivo, generar nombres en el servidor y almacenar fuera de las rutas web ejecutables, con ejecución desactivada.

Confianza: alta para la ausencia de validación y el orden de operaciones; consecuencias de ejecución condicionadas. Validación: dos trazas desde la entrada hasta el sistema de archivos; no se subió ni escribió ningún archivo en la aplicación. Comparación: la conservación de tipos inseguros permanece; los cambios mysql/mysqli no la corrigen.

### SEC-011 — P2: El transporte de correo activo desactiva la verificación TLS del certificado

Evidencia: index_archivos/MailClass.php:11-15,83-90; index_archivos/resetpassword/ResetPassword.php:102-103,249-259; index_archivos/2fa/TwoFaClass.php:19-21; index_archivos/embarques/EmbarqueClass.php:506-510,541-548; embarques/embarquesController.php:142.

COMPORTAMIENTO ACTUAL / DEFECTO CONFIRMADO: El transporte compartido de SendGrid y el de correo de embarques establecen CURLOPT_SSL_VERIFYPEER en false mientras envían una cabecera de autorización de tipo bearer y el contenido del mensaje. El restablecimiento y MFA llaman al método compartido: son flujos activos, no simples valores predeterminados de una biblioteca incluida.

Activación y precondiciones: Flujo cURL/correo operativo y capacidad del atacante para interceptar o redirigir la conexión utilizando un certificado que el cliente debería rechazar.

RIESGO: Exposición de la credencial del servicio de correo, de mensajes de restablecimiento/MFA o de información de negocio, y manipulación de respuestas. La comprobación del nombre de host por sí sola no restablece la validación de la cadena de confianza. RECOMENDACIÓN: Activar la verificación del certificado, mantener la del nombre de host, configurar certificados de autoridades de confianza y rechazar errores de transporte.

Confianza: alta; defecto confirmado en el código. Validación: trazado de los llamadores hasta cURL; no se enviaron correos ni se abrieron conexiones TLS. Comparación: MailClass.php no cambia respecto de la referencia; el segundo transporte activo también permanece en master.

### SEC-012 — P1: La credencial de correo incluida en el repositorio requiere rotación

Evidencia: index_archivos/cnfdb105.php:7. Se omiten el valor y cualquier fragmento del código que lo contenga.

DEFECTO CONFIRMADO: Existe una credencial de servicio de correo incorporada directamente en esa ubicación. Activación y precondiciones: Acceso a una copia o al historial del repositorio que incluya esa línea; su utilidad depende de la vigencia y de los permisos del servicio, que no se han probado.

RIESGO: Uso no autorizado del servicio de correo si la credencial sigue vigente. RECOMENDACIÓN: Revocar o rotar la credencial, revisar su uso histórico y sustituir el literal por un mecanismo controlado de suministro de secretos. Eliminar el literal sin rotación no es suficiente.

Confianza: alta para su presencia en el repositorio; vigencia desconocida. Validación: inspección local sin exponer el valor y comparación con la referencia; no se probó la credencial. Comparación: la asignación no cambia respecto de origin/master_peru. Las demás ubicaciones del archivo source-audits/master/2026-11-18/secret-locations.json son indicios para revisión; no equivalen a seis vías de explotación verificadas.

### SEC-013 — P2: Se distribuye un punto de entrada phpinfo sin restricción en la aplicación

Evidencia: info.php:1-2; .htaccess:1-16; Dockerfile:6.

COMPORTAMIENTO ACTUAL / DEFECTO CONFIRMADO: info.php llama directamente a phpinfo() sin guardia de aplicación. Las reglas de acceso de la raíz inspeccionadas no deniegan expresamente ese archivo.

Activación y precondiciones: El despliegue debe servir el archivo como PHP y ninguna regla previa del servidor o infraestructura debe bloquearlo.

RIESGO: Revelación de configuración, versiones de extensiones, rutas y, según la configuración, valores del entorno o de la solicitud. No se acredita que phpinfo() exponga la credencial de correo concreta. RECOMENDACIÓN: Excluir los diagnósticos de los archivos desplegables o restringirlos a un canal operativo autenticado.

Confianza: alta para la presencia del diagnóstico; exposición en el despliegue sin verificar. Validación: lectura completa del punto de entrada de dos líneas y de las reglas de raíz, sin solicitar la página. Comparación: info.php no cambia respecto de la referencia.

### SEC-014 — P2: El registro de acceso serializa la sesión e incluye su JWT

Evidencia: index_archivos/veriflogin.php:96-104; index_archivos/encodeUser.php:9-13; index_archivos/logAsgard.php:12-32,54-65.

COMPORTAMIENTO ACTUAL / DEFECTO CONFIRMADO: El acceso sin MFA asigna tokenJWT y después pasa la sesión completa a saveLog(). El registro convierte todos los campos recibidos a JSON para insertarlos en log_asgard_cloud, sin selección explícita ni eliminación de credenciales.

Activación y precondiciones: Acceso sin MFA y generación de JWT operativos, INSERT de registro correcto y acceso del tercero a la tabla, exportaciones o copias de seguridad.

RIESGO: Propagación de material de autenticación y metadatos de identidad al almacenamiento de registros. La posibilidad de reutilizar el JWT depende de su aceptación posterior, cuyo código está en un submódulo no poblado y permanece sin verificar. RECOMENDACIÓN: Registrar únicamente campos explícitamente autorizados del evento y la identidad; excluir tokens y credenciales y controlar la conservación y el acceso a los registros.

Confianza: alta para el flujo del token hasta el INSERT construido; media para sus consecuencias de reutilización. Validación: trazado entre acceso y registro, sin crear filas. Comparación: master migra el registro a mysqli, pero mantiene la serialización de toda la sesión.

Observaciones adicionales del registro: logAsgard.php:55 intenta obtener primero la IP pública del servidor mediante un comando dig fijo; después recurre a cabeceras de IP sin comprobar un proxy de confianza. Esto puede atribuir incorrectamente los eventos. No se demuestra inyección de comandos, ya que el comando es fijo. La interpolación directa de JSON y metadatos también puede provocar fallos de INSERT. Son cuestiones acotadas para revisión posterior, no hallazgos adicionales. No se ha acreditado la integridad del registro de intentos fallidos o restablecimientos.

## Validación reproducible y aspectos pendientes

El script scripts/audit/security_probes.py reproduce las doce pruebas aisladas con PHP 8.4 CLI. Lee la fuente indicada mediante --source y comprueba las huellas de los cinco archivos revisados antes de extraer métodos en memoria. No contiene copias del código de aplicación ni credenciales. Se ejecutó contra la copia auditada con PHP 8.4.25 y obtuvo doce resultados correctos, conservados en source-audits/master/2026-11-18/security-probes.json.

Las pruebas incluyen siete casos de imagen/descarga, tres de permisos —rama autenticada, Error anónimo de PHP 8.4 y simulación explícita de la constante antigua— y dos métodos aislados: restablecimiento sin token con funciones de base de datos simuladas y asignación de identidad MFA antes de una excepción deliberada de registro. session_start se sustituye solo en memoria; los métodos no ejecutan sus inclusiones. No se crean sesiones en disco ni se realizan operaciones reales sobre archivos de aplicación, bases de datos o red. La simulación de la constante no equivale a ejecutar PHP 5.4.

Para reproducir el resultado desde la raíz del paquete de conocimiento:

~~~powershell
python scripts/audit/security_probes.py --source C:/repos/proveedores-github-review-20261118 --output source-audits/master/2026-11-18/security-probes.json
~~~

El script requiere Python 3 y PHP 8.4 CLI, comprueba la coincidencia con la fuente revisada y solo permite guardar su JSON fuera del árbol de la aplicación. Si cambia la fuente, rechaza la ejecución; esas pruebas deben revisarse para una nueva versión.

Evidencias complementarias:

- source-audits/master/2026-11-18/guard-probes.json: ocho pruebas de guardias sobre el código fuente con resultado correcto, sin ejecutar manejadores, base de datos ni red. Acreditan la denegación y el filtrado de rutas comprobados, no la autenticación completa ni la pertenencia del recurso.
- source-audits/master/2026-11-18/php-lint.json: resultados sintácticos con PHP 8.4 descritos anteriormente; no acreditan ejecución en producción.
- source-audits/master/2026-11-18/secret-locations.json: metadatos de ubicación sin valores secretos.

Los inventarios de puntos de entrada, referencias SQL, Graphify y Brownfield sirven para orientar la cobertura. Las referencias SQL no son DDL ni prueban la existencia de tablas. Los recuentos de riesgos automáticos, puntos de ejecución SQL, operaciones de subida y nodos o relaciones del grafo no equivalen a vulnerabilidades verificadas. No se han transformado esos recuentos en hallazgos. El análisis nativo de Asgard no está disponible por la restricción de AppControl; su salida no forma parte de esta evidencia.

Aspectos pendientes (❓): versión real de PHP, funciones de compatibilidad y resolución de inclusiones; dependencias vendor y submódulos; esquema, permisos y datos de base de datos; enlaces simbólicos y publicación del almacenamiento; configuración efectiva de Apache, proxy TLS, cookies y orígenes; consumidores del JWT; límites de subida y analizadores de documentos; cobertura completa de autorización por punto de entrada; registros de producción, vigencia de la credencial y aislamiento entre proveedores. Requieren revisión autorizada de configuración o pruebas en un entorno de validación, sin inferencias a partir de comprobaciones sintácticas o coincidencias automáticas.

La comprobación anterior validó los catorce identificadores originales, sesenta intervalos y treinta y tres archivos normalizando CRLF/LF. La revisión iterativa añade SEC-015 y sus referencias; el [resultado actual de validación](../snapshots/current/knowledge-validation.json) comprueba el registro ampliado y las líneas en ambos pins. Se comprobó la ausencia del valor de la credencial en los entregables sin mostrarlo. El código de aplicación continúa sin modificaciones.

Este informe documenta defectos sustentados por evidencia del código y mantiene explícitas las incertidumbres de ejecución. No constituye una aprobación para producción.

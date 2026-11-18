# Actores, identidad y permisos observados

Auditoría estática del 18-11-2026. **AS-IS observado en fuente; no es una matriz de autorizaciones aprobada por negocio ni una prueba del despliegue.**

Base `M` = `master`, commit **a8ce2c23dead8552d2c4699e4a9b9134f7a18707**, inspeccionado en `C:/repos/proveedores-github-review-20261118`. Contraste `P` = `origin/master_peru`, commit **95fe9a4c3b3cddd84be922cc0e1eb9c88603df62**, leído mediante `git show`. Una referencia `M:ruta:Lx-Ly` fija commit, archivo y líneas; `P:` usa el segundo commit. Los IDs de evidencia de esta página son locales.

Lecturas complementarias: [flujos](workflows.md), [reglas](business-rules.md), [manual](user-manual.md), [Bolivia/master](../variants/bolivia.md) y [Perú](../variants/peru.md). El grafo histórico sirvió para localizar clases; contiene material de Perú y no acredita el comportamiento de M.

## Identidad de acceso y entidad representada

| Dato | Significado que demuestra el código | Evidencia |
|---|---|---|
| `idusuarioaccesoproveedor` | Cuenta individual de `prov_usuarioaccesoproveedor`; identifica permisos de menú y algunos autores | A01, A03 |
| `idtipoproveedor` | Tipo de entidad representada; selecciona ramas de interfaz y consultas | A01, A02, A04 |
| `idtransportista` en sesión | Se carga desde `idproveedor` para todos los tipos; el nombre no significa que toda cuenta sea transportista | A01 |
| `tabla`, `idutilizar` | Metadatos de `prov_tipoproveedor` copiados a sesión. El listado clásico de solicitudes utiliza `idutilizar` como nombre de columna | A01, A09 |
| `company_type` del payload | Clase de empresa para integraciones; se obtiene en `UserFinder`, no es el ID de permiso del menú | A02 |
| `tokenJWT` | Token guardado en sesión y utilizado por integraciones. Su existencia no demuestra autorización de cada endpoint PHP | A01, A07, A13 |

**Consecuencia observada:** hay operaciones con autor = cuenta y otras con autor = entidad representada. Por ejemplo, la cabecera de costos guarda `created_by = idtransportista` y su detalle usa `idusuarioaccesoproveedor`; no deben fusionarse ambos identificadores en informes de auditoría. [A10]

## Tipos de actor y constantes de integración

Los números siguientes son valores de `idtipoproveedor`, no valores demostrados de las constantes. `UserFinder` incluye `intercambioDocumental/companyTypes.php`; ese archivo pertenece a un submódulo no materializado en el checkout. Se observan los nombres de constantes referenciados, pero **❓ sus valores numéricos no se verificaron**. [A02, A14]

| Tipo | Actor según las relaciones leídas | Constante utilizada por `UserFinder` en M | Límite de la interpretación |
|---|---|---|---|
| 1 | Operador logístico; nombre de empresa desde `dav_transportista` | `OPERADOR_LOGISTICO` | No implica administrador global |
| 2 | Proveedor de mercancía; empresa desde `dav_proveedor` | `PROVEEDOR` | Tiene rama de consulta por `idproveedormercancia` |
| 3 | Agencia/agente de aduana; empresa desde `ada_agentesaduana` | `AGENCIA_DESPACHANTE` | Tiene rama por `idagentesaduana` |
| 4 | Agente de proveedor, según `idagenteproveedor` | No tiene caso específico; conserva el valor inicial `OPERADOR_LOGISTICO` | Es un desajuste observable del mapeo, no una equivalencia de negocio validada |
| 5 | Agente de seguro, según `idagenteseguro` | `AGENTE_SEGURO` | El `CASE company_name` de M solo contempla 1, 2 y 3 |
| 6 | Gestor/operador de transporte, según `gestor_transporte_id` | `OPERADOR_TRANSPORTE` | Tampoco tiene nombre de empresa resuelto por ese `CASE` |
| 99 | Tipo especial que habilita la rama «Registro de Solicitudes» del menú | Sin caso específico en M | ❓ No se puede denominar superusuario ni administrador a partir de esa condición |
| 7 en P | Concesionario, desde `cn_concesionario` | `CONCESIONARIO`, solo en P | P incorpora caso 7 y menús propios; no trasladar esa autorización a M |

Evidencia de la tabla: [A02, A04, A05, A12]. Las expresiones «gestor» y «operador de transporte» conviven en el código; no se ha confirmado que negocio las considere idénticas.

## Visibilidad del menú

`MenuClass` cuenta y obtiene filas mediante la relación `prov_proveedorusuariospermisos.idusuarioaccesoproveedor` → `prov_modulosproveedor.id`. Devuelve `descripcion`, `enlace` e `icono` del catálogo. Por eso no se puede reconstruir la lista real de subopciones de un usuario sin datos de configuración. Ambos menús (`menu.php` y `menu_b4.php`) aplican la misma estructura principal, con diferencias de presentación. [A03, A04]

| Grupo del catálogo | Condición visible en M | Qué puede afirmarse |
|---|---|---|
| 1 | Tipo 1 y cantidad de permisos > 0 | Se utiliza la primera opción devuelta; etiqueta dinámica |
| 2 | Tipo 99 y cantidad > 0 | Rama «Registro de Solicitudes»; la condición repite 99 en ambos operandos |
| 3 | Submenú «Logística» → «Embarques» | Cada enlace procede de los permisos de la cuenta |
| 4 | Tipo 1 o 6 | Submenú «Viajes», con opciones del catálogo; en Bootstrap 4 se ordenan por descripción |
| 5 | Tipo 1 | Submenú «Parametros», condicionado también a las filas disponibles |
| 6 | Permisos de pestañas del detalle | IDs de opciones: 11 Gestión Logistica, 12 Gestión Aduanera, 13 Costos, 14 Documentos, 15 Tracking, 16 Crear Viaje, 17 Descripción de Items, 20 Estado de Pedidos, 21 Servicios Adicionales, 22 Inventario; se añaden condiciones específicas [A18] |
| 7 | Existe al menos una fila del grupo | «Inventario por Chasis» usa el primer enlace |
| 8 / 9 | Iteración sobre los permisos correspondientes | «Reportes» / «Dashboard»; el contenedor puede aparecer sin opciones |
| 99 | Una fila tiene `enlace = #buscador_global` | Icono de búsqueda y modal «Buscar Embarques» |

Evidencia: [A03, A04]. P añade «Pedidos» (grupo 10, tipos 1/6/7) y «Pre Embarques» (grupo 15, tipos 1/7); son variantes documentadas por separado. [A12]

En detalle, Gestión Aduanera exige internacional y tipo 3/5/6; Tracking muestra una excepción explícita para cuenta ID 195 además del tipo 1. Crear Viaje exige tipo 1 y `fecha_finalizacion` vacía. Descripción de Items exige pedido asociado. Los costos reciben una bandera de edición según fecha de finalización. Son condiciones UI observadas, no una concesión universal de esos derechos en los endpoints. [A18]

## Alcance de datos: controles positivos observados

| Operación revisada | Restricción presente en el código | Lo que no acredita |
|---|---|---|
| Lista de embarques, tipo 1 | Unión de embarques con operador aceptado vinculado por `dav_clientetransportista` y embarques del propio `dav_transportista`; filtra alcance y borrado lógico | Autorización de escritura de cualquier ID obtenido |
| Lista de embarques, tipos 2–6 | Relación respectiva por proveedor de mercancía, agente de aduana, agente de proveedor, agente de seguro o gestor de transporte; `deleted_at IS NULL` y alcance | Una política uniforme para todos los tipos y rutas |
| Lista de viajes | `operador_id = idtransportista` de sesión y `deleted_at IS NULL` | Que el detalle, la edición o el borrado repitan ese predicado |
| Catálogo de clientes propios | `prov_clientes_proveedores.transportista_id` y borrado lógico | Que «cliente propio» sea el mismo concepto que `dav_cliente` |
| Solicitudes clásicas | Aprobadas, no anuladas, no liquidadas y columna de relación `idutilizar` igual a entidad de sesión | Acceso directo al detalle por otro ID |
| Descarga de documentos | Guardián con 403 si no hay ninguna de cuatro identidades de sesión; rechaza `..` y NUL en `p`; `download.php` aplica `basename` a `f` | Pertenencia del archivo a un proveedor concreto |

Evidencia: [A05, A06, A08, A09, A11]. El ámbito de una consulta no debe convertirse en garantía de todas las demás.

## Autenticación y sesión: secuencia realmente leída

1. `login.php` crea un token de sesión y lo incluye en el formulario. `veriflogin.php` comprueba el token, devuelve 403 si es inválido y lo consume. [A01]
2. El verificador limita usuario a caracteres alfanuméricos, `@._-`, longitud 25 y contraseña de longitud 50. Las ramas de formato/longitud asignan una URL y hacen `exit()` antes del formulario de retorno; no puede prometerse que muestren el error 3. [A01]
3. Se consulta la cuenta mediante PDO parametrizado. La validez admite la comparación MD5 de la contraseña de la cuenta **o** una coincidencia con los hashes de la tabla `master_pass`. Después se exige cuenta activa; `deleted_at` no nulo la considera inactiva. Esto describe un mecanismo técnico existente, no una autorización empresarial para su uso. [A01]
4. Si la contraseña alcanza 90 días, el flujo establece dos identidades de sesión y conduce a cambio de contraseña. Si no, decide por el campo `2fa`. En la rama sin MFA regenera el ID de sesión, carga identidad, crea JWT e intenta registrar inicio de sesión. [A01]
5. MFA envía seis dígitos por correo; el verificador acepta una antigüedad de hasta 600 segundos, consume el código y aumenta intentos fallidos; con contador > 3 pone `activo = NULL`. La consulta del código usa código, tipo `PROVEEDOR` y borrado lógico; no incluye correo, IP o cuenta. [A07]
6. La interfaz llama primero al verificador y después a `autenticar.php`. Ese endpoint llama directamente a `autenticar(info)`; el método decodifica la identidad recibida y carga sesión/JWT. En esta cadena leída no hay una comprobación de servidor que vincule el segundo paso a un código previamente verificado. **RISK observado en la implementación; ❓ impacto efectivo pendiente de prueba controlada y de controles externos.** [A07]
7. «Salir» ejecuta `session_destroy()`, elimina dos cookies de encuesta mediante JavaScript y redirige. «Volver a Ingresar» solo enlaza a login en el menú; no equivale a esa secuencia de salida. [A04, A15]

## Controles compartidos y sus límites

**AS-IS:** `permisos.php` llama a `session_start()` y pregunta si está definida `idtransportista`. Si falta, emite HTML para reenviar al login conservando POST y URL; no contiene una salida terminal ni consulta los permisos de módulo. Se inspeccionó completo y se siguieron sus inclusiones en pantallas y acciones concretas. No se está deduciendo la ausencia de controles mediante una búsqueda de texto. [A08]

**RISK:** el borrado/interrupción de viaje y el guardado de rating incluyen ese control compartido, pero sus acciones revisadas reciben IDs del cliente; los métodos de interrupción/borrado lógico operan por ID sin volver a filtrar por entidad ni estado previo. El rating toma incluso `usuario_id` de POST. Estos son límites de las cadenas leídas, no prueba de explotación, ni conclusión de que todo el sistema carezca de autorización. [A06, A16]

**AS-IS de configuración:** `cnfdb105.php` carga `.env.php`, autoload y zona `America/La_Paz`. El verificador de login establece cabeceras y opciones de cookie, algunas después de `session_start()`. ❓ La cookie efectiva, HTTPS, CSP aplicada, caducidad, sesiones compartidas y controles del servidor/proxy requieren observación en ejecución. No se reproducen valores de credenciales, claves de firma ni secretos de configuración. [A01, A17]

**Recuperación de contraseña:** el camino separado de MFA genera registro/correo, verifica código por usuario o correo y devuelve identificador del registro consumido. Su caducidad compara inicio del día actual con creación; no usa los 600 segundos de MFA. El endpoint final recibe contraseña e identificador; el método busca la solicitud por ID y actualiza la cuenta sin volver a comprobar token/antigüedad en esa función. **RISK de vinculación entre pasos**, pendiente de controles externos y prueba controlada; no se publica un procedimiento de acceso alternativo. [A19]

## Registro de evidencia

| ID | Localización exacta |
|---|---|
| A01 | `M:index_archivos/login.php:L1-L13,L90-L94`; `M:index_archivos/veriflogin.php:L1-L132` |
| A02 | `M:src/core/users/application/Find/UserFind.php:L3-L71` |
| A03 | `M:index_archivos/MenuClass.php:L11-L44` |
| A04 | `M:index_archivos/menu_b4.php:L98-L279`; `M:index_archivos/menu.php:L34-L154` |
| A05 | `M:index_archivos/embarques/EmbarqueClass.php:L187-L306`; `M:index_archivos/embarques/CotizacionClass.php:L265-L340` |
| A06 | `M:index_archivos/tracking/listaviajes.php:L1-L15,L273-L291`; `M:index_archivos/tracking/ListaViajesClass.php:L9-L100`; `M:index_archivos/tracking/HerramientasClass.php:L5-L47`; `M:index_archivos/tracking/ajax/delete_trip.php:L1-L7`; `M:index_archivos/tracking/ajax/discontinued-trip.php:L1-L10`; `M:index_archivos/tracking/ajax/eliminarviaje.php:L1-L7` |
| A07 | `M:index_archivos/2fa.php:L10-L14,L61-L80`; `M:index_archivos/2fa/TwoFaClass.php:L12-L39,L134-L218`; `M:index_archivos/2fa/ajax/autenticar.php:L1-L6`; `M:index_archivos/2fa/ajax/verificar-codigo.php:L1-L6` |
| A08 | `M:index_archivos/permisos.php:L1-L27`; `M:index_archivos/guardia_descargas_rel.php:L1-L5`; `M:index_archivos/download.php:L1-L42` |
| A09 | `M:index_archivos/versolicitud.php:L59-L103` |
| A10 | `M:index_archivos/embarques/CostosClass.php:L382-L390,L576-L590` |
| A11 | `M:index_archivos/parametros/clientes/ClienteProveedorClass.php:L12-L19` |
| A12 | `P:src/core/users/application/Find/UserFind.php:L25-L63`; `P:index_archivos/menu_b4.php:L148-L172` |
| A13 | `M:index_archivos/tracking/TrackingNewClass.php:L967-L989` |
| A14 | `M:.gitmodules:L1-L8`; gitlink `M:index_archivos/intercambioDocumental` = `dc840f9dd80d5d0bda0f31c343a0f9f877519327` |
| A15 | `M:index_archivos/logout.php:L1-L17` |
| A16 | `M:index_archivos/rating/rating.php:L1-L13`; `M:index_archivos/rating/RatingClass.php:L1-L29` |
| A17 | `M:index_archivos/cnfdb105.php:L1-L3,L11,L29-L37` |
| A18 | `M:index_archivos/embarques/embarquever.php:L128-L144,L219-L284`; `M:index_archivos/embarques/frames/costos.php:L51-L68` |
| A19 | `M:index_archivos/resetpassword/ResetPassword.php:L11-L94`; `M:index_archivos/resetpassword/ajax/generateToken.php:L1-L13`; `M:index_archivos/resetpassword/ajax/sendCredentials.php:L1-L13`; `M:index_archivos/resetpassword/ajax/resetPassword.php:L1-L13` |

## Verificación y brechas

El 18-11-2026 se ejecutó `php -l` con PHP CLI 8.4.25 sobre `permisos.php`, `veriflogin.php`, `TrackingNewClass.php` y `embarquesController.php`: sin errores de sintaxis; `TrackingNewClass::origins` emite aviso de parámetro opcional anterior a obligatorio en L799. Esta comprobación no ejecuta autenticación ni consultas y no acredita compatibilidad con PHP 5.4, declarado en `M:Dockerfile:L1-L6`. Asgard nativo no ejecutado por bloqueo de Windows App Control comunicado en la revisión; se utilizó análisis estático alternativo. No se realizaron peticiones ni envíos a servicios reales.

❓ Pendientes: catálogo real de tipos y permisos por cuenta; valores de constantes del submódulo; correspondencia entre tipo 4 y payload; revisión de MFA con sus controles externos; pruebas de aislamiento entre dos proveedores; privilegios SQL del usuario de aplicación; política de quién puede reactivar una cuenta. Ninguno se presenta como requisito validado ni como un PASS de seguridad.

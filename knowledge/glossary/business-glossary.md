# Glosario de negocio de Proveedores

Revisión de fuente: **18 de noviembre de 2026**. Contiene **81 conceptos de negocio** redactados en español, con significado local, uso, relaciones, alias y evidencia. Es un diccionario operativo revisado contra código; **no hay entradas aprobadas por un responsable de negocio ni validación de ejecución**.

[Diccionario e índice JSON](business-glossary.json) · [Registro de revisión y asuntos pendientes](review-register.md)

## Procedencia y lectura

Las referencias identifican archivos de la aplicación privada; se publican únicamente paráfrasis y ubicaciones, sin código fuente, credenciales ni datos de clientes.

| Referencia | Commit fijado |
| --- | --- |
| `master` | `a8ce2c23dead8552d2c4699e4a9b9134f7a18707` |
| `origin/master_peru` | `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` |

Repositorio inspeccionado: `C:/repos/proveedores-github-review-20261118`. Las líneas son inclusivas y corresponden al archivo en el commit citado, no a un checkout posterior. Se leyeron clases, formularios, componentes y consultas de ambos commits; una ruta coincidente no bastó para declarar significado compartido.

| Marca | Cómo interpretarla |
| --- | --- |
| `observed` | Significado o comportamiento local explícito en la fuente. |
| `inferred` | Interpretación funcional de relaciones observadas; requiere confirmación de negocio. |
| `unknown` | Uso local acotado; acepción precisa o expansión de sigla sin confirmar. |
| `shared_evidence` | Significado contrastado en ambas ramas con citas independientes; no afirma implementaciones idénticas. |
| `master` | Acepción documentada en master sin extenderla automáticamente a Perú. |
| `peru` | Variante o flujo documentado en la rama Perú; no acredita exclusividad territorial absoluta. |
| `bolivia` | Ámbito reservado sin entradas asignadas: no se deriva del nombre de rama ni de la zona horaria del contenedor. |

Distribución: **76** conceptos compartidos, **1** de master y **4** variantes de Perú; **69 observed**, **9 inferred** y **3 unknown**. Las inferencias y dudas forman parte de la revisión, no se presentan como hechos confirmados.

## Relaciones que evitan confusiones

| Conceptos | Distinción operativa |
| --- | --- |
| Cotización → embarque → viajes | La aceptación del operador cambia un indicador del registro de cotización; los viajes se asignan por separado y contienen empresa, conductor, carga y localizaciones. No representa una secuencia obligatoria de todas las altas. |
| Tramo / ruta / viaje | El tramo describe ubicaciones de una parte del trayecto; la ruta informa recorrido, fechas y modalidad; el viaje es la asignación de transporte. |
| Orden de compra / pedido | El formulario distingue ambas referencias. «Pedido» se guarda en `ordencompra` y «Orden de Compra» en `ordencompraini`. Hay además pedidos operativos con posiciones. |
| Proveedor / operador / transportista | El suministrador de mercancía, el operador logístico, la empresa del viaje y el conductor son papeles diferentes. Algunos identificadores y nombres de funciones son homónimos. |
| Estado / EDP | Conviven catálogo de estados de embarque, estado de viaje, historial EDP, resumen calculado y filtros de solicitudes aduaneras. Sus etiquetas no son equivalencias automáticas. |
| Inventario / existencias | El módulo revisado muestra inspecciones de vehículos en distintos momentos. No acredita un saldo de stock, una valoración contable ni disponibilidad de venta. |

Los enlaces de cada entrada llevan a las referencias exactas que sustentan estas distinciones.

## Índice alfabético

| Concepto | Ámbito | Confianza |
| --- | --- | --- |
| [Accesorio inventariado](#accesorio) | `shared_evidence` | `observed` |
| [Aceptación de la cotización del operador](#aceptacion-cotizacion) | `shared_evidence` | `observed` |
| [Aceptado en el resumen del embarque](#aceptado-resumen) | `shared_evidence` | `observed` |
| [Aduana seleccionada](#aduana) | `shared_evidence` | `observed` |
| [Agente de aduana](#agente-aduana) | `shared_evidence` | `observed` |
| [Agente de seguro](#agente-seguro) | `shared_evidence` | `observed` |
| [Agente del proveedor de mercancía](#agente-proveedor) | `shared_evidence` | `observed` |
| [Alcance del viaje](#alcance-viaje) | `shared_evidence` | `observed` |
| [Almacén del cliente](#almacen-cliente) | `shared_evidence` | `observed` |
| [Bulto y tipo de bulto](#bulto) | `shared_evidence` | `observed` |
| [Carpeta del caso](#carpeta) | `shared_evidence` | `observed` |
| [Caso aduanero](#caso-aduanero) | `shared_evidence` | `inferred` |
| [Categoría de costo](#categoria-costo) | `shared_evidence` | `observed` |
| [Chasis como identificador de vehículo](#chasis) | `shared_evidence` | `observed` |
| [Clase de mercancía](#clase-mercancia) | `shared_evidence` | `observed` |
| [Cliente de la operación logística](#cliente-logistico) | `shared_evidence` | `observed` |
| [Cliente propio del operador](#cliente-del-operador) | `shared_evidence` | `observed` |
| [Código UN de mercancía](#codigo-un) | `shared_evidence` | `inferred` |
| [Concepto de costo](#concepto-costo) | `shared_evidence` | `observed` |
| [Concesionario asociado al cliente](#concesionario-cliente) | `peru` | `observed` |
| [Conductor](#conductor) | `shared_evidence` | `observed` |
| [Conductor de relevo](#conductor-relevo) | `shared_evidence` | `observed` |
| [Contaminación en la revisión del vehículo](#contaminacion) | `shared_evidence` | `observed` |
| [Contenedor](#contenedor) | `shared_evidence` | `observed` |
| [Cotización logística](#cotizacion) | `shared_evidence` | `observed` |
| [Creación de viaje desde VIN seleccionados](#viaje-desde-vin) | `peru` | `observed` |
| [DAM en el control de solicitudes](#dam) | `shared_evidence` | `unknown` |
| [Declarante del cliente](#declarante) | `shared_evidence` | `observed` |
| [Desperfecto del vehículo](#desperfecto) | `shared_evidence` | `observed` |
| [Documento adjunto del embarque](#documento-adjunto) | `shared_evidence` | `observed` |
| [Documento de soporte del viaje](#documento-soporte-viaje) | `shared_evidence` | `observed` |
| [Documento previo de la solicitud](#documento-previo) | `shared_evidence` | `observed` |
| [DUI en la clasificación de despacho](#dui) | `shared_evidence` | `unknown` |
| [Embarque](#embarque) | `shared_evidence` | `inferred` |
| [Empresa de transporte del viaje](#empresa-transporte) | `shared_evidence` | `observed` |
| [En proceso en el resumen del embarque](#en-proceso-resumen) | `shared_evidence` | `observed` |
| [Enviado en el resumen del embarque](#enviado-resumen) | `shared_evidence` | `observed` |
| [Estado de la asignación de viaje](#estado-viaje) | `shared_evidence` | `inferred` |
| [Estado de pedidos (EDP)](#edp) | `shared_evidence` | `observed` |
| [Estado del catálogo de embarques](#estado-catalogo-embarque) | `shared_evidence` | `observed` |
| [Estado resumen calculado del embarque](#estado-resumen) | `shared_evidence` | `observed` |
| [Estados de las listas de solicitudes aduaneras](#estados-solicitud-aduanera) | `shared_evidence` | `inferred` |
| [Fecha límite de cierre de tránsito](#cierre-transito) | `shared_evidence` | `observed` |
| [Finalizado en el resumen del embarque](#finalizado-resumen) | `shared_evidence` | `observed` |
| [Fotografías 360° del inventario](#fotografias-360) | `peru` | `observed` |
| [Gestor de transporte](#gestor-transporte) | `shared_evidence` | `inferred` |
| [Incoterm seleccionado](#incoterm) | `shared_evidence` | `observed` |
| [Inventario de depósito transitorio](#inventario-deposito) | `shared_evidence` | `observed` |
| [Inventario de despacho y recepción](#inventario-nacional-local) | `shared_evidence` | `observed` |
| [Inventario del vehículo](#inventario-vehicular) | `shared_evidence` | `observed` |
| [Inventario en puerto de carga](#inventario-puerto) | `shared_evidence` | `observed` |
| [Inventario post nacionalización](#inventario-post-nacionalizacion) | `shared_evidence` | `observed` |
| [Ítem o posición del pedido](#item-posicion) | `shared_evidence` | `observed` |
| [Magnitudes de la carga](#magnitudes-carga) | `shared_evidence` | `observed` |
| [Modalidad de transporte](#modalidad-transporte) | `shared_evidence` | `observed` |
| [Moneda del costo](#moneda-costo) | `shared_evidence` | `observed` |
| [Operador logístico](#operador-logistico) | `shared_evidence` | `observed` |
| [Orden de compra de referencia](#orden-compra) | `shared_evidence` | `observed` |
| [Origen y destino del viaje](#origen-destino) | `shared_evidence` | `observed` |
| [Parte de recepción](#parte-recepcion) | `master` | `inferred` |
| [Partida del inventario](#partida-inventario) | `shared_evidence` | `unknown` |
| [Pedido de referencia](#pedido-referencia) | `shared_evidence` | `observed` |
| [Pedido operativo](#pedido-operativo) | `shared_evidence` | `observed` |
| [Pendiente en el resumen del embarque](#pendiente-resumen) | `shared_evidence` | `observed` |
| [Peso y peso bruto de la carga](#peso-carga) | `shared_evidence` | `observed` |
| [Propuesta de costos del operador](#propuesta-costos) | `shared_evidence` | `observed` |
| [Proveedor de mercancía](#proveedor-mercancia) | `shared_evidence` | `observed` |
| [Régimen de la solicitud](#regimen-aduanero) | `shared_evidence` | `observed` |
| [Registro de kilometraje con imagen](#registro-kilometraje-imagen) | `peru` | `observed` |
| [Revisión de cotización](#revision-cotizacion) | `shared_evidence` | `observed` |
| [Ruta autorizada del viaje](#ruta-autorizada) | `shared_evidence` | `observed` |
| [Ruta del embarque](#ruta-embarque) | `shared_evidence` | `observed` |
| [Sentido del viaje](#sentido-viaje) | `shared_evidence` | `observed` |
| [Solicitud de gestión aduanera](#solicitud-aduanera) | `shared_evidence` | `observed` |
| [Tipo de carga o carguío](#tipo-carga) | `shared_evidence` | `observed` |
| [Tipo de declaración](#tipo-declaracion) | `shared_evidence` | `observed` |
| [Tipo de mercancía](#tipo-mercancia) | `shared_evidence` | `observed` |
| [Trámite de una solicitud](#tramite) | `shared_evidence` | `inferred` |
| [Tramo del embarque](#tramo) | `shared_evidence` | `inferred` |
| [Viaje](#viaje) | `shared_evidence` | `observed` |
| [Volumen de la carga](#volumen-carga) | `shared_evidence` | `observed` |

## Actores

<a id="cliente-logistico"></a>
### Cliente de la operación logística

**Definición.** Organización seleccionada como solicitante del embarque y vinculada al catálogo general de clientes. Sus relaciones determinan proveedores, operadores de transporte y almacenes disponibles.

**Uso y relaciones.** Distinguir del cliente propio del operador y de la persona solicitante; el selector «Solicitante» usa el identificador del cliente.

**Alias de búsqueda:** cliente; solicitante del embarque. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E001](#e001), [E002](#e002), [E003](#e003), [E004](#e004).

<a id="cliente-del-operador"></a>
### Cliente propio del operador

**Definición.** Cliente que el operador mantiene en su directorio, con nombre, identificación, dirección y contacto, asociado al operador que lo registra.

**Uso y relaciones.** Es un directorio distinto del catálogo general de clientes del embarque; no asumir identidad ni equivalencia de claves entre ambos.

**Alias de búsqueda:** cliente del proveedor; cliente externo del operador. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E005](#e005), [E006](#e006).

<a id="proveedor-mercancia"></a>
### Proveedor de mercancía

**Definición.** Actor que suministra la mercancía y se referencia en los datos del embarque y de la solicitud aduanera. El código lo distingue del operador logístico y del gestor de transporte.

**Uso y relaciones.** «Proveedor» sin contexto es ambiguo: aquí designa al suministrador de bienes, no al conductor ni a toda empresa de transporte.

**Alias de búsqueda:** proveedor de bienes; proveedor. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E007](#e007), [E008](#e008), [E009](#e009), [E010](#e010).

<a id="operador-logistico"></a>
### Operador logístico

**Definición.** Actor asociado al cliente para gestionar el transporte del embarque. La consulta del operador elegido recupera la relación cliente–transportista cuya propuesta figura aceptada.

**Uso y relaciones.** Distinguir la empresa del catálogo, su relación con el cliente y el usuario de acceso; sus identificadores no son intercambiables.

**Alias de búsqueda:** operador de transporte; transportista del catálogo. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E011](#e011), [E012](#e012), [E013](#e013), [E014](#e014).

<a id="empresa-transporte"></a>
### Empresa de transporte del viaje

**Definición.** Empresa registrada en un viaje junto con placa, tipo de unidad y capacidad. Es parte de la asignación concreta de transporte.

**Uso y relaciones.** El viaje conserva estos datos asociados; no confundir esta empresa con la relación cliente–operador ni con el conductor.

**Ejemplo observado.** El alta del viaje guarda el nombre de empresa junto con placa, tipo de unidad y capacidad.

**Alias de búsqueda:** empresa transportista; carrier. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E015](#e015), [E016](#e016).

<a id="conductor"></a>
### Conductor

**Definición.** Persona asignada al viaje, registrada con nombre y datos de identificación, contacto y licencia. La creación del viaje guarda al conductor principal.

**Uso y relaciones.** En este contexto «transportista» también puede nombrar a la persona conductora; distinguirla de la empresa de transporte.

**Alias de búsqueda:** chofer; transportista del viaje; driver. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E017](#e017), [E018](#e018), [E019](#e019), [E020](#e020).

<a id="conductor-relevo"></a>
### Conductor de relevo

**Definición.** Segunda asignación de conductor del viaje, guardada con un tipo de conductor distinto del principal.

**Uso y relaciones.** Comparte estructura con el conductor principal; el tipo identifica su papel en el viaje.

**Alias de búsqueda:** chofer de relevo. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E021](#e021), [E022](#e022).

<a id="gestor-transporte"></a>
### Gestor de transporte

**Definición.** Actor diferenciado del operador logístico y del agente de aduana que figura entre los participantes del embarque y destinatarios de actualizaciones de pedidos.

**Uso y relaciones.** La evidencia acredita su participación y notificación; no delimita todas sus responsabilidades contractuales.

**Alias de búsqueda:** gestor. **Ámbito:** `shared_evidence`. **Confianza:** `inferred`.

**Evidencia:** [E023](#e023), [E024](#e024).

<a id="agente-aduana"></a>
### Agente de aduana

**Definición.** Actor aduanero asignado al embarque y consultado por nombre desde su catálogo. Participa en las notificaciones de estado junto con cliente, gestor y operador.

**Uso y relaciones.** No equivale a la aduana como dependencia ni al declarante configurado para el cliente.

**Alias de búsqueda:** agente aduanero. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E025](#e025), [E026](#e026), [E027](#e027), [E028](#e028).

<a id="agente-seguro"></a>
### Agente de seguro

**Definición.** Actor del catálogo de agentes de seguro vinculado al embarque y recuperado por nombre.

**Uso y relaciones.** La vinculación no acredita por sí misma contratación, cobertura ni vigencia de una póliza.

**Alias de búsqueda:** agente de seguros. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E029](#e029), [E030](#e030).

<a id="agente-proveedor"></a>
### Agente del proveedor de mercancía

**Definición.** Actor asociado a proveedores de mercancía que puede seleccionarse y asignarse al embarque.

**Uso y relaciones.** La lista se obtiene por proveedor; el nombre de un parámetro «transportista» no convierte a este agente en empresa de transporte.

**Alias de búsqueda:** agente proveedor. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E031](#e031), [E032](#e032).

<a id="declarante"></a>
### Declarante del cliente

**Definición.** Registro activo de declarante asociado al cliente, que puede marcarse como principal y seleccionarse en la gestión aduanera.

**Uso y relaciones.** Es distinto del cliente solicitante y del agente de aduana. El código consultado no fija su representación jurídica.

**Alias de búsqueda:** cliente declarante. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E033](#e033), [E034](#e034).

## Operación y carga

<a id="cotizacion"></a>
### Cotización logística

**Definición.** Solicitud de valoración del transporte que registra cliente, mercancía, magnitudes y trayecto. Se lista como cotización mientras el indicador correspondiente está activado en el mismo registro utilizado para el embarque.

**Uso y relaciones.** Se relaciona con propuestas de operadores; la aceptación de una propuesta desactiva el indicador de cotización.

**Ejemplo observado.** La aceptación marca al operador elegido y cambia el registro de cotización a embarque.

**Alias de búsqueda:** cotización; solicitud de cotización. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E035](#e035), [E036](#e036), [E037](#e037), [E038](#e038).

<a id="embarque"></a>
### Embarque

**Definición.** Unidad de gestión logística que reúne datos de cliente y carga y sirve de referencia para documentos, rutas, solicitudes aduaneras y viajes. En la conversión desde cotización se conserva el registro y se cambia su indicador.

**Uso y relaciones.** No equivale a un viaje individual: los viajes se vinculan por separado al embarque.

**Alias de búsqueda:** operación logística. **Ámbito:** `shared_evidence`. **Confianza:** `inferred`.

**Evidencia:** [E037](#e037), [E038](#e038), [E039](#e039), [E040](#e040), [E041](#e041), [E042](#e042), [E043](#e043), [E044](#e044).

<a id="viaje"></a>
### Viaje

**Definición.** Asignación concreta de transporte con información de orden, empresa, conductor, carga, orígenes, destinos y documentos de soporte. Puede recuperarse sin embarque y vincularse después a uno.

**Uso y relaciones.** Distinguir del embarque y de su ruta informativa; un viaje tiene sus propios datos y estado.

**Alias de búsqueda:** asignación de viaje; journey. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E045](#e045), [E046](#e046), [E043](#e043), [E044](#e044).

<a id="alcance-viaje"></a>
### Alcance del viaje

**Definición.** Clasificación del ámbito del traslado obtenida del catálogo de tipos de viaje y guardada en la asignación. No es la misma selección que el sentido de ida o vuelta.

**Uso y relaciones.** La pantalla y las reglas distinguen contextos internacional, nacional y local; no deducir fronteras o distancias de un número de catálogo.

**Alias de búsqueda:** alcance; tipo de viaje del embarque. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E047](#e047), [E048](#e048), [E049](#e049), [E050](#e050), [E051](#e051), [E052](#e052), [E053](#e053), [E054](#e054).

<a id="sentido-viaje"></a>
### Sentido del viaje

**Definición.** Elección entre solo ida, ida y vuelta o solo vuelta en la asignación de transporte.

**Uso y relaciones.** Se guarda como tipo de viaje de la asignación; no confundir con el alcance nacional, internacional o local.

**Ejemplo observado.** El selector ofrece «Solo Ida», «Ida y Vuelta» y «Solo vuelta».

**Alias de búsqueda:** solo ida; ida y vuelta; solo vuelta; tipo de viaje de la asignación. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E055](#e055), [E056](#e056).

<a id="modalidad-transporte"></a>
### Modalidad de transporte

**Definición.** Selección que caracteriza cómo se transporta la carga y que la pantalla del embarque denomina «Modalidad de Transporte». La presentación de rutas distingue transporte marítimo, aéreo, terrestre y ferroviario mediante catálogos de empresas diferentes.

**Uso y relaciones.** El identificador de tipo de embarque y el de modo de transporte proceden de estructuras distintas; no igualarlos por su valor numérico.

**Alias de búsqueda:** tipo de embarque; modo de transporte. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E057](#e057), [E058](#e058), [E059](#e059), [E060](#e060).

<a id="tramo"></a>
### Tramo del embarque

**Definición.** Parte numerada del trayecto descrita mediante registros de ubicación y tipo: región, localidad, puerto o aeropuerto, lugar de entrega y tipo de carga.

**Uso y relaciones.** Sirve para representar los puntos del trayecto previsto en la cotización o el embarque; no equivale a una asignación de conductor.

**Alias de búsqueda:** tramo logístico. **Ámbito:** `shared_evidence`. **Confianza:** `inferred`.

**Evidencia:** [E061](#e061), [E062](#e062).

<a id="ruta-embarque"></a>
### Ruta del embarque

**Definición.** Registro de recorrido que informa origen y destino, localidades de salida y arribo, fechas, tiempo de tránsito y modalidad o empresa de transporte.

**Uso y relaciones.** Se consulta y añade al embarque por separado de los tramos de cotización y del viaje terrestre.

**Alias de búsqueda:** itinerario; ruta. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E063](#e063), [E064](#e064).

<a id="origen-destino"></a>
### Origen y destino del viaje

**Definición.** Lugares de salida y llegada guardados como colecciones separadas al crear el viaje. Pueden contener ítems y cantidades asociados a cada localización.

**Uso y relaciones.** Distinguir del par de puntos mostrado en una ruta informativa del embarque.

**Alias de búsqueda:** localizaciones del viaje; puntos de carga y entrega. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E065](#e065), [E066](#e066), [E067](#e067), [E068](#e068).

<a id="orden-compra"></a>
### Orden de compra de referencia

**Definición.** Referencia comercial capturada por la pantalla como «Orden de Compra» y guardada en el campo inicial de orden de compra del embarque.

**Uso y relaciones.** Coexiste con una referencia «Pedido» en otro campo; el código no demuestra aquí un proceso completo de aprobación de compras.

**Alias de búsqueda:** OC; ordencompraini. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E069](#e069), [E070](#e070).

<a id="pedido-referencia"></a>
### Pedido de referencia

**Definición.** Referencia que la pantalla del embarque etiqueta «Pedido», aunque se almacena en un campo denominado ordencompra.

**Uso y relaciones.** No confundir con la orden de compra contigua ni con el pedido operativo con cabecera y posiciones.

**Ejemplo observado.** En el mismo formulario hay dos entradas: «Orden de Compra» y «Pedido».

**Alias de búsqueda:** pedido del embarque; ordencompra. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E069](#e069), [E070](#e070).

<a id="pedido-operativo"></a>
### Pedido operativo

**Definición.** Agrupación de posiciones con cabecera vinculada a proveedor, cliente y embarque y con un detalle de posiciones. Hay una rutina que lo crea a partir de chasis en un caso local condicionado.

**Uso y relaciones.** La creación automática revisada depende de un cliente concreto y del alcance local; no extenderla a todos los clientes o embarques.

**Ejemplo observado.** La rutina local divide una lista de chasis y crea una posición por elemento; su llamada está condicionada a un cliente.

**Alias de búsqueda:** pedido con posiciones; pedido logístico. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E071](#e071), [E072](#e072), [E073](#e073), [E074](#e074).

<a id="item-posicion"></a>
### Ítem o posición del pedido

**Definición.** Unidad de detalle identificada por una posición y asociada a un pedido. La pantalla muestra descripción, SKU y ubicación; en el caso vehicular la posición se genera a partir del chasis.

**Uso y relaciones.** El significado de posición depende de la carga; no asumir que todo SKU o posición es un VIN.

**Alias de búsqueda:** ítem; posición; item. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E075](#e075), [E076](#e076), [E077](#e077), [E078](#e078).

<a id="bulto"></a>
### Bulto y tipo de bulto

**Definición.** Unidad de agrupación de carga cuyo tipo se elige de un catálogo de unidades y se relaciona con cantidades en las magnitudes o localizaciones.

**Uso y relaciones.** Distinguir la cantidad de bultos de su tipo y de la cantidad de contenedores.

**Alias de búsqueda:** tipo de bulto; unidad de bulto. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E079](#e079), [E080](#e080), [E081](#e081), [E082](#e082).

<a id="tipo-carga"></a>
### Tipo de carga o carguío

**Definición.** Clasificación de carga seleccionada en los datos de trayecto y guardada también en la orden del viaje.

**Uso y relaciones.** La interfaz de tramos usa «Tipo de Carguío»; no confundir esta clasificación con tipo de mercancía o tipo de bulto.

**Alias de búsqueda:** tipo de carguío. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E083](#e083), [E084](#e084), [E085](#e085), [E086](#e086).

<a id="tipo-mercancia"></a>
### Tipo de mercancía

**Definición.** Clasificación de la mercancía seleccionada desde un catálogo y almacenada en el embarque y la orden del viaje.

**Uso y relaciones.** Es el nivel del que depende la clase de mercancía; no se han validado los valores completos del catálogo ni obligaciones externas.

**Alias de búsqueda:** mercancía; tipoMercancia. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E087](#e087), [E088](#e088), [E085](#e085), [E086](#e086).

<a id="clase-mercancia"></a>
### Clase de mercancía

**Definición.** Clasificación dependiente del tipo de mercancía que permite seleccionar un registro de clase; de esa clase depende el selector UN.

**Uso y relaciones.** No atribuir a una clase una categoría regulatoria concreta sin revisar el valor y su uso operativo.

**Alias de búsqueda:** clase. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E089](#e089), [E090](#e090).

<a id="codigo-un"></a>
### Código UN de mercancía

**Definición.** Valor denominado UN que la aplicación selecciona de un catálogo dependiente de la clase de mercancía y guarda en la orden del viaje.

**Uso y relaciones.** Se observa su uso como dato de clasificación; la fuente revisada no valida significado normativo, valores ni condiciones de transporte.

**Alias de búsqueda:** UN; número UN. **Ámbito:** `shared_evidence`. **Confianza:** `inferred`.

**Evidencia:** [E091](#e091), [E092](#e092), [E085](#e085), [E086](#e086).

<a id="incoterm"></a>
### Incoterm seleccionado

**Definición.** Condición comercial de la operación elegida desde el catálogo de Incoterms en el formulario internacional. Interviene en la selección de conceptos de costos.

**Uso y relaciones.** El glosario documenta su uso en la aplicación; no define versiones de reglas, reparto de riesgos ni obligaciones contractuales.

**Alias de búsqueda:** Incoterms. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E093](#e093), [E094](#e094), [E095](#e095), [E096](#e096).

<a id="magnitudes-carga"></a>
### Magnitudes de la carga

**Definición.** Conjunto de medidas y cantidades del embarque: tipo y cantidad de bultos, peso, peso bruto, dimensiones y volumen, con sus unidades.

**Uso y relaciones.** Pueden existir varias líneas de dimensiones y volumen y registros de contenedores relacionados.

**Ejemplo observado.** El alta permite varias líneas de dimensiones y volumen dentro de las magnitudes del embarque.

**Alias de búsqueda:** dimensiones de carga; medidas de carga. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E097](#e097), [E098](#e098).

<a id="contenedor"></a>
### Contenedor

**Definición.** Elemento de la descripción logística que se registra mediante tipo y cantidad en las magnitudes del embarque y mediante datos específicos en la orden del viaje.

**Uso y relaciones.** El catálogo separa selectores de tipo y número; no asumir que todo valor denominado contenedor es un número físico de equipo.

**Alias de búsqueda:** tipo de contenedor; cantidad de contenedores. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E099](#e099), [E100](#e100), [E101](#e101), [E102](#e102), [E085](#e085), [E086](#e086).

<a id="peso-carga"></a>
### Peso y peso bruto de la carga

**Definición.** Medidas que el embarque guarda por separado junto con sus unidades; la carga del viaje también conserva peso y unidad de peso.

**Uso y relaciones.** La existencia de dos campos no acredita por sí sola una fórmula de tara ni una conversión automática.

**Alias de búsqueda:** peso; peso bruto. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E081](#e081), [E082](#e082), [E103](#e103), [E104](#e104).

<a id="volumen-carga"></a>
### Volumen de la carga

**Definición.** Magnitud registrada con unidad de volumen, junto con dimensiones y su unidad en las líneas de carga del viaje.

**Uso y relaciones.** Usar la unidad guardada; el pasaje revisado no demuestra cálculo automático ni equivalencia con peso facturable.

**Alias de búsqueda:** volumen; dimensiones. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E103](#e103), [E104](#e104).

<a id="almacen-cliente"></a>
### Almacén del cliente

**Definición.** Lugar de almacenamiento configurado para un cliente y ofrecido como opción cuando figura activo.

**Uso y relaciones.** Se relaciona con las ubicaciones de la operación; no confundir con una denominación de aduana o con el inventario de un vehículo.

**Alias de búsqueda:** almacén. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E105](#e105), [E106](#e106).

## Costos, documentos y aduanas

<a id="propuesta-costos"></a>
### Propuesta de costos del operador

**Definición.** Detalle de importes por concepto asociado a la participación de un operador en la cotización. Al guardarlo, el sistema marca que el operador completó su cotización y registra la fecha.

**Uso y relaciones.** Distinguir esta propuesta del registro posterior de costos por categoría del embarque.

**Alias de búsqueda:** cotización del operador; oferta de costos. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E107](#e107), [E108](#e108).

<a id="aceptacion-cotizacion"></a>
### Aceptación de la cotización del operador

**Definición.** Acción que marca como aceptada la participación del operador y convierte el registro de cotización en embarque mediante su indicador.

**Uso y relaciones.** Es una transición concreta de la propuesta; no equivale a «Aceptado» en el resumen aduanero.

**Alias de búsqueda:** operador aceptado; aceptación de costos. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E037](#e037), [E038](#e038).

<a id="revision-cotizacion"></a>
### Revisión de cotización

**Definición.** Solicitud de revisión que incrementa un contador y registra la fecha en la participación del operador cuando se utiliza el envío de costos con estado de revisión.

**Uso y relaciones.** La rama de revisión del envío contiene la escritura observada; otra función de nombre parecido termina antes de ejecutar su consulta.

**Alias de búsqueda:** revisión de costos. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E109](#e109), [E110](#e110).

<a id="concepto-costo"></a>
### Concepto de costo

**Definición.** Renglón que describe un cargo y su importe. Existe tanto en el detalle de la propuesta de un operador como en el detalle de costos por categoría del embarque.

**Uso y relaciones.** No tratar ambos detalles como una única tabla ni como un catálogo idéntico; el detalle por categoría permite concepto adicional y marca de automático.

**Ejemplo observado.** El detalle de costos por categoría guarda concepto, importe y una marca que indica si es automático.

**Alias de búsqueda:** cargo; concepto. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E111](#e111), [E112](#e112), [E113](#e113), [E114](#e114).

<a id="categoria-costo"></a>
### Categoría de costo

**Definición.** Agrupación del registro de costos del embarque elegida desde un catálogo de categorías no eliminadas. Una categoría reúne conceptos y su total.

**Uso y relaciones.** Al guardar costos de una categoría se reemplaza lógicamente el registro previo de esa categoría; no asumir que cada guardado añade otro costo acumulable.

**Alias de búsqueda:** categoría de costos. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E115](#e115), [E116](#e116), [E117](#e117), [E118](#e118).

<a id="moneda-costo"></a>
### Moneda del costo

**Definición.** Divisa seleccionable por código y nombre para identificar la moneda del registro de costos.

**Uso y relaciones.** La disponibilidad del catálogo no demuestra conversión, tipo de cambio ni que puedan sumarse importes de monedas distintas.

**Alias de búsqueda:** divisa; moneda. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E119](#e119), [E120](#e120), [E121](#e121), [E122](#e122).

<a id="documento-adjunto"></a>
### Documento adjunto del embarque

**Definición.** Archivo cargado y registrado como documento del embarque, con nombre y número interno de documento dentro de ese embarque.

**Uso y relaciones.** Distinguir el archivo adjunto de los tipos de documento de soporte del viaje y de los documentos previos de una solicitud aduanera.

**Alias de búsqueda:** adjunto; documento del embarque. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E123](#e123), [E124](#e124).

<a id="documento-soporte-viaje"></a>
### Documento de soporte del viaje

**Definición.** Selección de documentos de un catálogo que se vincula a la asignación de viaje, al operador y, cuando existe, al embarque.

**Uso y relaciones.** El guardado observado registra identificadores de documentos; no demuestra por sí solo la carga de un archivo ni su validez.

**Alias de búsqueda:** documentación de soporte. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E125](#e125), [E126](#e126).

<a id="solicitud-aduanera"></a>
### Solicitud de gestión aduanera

**Definición.** Solicitud vinculada al embarque que reúne cliente, proveedor, línea, aduana, régimen, declaración, datos de transporte y referencias de pedido. El código la consulta como caso previo.

**Uso y relaciones.** Puede relacionarse con casos y trámites posteriores; no confundir con el embarque ni con una declaración aduanera presentada.

**Alias de búsqueda:** gestión aduanera; caso previo; solicitud de aduana. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E127](#e127), [E128](#e128), [E129](#e129), [E130](#e130).

<a id="documento-previo"></a>
### Documento previo de la solicitud

**Definición.** Registro documental de una solicitud aduanera con tipo, emisor, formato, número, fecha de recepción, plazo, importe y divisa. El alta puede generar registros según el modo de transporte.

**Uso y relaciones.** Un registro generado no acredita recepción efectiva del documento: algunos campos se inicializan vacíos.

**Ejemplo observado.** Al crear la solicitud se generan registros documentales con número o emisor inicialmente vacíos.

**Alias de búsqueda:** documentación previa. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E131](#e131), [E132](#e132).

<a id="caso-aduanero"></a>
### Caso aduanero

**Definición.** Registro de gestión asociado a una solicitud previa, con carpeta y fechas operativas, que se utiliza para clasificar solicitudes aprobadas, en proceso o de despacho.

**Uso y relaciones.** La relación entre embarque y caso no debe deducirse solo de la orden de compra: las consultas revisadas utilizan criterios diferentes.

**Alias de búsqueda:** caso; expediente aduanero. **Ámbito:** `shared_evidence`. **Confianza:** `inferred`.

**Evidencia:** [E133](#e133), [E134](#e134).

<a id="carpeta"></a>
### Carpeta del caso

**Definición.** Referencia del caso aduanero mostrada en las listas de solicitudes. Su presencia también sirve al resumen del embarque para mostrar el estado «Aceptado».

**Uso y relaciones.** No confundir la referencia de expediente con un directorio de archivos del servidor.

**Alias de búsqueda:** número de carpeta; carpeta aduanera. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E135](#e135), [E136](#e136), [E137](#e137), [E138](#e138).

<a id="tramite"></a>
### Trámite de una solicitud

**Definición.** Unidad de gestión asociada a un caso previo que la consulta de solicitudes del embarque cuenta separadamente.

**Uso y relaciones.** La fuente demuestra la relación y el conteo; no define todas las etapas o responsabilidades de un trámite.

**Alias de búsqueda:** trámite aduanero. **Ámbito:** `shared_evidence`. **Confianza:** `inferred`.

**Evidencia:** [E127](#e127), [E128](#e128).

<a id="regimen-aduanero"></a>
### Régimen de la solicitud

**Definición.** Clasificación seleccionada del catálogo de regímenes y guardada en la gestión aduanera.

**Uso y relaciones.** La presencia del selector no acredita elegibilidad, requisitos legales ni vigencia de cada régimen.

**Alias de búsqueda:** régimen; régimen aduanero. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E139](#e139), [E140](#e140), [E141](#e141), [E142](#e142).

<a id="tipo-declaracion"></a>
### Tipo de declaración

**Definición.** Clasificación documental seleccionada de un catálogo para la gestión aduanera. La consulta revisada excluye un identificador del selector.

**Uso y relaciones.** No inferir el nombre del valor excluido ni una obligación de presentar determinada declaración.

**Alias de búsqueda:** declaración. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E143](#e143), [E144](#e144), [E141](#e141), [E142](#e142).

<a id="aduana"></a>
### Aduana seleccionada

**Definición.** Dependencia o ubicación aduanera elegida del catálogo de aduanas y asociada a la solicitud; se muestra mediante código y nombre.

**Uso y relaciones.** Distinguirla del agente de aduana, que es un actor, y de la aduana de nacionalización registrada para un viaje.

**Alias de búsqueda:** aduana de la solicitud. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E145](#e145), [E146](#e146), [E147](#e147), [E148](#e148).

<a id="ruta-autorizada"></a>
### Ruta autorizada del viaje

**Definición.** Conjunto de datos de ruta que la asignación guarda cuando se informa aduana de nacionalización: ruta asignada, tipo de despacho, fecha límite de cierre de tránsito, descarga en aduana y plazo.

**Uso y relaciones.** La denominación de la estructura no prueba autorización administrativa; el glosario describe los datos capturados.

**Alias de búsqueda:** ruta asignada; datos aduaneros del viaje. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E149](#e149), [E150](#e150).

<a id="cierre-transito"></a>
### Fecha límite de cierre de tránsito

**Definición.** Fecha informada junto con los datos aduaneros de la ruta del viaje y almacenada como límite de cierre de tránsito.

**Uso y relaciones.** Se diferencia de las fechas de salida y arribo. El código revisado no permite derivar un plazo legal ni confirmar el cierre efectivo.

**Alias de búsqueda:** cierre de tránsito; plazo de tránsito. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E149](#e149), [E150](#e150).

<a id="dam"></a>
### DAM en el control de solicitudes

**Definición.** Referencia operativa utilizada por el control de solicitudes enviadas para relacionar vehículos con registros DAM y contar vehículos que carecen de esa asociación.

**Uso y relaciones.** No se ha confirmado en esta revisión la expansión de la sigla ni su equivalencia jurídica por país; el conteo es una regla de la aplicación.

**Alias de búsqueda:** DAM; cantidad sin DAM. **Ámbito:** `shared_evidence`. **Confianza:** `unknown`.

**Evidencia:** [E151](#e151), [E152](#e152).

<a id="dui"></a>
### DUI en la clasificación de despacho

**Definición.** Sigla presente en el campo de fecha de pago usado para separar solicitudes en proceso de solicitudes de despacho.

**Uso y relaciones.** Se observa el criterio de fecha vacía o informada; quedan sin confirmar la expansión de la sigla y su equivalencia con DAM u otras declaraciones.

**Alias de búsqueda:** DUI; pago DUI. **Ámbito:** `shared_evidence`. **Confianza:** `unknown`.

**Evidencia:** [E153](#e153), [E154](#e154), [E155](#e155), [E156](#e156).

## Inventario y seguimiento

<a id="inventario-vehicular"></a>
### Inventario del vehículo

**Definición.** Consulta de la condición y los elementos de un vehículo identificado por chasis, con datos de partida, modelo, lugar y fecha de inventario. La interfaz distingue diferentes momentos de revisión.

**Uso y relaciones.** En este módulo no significa por sí mismo un saldo contable de existencias ni una cantidad disponible para vender.

**Alias de búsqueda:** inventario; inspección de vehículo. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E157](#e157), [E158](#e158), [E159](#e159), [E160](#e160).

<a id="inventario-puerto"></a>
### Inventario en puerto de carga

**Definición.** Sección de revisión de vehículos que la interfaz distingue como inventario realizado en puerto de carga.

**Uso y relaciones.** Es uno de los momentos del inventario, junto con depósito transitorio y post nacionalización; no acredita que todos los vehículos hayan sido revisados.

**Alias de búsqueda:** inventario puerto. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E159](#e159), [E160](#e160).

<a id="inventario-deposito"></a>
### Inventario de depósito transitorio

**Definición.** Sección de inventario separada para la revisión denominada «Depósito transitorio».

**Uso y relaciones.** La etiqueta identifica un contexto de revisión; no define el régimen jurídico del depósito ni su plazo de permanencia.

**Alias de búsqueda:** depósito transitorio. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E159](#e159), [E160](#e160).

<a id="inventario-post-nacionalizacion"></a>
### Inventario post nacionalización

**Definición.** Sección de inventario que la aplicación presenta como revisión posterior a la nacionalización y distingue de puerto y depósito.

**Uso y relaciones.** La visibilidad de la sección no acredita que una operación haya completado un procedimiento aduanero.

**Alias de búsqueda:** post nacionalización; salida de depósito. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E159](#e159), [E160](#e160).

<a id="inventario-nacional-local"></a>
### Inventario de despacho y recepción

**Definición.** Revisiones separadas para despacho y recepción en contextos nacional y local. El contexto local añade una revisión de showroom.

**Uso y relaciones.** Distinguir despacho físico del inventario de la lista aduanera de solicitudes de despacho.

**Alias de búsqueda:** inventario local; inventario nacional; showroom. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E051](#e051), [E052](#e052).

<a id="chasis"></a>
### Chasis como identificador de vehículo

**Definición.** Dato que identifica al vehículo al consultar su inventario y que, en una creación local condicionada, se utiliza como posición del detalle de pedido.

**Uso y relaciones.** Permite relacionar posiciones e inventario; no se ha comprobado una regla general que convierta todo campo de chasis en un VIN validado.

**Alias de búsqueda:** chasis de vehículo. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E157](#e157), [E158](#e158), [E075](#e075), [E076](#e076).

<a id="partida-inventario"></a>
### Partida del inventario

**Definición.** Dato de referencia mostrado junto al chasis y modelo del vehículo en el detalle del inventario.

**Uso y relaciones.** El código de presentación no explica si corresponde a lote, partida documental o clasificación arancelaria. No usar esas acepciones como sinónimos confirmados.

**Ejemplo observado.** El encabezado del inventario muestra partida, chasis y modelo como datos separados.

**Alias de búsqueda:** partida. **Ámbito:** `shared_evidence`. **Confianza:** `unknown`.

**Evidencia:** [E161](#e161), [E162](#e162).

<a id="parte-recepcion"></a>
### Parte de recepción

**Definición.** Evidencia de recepción que la interfaz del inventario consulta por chasis y presenta mediante imágenes.

**Uso y relaciones.** Documenta la consulta de imágenes; no se han validado el contenido obligatorio del parte, firmas o efectos de aceptación. En Perú el componente homónimo consulta fotografías 360°; no se ha demostrado equivalencia funcional con este parte.

**Alias de búsqueda:** parte recepción. **Ámbito:** `master`. **Confianza:** `inferred`.

**Evidencia:** [E163](#e163).

<a id="desperfecto"></a>
### Desperfecto del vehículo

**Definición.** Daño o defecto registrado en el inventario con atributo, tipo, indicación de levedad, ubicación, comentario y posible evidencia fotográfica.

**Uso y relaciones.** La consulta presenta autor y fecha de inventario; no determina responsabilidad, costo de reparación ni indemnización.

**Alias de búsqueda:** daño; defecto. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E164](#e164), [E165](#e165).

<a id="contaminacion"></a>
### Contaminación en la revisión del vehículo

**Definición.** Evaluación del inventario que registra nombre de evaluación, resultado, comentario y fotografías cuando existen.

**Uso y relaciones.** Es una sección de inspección; el pasaje no identifica sustancias, umbrales técnicos ni criterios regulatorios.

**Alias de búsqueda:** evaluación de contaminación. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E166](#e166), [E167](#e167).

<a id="accesorio"></a>
### Accesorio inventariado

**Definición.** Elemento del vehículo mostrado en el inventario con nombre, cantidad, observaciones y fotografía cuando existe.

**Uso y relaciones.** Se distingue de los desperfectos del vehículo y de la mercancía general del embarque.

**Alias de búsqueda:** accesorios. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E168](#e168), [E169](#e169).

<a id="estado-catalogo-embarque"></a>
### Estado del catálogo de embarques

**Definición.** Valor del catálogo de estados usado para mostrar una etiqueta de estado del embarque, con configuración de color o estilo.

**Uso y relaciones.** No es intercambiable con estado del viaje, anotación EDP ni resumen calculado a partir de fechas.

**Alias de búsqueda:** estado de embarque; estado. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E170](#e170), [E171](#e171).

<a id="edp"></a>
### Estado de pedidos (EDP)

**Definición.** Anotación de seguimiento asociada al embarque que registra etapa seleccionada, fecha, texto, valor y autor. El catálogo de etapas puede variar por cliente y tipo de proveedor.

**Uso y relaciones.** Es un historial de anotaciones; no equivale a un único estado universal ni requiere necesariamente un pedido operativo identificado.

**Ejemplo observado.** El historial distingue anotaciones de cliente, usuario interno y operador por el tipo de autor.

**Alias de búsqueda:** EDP; estado de pedido; seguimiento de pedidos. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E172](#e172), [E173](#e173).

<a id="estado-viaje"></a>
### Estado de la asignación de viaje

**Definición.** Dato propio del viaje que se guarda al crear su información. La rutina revisada utiliza un valor nulo o un código según el indicador de asignación.

**Uso y relaciones.** No se ha confirmado el nombre de todos sus códigos; no traducir el código de creación a un estado de embarque.

**Alias de búsqueda:** estado del viaje. **Ámbito:** `shared_evidence`. **Confianza:** `inferred`.

**Evidencia:** [E049](#e049), [E050](#e050).

<a id="estado-resumen"></a>
### Estado resumen calculado del embarque

**Definición.** Etiqueta calculada a partir de fechas de solicitud, envío, oficialización, carpeta y finalización. La función revisada elige una sola fila y aplica prioridades.

**Uso y relaciones.** Es una vista resumida; no acredita por sí sola que todos los casos o viajes estén en la misma etapa.

**Ejemplo observado.** Si hay fecha de finalización, la función devuelve «Finalizado» aunque existan también otras fechas.

**Alias de búsqueda:** resumen de estado. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E137](#e137), [E138](#e138).

<a id="pendiente-resumen"></a>
### Pendiente en el resumen del embarque

**Definición.** Etiqueta inicial del resumen cuando la fila consultada no activa condiciones de finalización, proceso, aceptación o envío.

**Uso y relaciones.** No significa que la aplicación haya comprobado todas las tareas pendientes de la operación.

**Alias de búsqueda:** pendiente. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E137](#e137), [E138](#e138).

<a id="enviado-resumen"></a>
### Enviado en el resumen del embarque

**Definición.** Etiqueta del resumen cuando hay fecha derivada de finalización o complemento de solicitud, o fecha de envío, sin cumplirse una condición de mayor prioridad.

**Uso y relaciones.** No equivale al envío de cotización al operador ni al filtro específico de solicitudes enviadas.

**Alias de búsqueda:** enviado. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E137](#e137), [E138](#e138).

<a id="aceptado-resumen"></a>
### Aceptado en el resumen del embarque

**Definición.** Etiqueta del resumen cuando existe carpeta y no prevalecen fecha de oficialización o finalización.

**Uso y relaciones.** Distinguir de la aceptación de la propuesta del operador, que modifica otros datos.

**Alias de búsqueda:** aceptado. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E137](#e137), [E138](#e138).

<a id="en-proceso-resumen"></a>
### En proceso en el resumen del embarque

**Definición.** Etiqueta del resumen cuando existe fecha de oficialización y no existe fecha de finalización.

**Uso y relaciones.** El filtro de solicitudes en proceso utiliza criterios adicionales; no asumir equivalencia con este resumen.

**Alias de búsqueda:** en proceso. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E137](#e137), [E138](#e138).

<a id="finalizado-resumen"></a>
### Finalizado en el resumen del embarque

**Definición.** Etiqueta de mayor prioridad cuando el embarque tiene fecha de finalización informada.

**Uso y relaciones.** Algunas pantallas usan esa fecha para ocultar acciones de alta. La etiqueta no demuestra cierre contable o legal.

**Alias de búsqueda:** finalizado; finalización. **Ámbito:** `shared_evidence`. **Confianza:** `observed`.

**Evidencia:** [E137](#e137), [E138](#e138), [E174](#e174), [E175](#e175).

<a id="estados-solicitud-aduanera"></a>
### Estados de las listas de solicitudes aduaneras

**Definición.** Clasificaciones calculadas por consultas diferentes: pendientes sin fecha de fin; enviadas con fecha de fin y sin aprobación; aprobadas según fecha de aprobación, tipo de usuario y caso no anulado; en proceso con aprobación y sin fecha de pago DUI; despacho con fecha de pago DUI.

**Uso y relaciones.** Son filtros de listas, no un catálogo único de transiciones. Algunas listas enlazan por cliente y referencia de pedido, por lo que no deben interpretarse como un historial exacto del embarque.

**Alias de búsqueda:** solicitud pendiente; solicitud enviada; solicitud aprobada; solicitud en proceso; solicitud de despacho. **Ámbito:** `shared_evidence`. **Confianza:** `inferred`.

**Evidencia:** [E176](#e176), [E177](#e177), [E178](#e178), [E179](#e179), [E180](#e180), [E181](#e181), [E182](#e182), [E183](#e183), [E184](#e184), [E185](#e185).

## Extensiones observadas en Perú

<a id="concesionario-cliente"></a>
### Concesionario asociado al cliente

**Definición.** Actor disponible en el selector que consulta los concesionarios vinculados al cliente y no eliminados.

**Uso y relaciones.** La consulta específica se observó en Perú; la revisión no confirma que el concesionario sea siempre destinatario, comprador o propietario de la mercancía.

**Alias de búsqueda:** concesionario. **Ámbito:** `peru`. **Confianza:** `observed`.

**Evidencia:** [E186](#e186).

<a id="viaje-desde-vin"></a>
### Creación de viaje desde VIN seleccionados

**Definición.** Flujo del detalle de ítems nacionales que crea una asignación a partir de vehículos seleccionados. Exige embarque nacional, origen, unidad, conductor y fecha y hora programadas, y rechaza VIN duplicados o ya asociados a viaje.

**Uso y relaciones.** Es una extensión observada en Perú. Un VIN debe pertenecer al embarque; la unidad y el origen deben corresponder al operador, y el conductor a la unidad o empresa elegida.

**Ejemplo observado.** Si alguno de los VIN seleccionados ya tiene viaje asociado, la validación rechaza la solicitud.

**Alias de búsqueda:** crear viaje desde ítems; selección de VIN; VIN. **Ámbito:** `peru`. **Confianza:** `observed`.

**Evidencia:** [E187](#e187), [E188](#e188), [E189](#e189).

<a id="registro-kilometraje-imagen"></a>
### Registro de kilometraje con imagen

**Definición.** Consulta específica del inventario que muestra kilometraje, observaciones e imagen y solicita el registro por chasis, embarque y tipo de inventario.

**Uso y relaciones.** La variante documentada corresponde al componente específico de Perú. Master ya muestra kilometraje dentro de accesorios, por lo que el concepto general de kilometraje no es exclusivo de Perú.

**Alias de búsqueda:** kilometraje de la unidad; odómetro. **Ámbito:** `peru`. **Confianza:** `observed`.

**Evidencia:** [E190](#e190), [E191](#e191).

<a id="fotografias-360"></a>
### Fotografías 360° del inventario

**Definición.** Conjunto de imágenes de revisión del vehículo que el componente de inventario de Perú consulta por chasis y tipo de inventario, presenta con comentario general y permite descargar en conjunto.

**Uso y relaciones.** El archivo conserva un nombre de parte de recepción, pero su contenido funcional se refiere a fotografías 360°; no tratar el nombre de archivo como prueba de equivalencia documental.

**Alias de búsqueda:** fotos 360; imágenes 360. **Ámbito:** `peru`. **Confianza:** `observed`.

**Evidencia:** [E192](#e192), [E193](#e193).

## Índice de evidencia de fuente

Cada referencia incluye rama, commit, ruta y rango de líneas. Las consultas SQL citadas prueban usos en el código; no prueban existencia de tablas, columnas, procedimientos o valores en una base de datos desplegada.

- <a id="e001"></a>**E001** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/CotizacionClass.php` · **L252-L262**.
- <a id="e002"></a>**E002** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/CotizacionClass.php` · **L252-L262**.
- <a id="e003"></a>**E003** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/componentes/embarques_datos.php` · **L1-L9**.
- <a id="e004"></a>**E004** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/componentes/embarques_datos.php` · **L1-L9**.
- <a id="e005"></a>**E005** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/parametros/clientes/ClienteProveedorClass.php` · **L12-L28**.
- <a id="e006"></a>**E006** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/parametros/clientes/ClienteProveedorClass.php` · **L12-L28**.
- <a id="e007"></a>**E007** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/CotizacionClass.php` · **L655-L674**.
- <a id="e008"></a>**E008** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/CotizacionClass.php` · **L663-L682**.
- <a id="e009"></a>**E009** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/componentes/estado-pedidos/controllers/EstadoPedidosClass.php` · **L172-L193**.
- <a id="e010"></a>**E010** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/componentes/estado-pedidos/controllers/EstadoPedidosClass.php` · **L172-L193**.
- <a id="e011"></a>**E011** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/EmbarqueClass.php` · **L39-L60**.
- <a id="e012"></a>**E012** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/EmbarqueClass.php` · **L83-L104**.
- <a id="e013"></a>**E013** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/CotizacionClass.php` · **L549-L559**.
- <a id="e014"></a>**E014** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/CotizacionClass.php` · **L549-L558**.
- <a id="e015"></a>**E015** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/tracking/TrackingNewClass.php` · **L1132-L1144**.
- <a id="e016"></a>**E016** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/tracking/TrackingNewClass.php` · **L1132-L1144**.
- <a id="e017"></a>**E017** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/tracking/TrackingNewClass.php` · **L192-L199**.
- <a id="e018"></a>**E018** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/tracking/TrackingNewClass.php` · **L192-L199**.
- <a id="e019"></a>**E019** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/tracking/TrackingNewClass.php` · **L1147-L1163**.
- <a id="e020"></a>**E020** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/tracking/TrackingNewClass.php` · **L1147-L1163**.
- <a id="e021"></a>**E021** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/tracking/TrackingNewClass.php` · **L212-L220**.
- <a id="e022"></a>**E022** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/tracking/TrackingNewClass.php` · **L212-L220**.
- <a id="e023"></a>**E023** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/componentes/estado-pedidos/controllers/EstadoPedidosClass.php` · **L148-L186**.
- <a id="e024"></a>**E024** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/componentes/estado-pedidos/controllers/EstadoPedidosClass.php` · **L148-L186**.
- <a id="e025"></a>**E025** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/CostosClass.php` · **L314-L338**.
- <a id="e026"></a>**E026** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/CostosClass.php` · **L316-L340**.
- <a id="e027"></a>**E027** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/componentes/estado-pedidos/controllers/EstadoPedidosClass.php` · **L148-L178**.
- <a id="e028"></a>**E028** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/componentes/estado-pedidos/controllers/EstadoPedidosClass.php` · **L148-L178**.
- <a id="e029"></a>**E029** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/EmbarqueClass.php` · **L69-L86**.
- <a id="e030"></a>**E030** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/EmbarqueClass.php` · **L113-L130**.
- <a id="e031"></a>**E031** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/EmbarqueClass.php` · **L650-L671**.
- <a id="e032"></a>**E032** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/EmbarqueClass.php` · **L744-L765**.
- <a id="e033"></a>**E033** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/SolicitudesClass.php` · **L653-L661**.
- <a id="e034"></a>**E034** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/SolicitudesClass.php` · **L559-L567**.
- <a id="e035"></a>**E035** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/CotizacionClass.php` · **L86-L101**.
- <a id="e036"></a>**E036** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/CotizacionClass.php` · **L86-L101**.
- <a id="e037"></a>**E037** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/CotizacionClass.php` · **L998-L1005**.
- <a id="e038"></a>**E038** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/CotizacionClass.php` · **L1007-L1014**.
- <a id="e039"></a>**E039** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/EmbarqueClass.php` · **L117-L126**.
- <a id="e040"></a>**E040** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/EmbarqueClass.php` · **L161-L170**.
- <a id="e041"></a>**E041** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/EmbarqueClass.php` · **L685-L690**.
- <a id="e042"></a>**E042** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/EmbarqueClass.php` · **L779-L784**.
- <a id="e043"></a>**E043** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/ViajesClass.php` · **L18-L35**.
- <a id="e044"></a>**E044** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/ViajesClass.php` · **L18-L35**.
- <a id="e045"></a>**E045** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/tracking/TrackingNewClass.php` · **L181-L220**.
- <a id="e046"></a>**E046** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/tracking/TrackingNewClass.php` · **L181-L220**.
- <a id="e047"></a>**E047** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/tracking/TrackingNewClass.php` · **L293-L305**.
- <a id="e048"></a>**E048** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/tracking/TrackingNewClass.php` · **L293-L305**.
- <a id="e049"></a>**E049** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/tracking/TrackingNewClass.php` · **L1099-L1107**.
- <a id="e050"></a>**E050** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/tracking/TrackingNewClass.php` · **L1099-L1107**.
- <a id="e051"></a>**E051** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/frames/inventario_local.php` · **L33-L40**.
- <a id="e052"></a>**E052** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/frames/inventario_local.php` · **L119-L126**.
- <a id="e053"></a>**E053** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/embarquecrear.php` · **L8-L12**.
- <a id="e054"></a>**E054** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/embarquecrear.php` · **L8-L12**.
- <a id="e055"></a>**E055** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/tracking/TrackingNewClass.php` · **L323-L338**.
- <a id="e056"></a>**E056** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/tracking/TrackingNewClass.php` · **L323-L338**.
- <a id="e057"></a>**E057** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/componentes/embarques_datos.php` · **L80-L87**.
- <a id="e058"></a>**E058** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/componentes/embarques_datos.php` · **L80-L87**.
- <a id="e059"></a>**E059** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/EmbarqueClass.php` · **L402-L419**.
- <a id="e060"></a>**E060** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/EmbarqueClass.php` · **L496-L513**.
- <a id="e061"></a>**E061** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/CotizacionClass.php` · **L739-L755**.
- <a id="e062"></a>**E062** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/CotizacionClass.php` · **L747-L763**.
- <a id="e063"></a>**E063** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/EmbarqueClass.php` · **L393-L421**.
- <a id="e064"></a>**E064** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/EmbarqueClass.php` · **L487-L515**.
- <a id="e065"></a>**E065** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/tracking/TrackingNewClass.php` · **L204-L210**.
- <a id="e066"></a>**E066** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/tracking/TrackingNewClass.php` · **L204-L210**.
- <a id="e067"></a>**E067** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/tracking/TrackingNewClass.php` · **L1315-L1333**.
- <a id="e068"></a>**E068** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/tracking/TrackingNewClass.php` · **L1315-L1333**.
- <a id="e069"></a>**E069** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/componentes/embarques_datos.php` · **L71-L78**.
- <a id="e070"></a>**E070** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/componentes/embarques_datos.php` · **L71-L78**.
- <a id="e071"></a>**E071** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/CotizacionClass.php` · **L680-L689**.
- <a id="e072"></a>**E072** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/CotizacionClass.php` · **L688-L697**.
- <a id="e073"></a>**E073** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/CotizacionClass.php` · **L1288-L1304**.
- <a id="e074"></a>**E074** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/CotizacionClass.php` · **L1343-L1359**.
- <a id="e075"></a>**E075** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/CotizacionClass.php` · **L1293-L1301**.
- <a id="e076"></a>**E076** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/CotizacionClass.php` · **L1348-L1356**.
- <a id="e077"></a>**E077** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/frames/items.php` · **L54-L70**.
- <a id="e078"></a>**E078** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/frames/items.php` · **L110-L125**.
- <a id="e079"></a>**E079** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/CotizacionClass.php` · **L570-L580**.
- <a id="e080"></a>**E080** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/CotizacionClass.php` · **L578-L588**.
- <a id="e081"></a>**E081** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/CotizacionClass.php` · **L699-L714**.
- <a id="e082"></a>**E082** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/CotizacionClass.php` · **L707-L722**.
- <a id="e083"></a>**E083** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/componentes/embarques_tramos.php` · **L124-L139**.
- <a id="e084"></a>**E084** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/componentes/embarques_tramos.php` · **L124-L139**.
- <a id="e085"></a>**E085** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/tracking/TrackingNewClass.php` · **L1110-L1129**.
- <a id="e086"></a>**E086** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/tracking/TrackingNewClass.php` · **L1110-L1129**.
- <a id="e087"></a>**E087** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/CotizacionClass.php` · **L216-L237**.
- <a id="e088"></a>**E088** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/CotizacionClass.php` · **L216-L237**.
- <a id="e089"></a>**E089** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/CotizacionClass.php` · **L228-L249**.
- <a id="e090"></a>**E090** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/CotizacionClass.php` · **L228-L249**.
- <a id="e091"></a>**E091** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/CotizacionClass.php` · **L240-L249**.
- <a id="e092"></a>**E092** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/CotizacionClass.php` · **L240-L249**.
- <a id="e093"></a>**E093** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/componentes/embarques_datos.php` · **L89-L98**.
- <a id="e094"></a>**E094** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/componentes/embarques_datos.php` · **L89-L98**.
- <a id="e095"></a>**E095** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/CostosClass.php` · **L250-L251**.
- <a id="e096"></a>**E096** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/CostosClass.php` · **L252-L253**.
- <a id="e097"></a>**E097** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/CotizacionClass.php` · **L699-L732**.
- <a id="e098"></a>**E098** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/CotizacionClass.php` · **L707-L740**.
- <a id="e099"></a>**E099** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/CotizacionClass.php` · **L596-L619**.
- <a id="e100"></a>**E100** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/CotizacionClass.php` · **L604-L627**.
- <a id="e101"></a>**E101** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/CotizacionClass.php` · **L723-L733**.
- <a id="e102"></a>**E102** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/CotizacionClass.php` · **L731-L741**.
- <a id="e103"></a>**E103** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/tracking/TrackingNewClass.php` · **L1166-L1184**.
- <a id="e104"></a>**E104** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/tracking/TrackingNewClass.php` · **L1166-L1184**.
- <a id="e105"></a>**E105** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/CotizacionClass.php` · **L537-L546**.
- <a id="e106"></a>**E106** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/CotizacionClass.php` · **L537-L546**.
- <a id="e107"></a>**E107** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/CostosClass.php` · **L269-L285**.
- <a id="e108"></a>**E108** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/CostosClass.php` · **L271-L287**.
- <a id="e109"></a>**E109** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/CotizacionClass.php` · **L987-L1013**.
- <a id="e110"></a>**E110** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/CotizacionClass.php` · **L996-L1022**.
- <a id="e111"></a>**E111** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/CostosClass.php` · **L269-L281**.
- <a id="e112"></a>**E112** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/CostosClass.php` · **L271-L283**.
- <a id="e113"></a>**E113** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/CostosClass.php` · **L382-L390**.
- <a id="e114"></a>**E114** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/CostosClass.php` · **L384-L392**.
- <a id="e115"></a>**E115** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/CostosClass.php` · **L340-L367**.
- <a id="e116"></a>**E116** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/CostosClass.php` · **L342-L369**.
- <a id="e117"></a>**E117** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/CostosClass.php` · **L443-L449**.
- <a id="e118"></a>**E118** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/CostosClass.php` · **L445-L451**.
- <a id="e119"></a>**E119** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/CostosClass.php` · **L453-L464**.
- <a id="e120"></a>**E120** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/CostosClass.php` · **L455-L466**.
- <a id="e121"></a>**E121** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/CostosClass.php` · **L576-L583**.
- <a id="e122"></a>**E122** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/CostosClass.php` · **L578-L585**.
- <a id="e123"></a>**E123** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/EmbarqueClass.php` · **L310-L332**.
- <a id="e124"></a>**E124** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/EmbarqueClass.php` · **L404-L426**.
- <a id="e125"></a>**E125** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/tracking/TrackingNewClass.php` · **L1347-L1363**.
- <a id="e126"></a>**E126** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/tracking/TrackingNewClass.php` · **L1347-L1363**.
- <a id="e127"></a>**E127** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/EmbarqueClass.php` · **L684-L690**.
- <a id="e128"></a>**E128** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/EmbarqueClass.php` · **L778-L784**.
- <a id="e129"></a>**E129** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/SolicitudesClass.php` · **L683-L719**.
- <a id="e130"></a>**E130** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/SolicitudesClass.php` · **L589-L625**.
- <a id="e131"></a>**E131** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/SolicitudesClass.php` · **L743-L745**.
- <a id="e132"></a>**E132** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/SolicitudesClass.php` · **L649-L651**.
- <a id="e133"></a>**E133** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/SolicitudesClass.php` · **L340-L367**.
- <a id="e134"></a>**E134** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/SolicitudesClass.php` · **L246-L273**.
- <a id="e135"></a>**E135** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/SolicitudesClass.php` · **L340-L354**.
- <a id="e136"></a>**E136** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/SolicitudesClass.php` · **L246-L260**.
- <a id="e137"></a>**E137** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/componentes/estado-pedidos/controllers/EstadoPedidosClass.php` · **L117-L138**.
- <a id="e138"></a>**E138** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/componentes/estado-pedidos/controllers/EstadoPedidosClass.php` · **L117-L138**.
- <a id="e139"></a>**E139** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/SolicitudesClass.php` · **L533-L535**.
- <a id="e140"></a>**E140** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/SolicitudesClass.php` · **L439-L441**.
- <a id="e141"></a>**E141** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/SolicitudesClass.php` · **L683-L694**.
- <a id="e142"></a>**E142** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/SolicitudesClass.php` · **L589-L600**.
- <a id="e143"></a>**E143** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/SolicitudesClass.php` · **L545-L547**.
- <a id="e144"></a>**E144** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/SolicitudesClass.php` · **L451-L453**.
- <a id="e145"></a>**E145** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/SolicitudesClass.php` · **L557-L559**.
- <a id="e146"></a>**E146** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/SolicitudesClass.php` · **L463-L465**.
- <a id="e147"></a>**E147** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/SolicitudesClass.php` · **L56-L76**.
- <a id="e148"></a>**E148** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/SolicitudesClass.php` · **L56-L76**.
- <a id="e149"></a>**E149** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/tracking/TrackingNewClass.php` · **L1336-L1344**.
- <a id="e150"></a>**E150** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/tracking/TrackingNewClass.php` · **L1336-L1344**.
- <a id="e151"></a>**E151** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/SolicitudesClass.php` · **L160-L176**.
- <a id="e152"></a>**E152** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/SolicitudesClass.php` · **L125-L141**.
- <a id="e153"></a>**E153** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/SolicitudesClass.php` · **L402-L408**.
- <a id="e154"></a>**E154** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/SolicitudesClass.php` · **L308-L314**.
- <a id="e155"></a>**E155** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/SolicitudesClass.php` · **L442-L447**.
- <a id="e156"></a>**E156** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/SolicitudesClass.php` · **L348-L353**.
- <a id="e157"></a>**E157** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/componentes/inventario/index.js` · **L11-L22**.
- <a id="e158"></a>**E158** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/componentes/inventario/index.js` · **L11-L22**.
- <a id="e159"></a>**E159** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/frames/inventario.php` · **L30-L34**.
- <a id="e160"></a>**E160** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/frames/inventario.php` · **L30-L34**.
- <a id="e161"></a>**E161** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/componentes/inventario/index.js` · **L11-L16**.
- <a id="e162"></a>**E162** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/componentes/inventario/index.js` · **L11-L16**.
- <a id="e163"></a>**E163** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/componentes/inventario/parte-recepcion.js` · **L27-L48**.
- <a id="e164"></a>**E164** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/componentes/inventario/desperfectos.js` · **L4-L31**.
- <a id="e165"></a>**E165** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/componentes/inventario/desperfectos.js` · **L4-L40**.
- <a id="e166"></a>**E166** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/componentes/inventario/contaminacion.js` · **L10-L26**.
- <a id="e167"></a>**E167** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/componentes/inventario/contaminacion.js` · **L10-L26**.
- <a id="e168"></a>**E168** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/componentes/inventario/accesorios.js` · **L10-L25**.
- <a id="e169"></a>**E169** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/componentes/inventario/accesorios.js` · **L10-L25**.
- <a id="e170"></a>**E170** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/EmbarqueClass.php` · **L20-L29**.
- <a id="e171"></a>**E171** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/EmbarqueClass.php` · **L64-L73**.
- <a id="e172"></a>**E172** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/componentes/estado-pedidos/controllers/EstadoPedidosClass.php` · **L14-L70**.
- <a id="e173"></a>**E173** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/componentes/estado-pedidos/controllers/EstadoPedidosClass.php` · **L14-L70**.
- <a id="e174"></a>**E174** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/frames/estado-pedidos.php` · **L20-L27**.
- <a id="e175"></a>**E175** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/frames/estado-pedidos.php` · **L20-L27**.
- <a id="e176"></a>**E176** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/SolicitudesClass.php` · **L74-L79**.
- <a id="e177"></a>**E177** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/SolicitudesClass.php` · **L74-L79**.
- <a id="e178"></a>**E178** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/SolicitudesClass.php` · **L203-L209**.
- <a id="e179"></a>**E179** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/SolicitudesClass.php` · **L168-L174**.
- <a id="e180"></a>**E180** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/SolicitudesClass.php` · **L353-L367**.
- <a id="e181"></a>**E181** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/SolicitudesClass.php` · **L259-L273**.
- <a id="e182"></a>**E182** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/SolicitudesClass.php` · **L394-L409**.
- <a id="e183"></a>**E183** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/SolicitudesClass.php` · **L300-L315**.
- <a id="e184"></a>**E184** — `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707` · `index_archivos/embarques/SolicitudesClass.php` · **L435-L448**.
- <a id="e185"></a>**E185** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/SolicitudesClass.php` · **L341-L354**.
- <a id="e186"></a>**E186** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/CotizacionClass.php` · **L560-L575**.
- <a id="e187"></a>**E187** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/frames/items.php` · **L61-L76**.
- <a id="e188"></a>**E188** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/ajax/FlujoCrearViajeDesdeItems.php` · **L19-L54**.
- <a id="e189"></a>**E189** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/ajax/FlujoCrearViajeDesdeItems.php` · **L68-L106**.
- <a id="e190"></a>**E190** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/componentes/inventario-local/kilometraje.js` · **L1-L20**.
- <a id="e191"></a>**E191** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/componentes/inventario-local/kilometraje.js` · **L46-L62**.
- <a id="e192"></a>**E192** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/componentes/inventario/parte-recepcion.js` · **L1-L31**.
- <a id="e193"></a>**E193** — `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` · `index_archivos/embarques/componentes/inventario/parte-recepcion.js` · **L54-L77**.

## Candidatos históricos y límites

Los **891 candidatos originales** permanecen separados en [el CSV histórico](../../source-audits/brownfield/reports/business_glossary/BUSINESS_GLOSSARY.csv), [su glosario original](../../source-audits/brownfield/reports/business_glossary/BUSINESS_GLOSSARY.md) y [su registro de revisión](../../source-audits/brownfield/reports/business_glossary/BUSINESS_GLOSSARY_REVIEW.md). Conservan `INFERRED_DRAFT_REVIEW_REQUIRED`: **891 sin validación individual**, incluidos 3 grupos genéricos, 865 candidatos de entidad y 23 candidatos de campo. No son las entradas de este diccionario ni se consideran definiciones aprobadas.

No corresponde calcular «891 menos 81»: no existe una correspondencia uno a uno entre identificadores históricos y conceptos de negocio. La [disposición individual de los 891 candidatos](historical-candidates-disposition.csv) identifica sus referencias candidatas en master sin dar por verificadas estructuras físicas de Perú ni sus significados de negocio.

La evidencia es estática. No se ejecutaron flujos ni se comprobó la base de datos física. Tampoco se verificaron externamente expansiones de siglas, reglas aduaneras, condiciones contractuales o plazos normativos. Véase el [registro de revisión](review-register.md) para dudas concretas y comprobaciones realizadas.

# Registro de revisión del glosario de negocio

Fecha: **2026-11-18**. Alcance: revisión estática directa de código y pantallas de los dos commits fijados. Este registro acompaña al glosario en Markdown y JSON.

## Resultado y significado de «revisado»

| Medida | Resultado |
| --- | ---: |
| Conceptos de negocio con definición, uso y evidencia | 81 |
| `shared_evidence` | 76 |
| `master` | 1 |
| `peru` | 4 |
| `bolivia` | 0 |
| `observed` | 69 |
| `inferred` | 9 |
| `unknown` | 3 |
| Aprobaciones de responsable de negocio registradas | 0 |
| Candidatos históricos conservados | 891 |
| Candidatos históricos sin validación individual en esta revisión | 891 |

Se revisaron conceptos reales de actores, contratación del transporte, embarques, viajes, trayectos, pedidos, mercancía, costos, documentación, solicitudes aduaneras, inventario y seguimiento. Los alias sirven para buscar dentro de un contexto y pueden ser homónimos. No se aprobaron equivalencias de claves ni se tradujeron nombres de tabla en definiciones.

`observed` acredita la descripción del código citado; `inferred` indica interpretación funcional pendiente; `unknown` conserva una acepción o sigla sin resolver aunque su uso local esté observado. Ninguna marca acredita validación de negocio, funcionamiento desplegado o cumplimiento normativo.

## Fuentes y método

- `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707`.
- `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62`.
- Lectura mediante objetos Git del repositorio `C:/repos/proveedores-github-review-20261118`, sin alterar ramas ni fuente.
- Se inspeccionaron directamente las clases de cotización, embarque, viajes, costos, solicitudes, clientes del operador y asignación de tracking; también formularios de datos, tramos, ítems y componentes de inventario y estados.
- La comparación entre ramas incluyó los pasajes citados, sus desplazamientos de líneas y diferencias de contenido. La coincidencia del nombre de archivo no se tomó como equivalencia funcional.
- No se exportaron código privado, SQL literal, documentos adjuntos, datos de personas, valores de configuración o secretos. Las referencias permiten a un lector autorizado consultar la fuente.
- El ámbito `bolivia` queda reservado. La configuración de zona horaria La Paz comunicada por la coordinación no basta para atribuir todos los comportamientos master a Bolivia.
- La ausencia de DDL de aplicación en la auditoría master impide validar un esquema físico. Aquí las referencias a estructuras son usos observados en consultas, no inventarios de tablas existentes.

El catálogo JSON contiene un **esquema completo Draft 2020-12 en `schema`** y un índice en `index`: identificador → JSON Pointer a la entrada, término normalizado → identificadores, alias → identificadores, ámbito, confianza, categoría y orden alfabético. El mismo diccionario se presenta en Markdown con índice de conceptos y catálogo de referencias. La normalización de búsqueda se declara en `index.normalization`.

## Homónimos, diferencias y pendientes de negocio

Las decisiones de separación ya están incorporadas. «Pendiente» describe la incertidumbre residual, no una definición inventada ni una solicitud de permiso para terminar el documento.

| ID | Conceptos | Decisión aplicada y pendiente |
| --- | --- | --- |
| G01 | Proveedor / operador / empresa / conductor | Se separan suministrador de mercancía, operador logístico, empresa del viaje y persona conductora. Los nombres «proveedor» y «transportista» no garantizan identidad entre estructuras. |
| G02 | Identificador de operador | Diferencia comprobada: el selector de master devuelve como `id` la relación cliente–transportista; Perú devuelve como `id` el transportista y conserva también el identificador de relación. No usar un alias de consulta como clave canónica común. |
| G03 | Cliente / solicitante | Se separa catálogo general de clientes del directorio propio del operador. El solicitante del selector del embarque es una organización; el nombre del solicitante de una solicitud puede identificar a una persona. Falta confirmación de equivalencias de identidad entre directorios. |
| G04 | Pedido / orden de compra | La interfaz guarda «Pedido» en `ordencompra` y «Orden de Compra» en `ordencompraini`. Se separan estas referencias del pedido operativo con posiciones. Falta validar formatos, unicidad y reglas de conciliación con negocio. |
| G05 | Tipo de viaje / alcance / modalidad | Se separa ámbito internacional/nacional/local de sentido solo ida/ida y vuelta/solo vuelta, y de modalidad de transporte. No hay equivalencia universal entre identificadores de catálogos diferentes. |
| G06 | Estado | Se separan estado del catálogo de embarques, estado del viaje, historial EDP, resumen calculado y filtros de solicitudes. Los valores de catálogos no leídos no reciben nombres inventados. |
| G07 | DAM | `unknown`: se observa asociación de vehículos a DAM y conteo de ausencias. Pendientes expansión de sigla y equivalencia documental por país. |
| G08 | DUI | `unknown`: se observa una fecha de pago utilizada en filtros. Pendientes expansión de sigla, semántica exacta de la fecha y relación con DAM; no se afirma equivalencia. |
| G09 | Partida | `unknown`: el inventario muestra partida junto a chasis y modelo. No se confirma acepción arancelaria, lote o referencia documental. |
| G10 | Parte de recepción / fotos 360° | El pasaje master consulta imágenes de parte de recepción. El archivo homónimo en Perú consulta fotos 360° con comentario y descarga. Se crean dos entradas con ámbitos distintos; no se presume equivalencia documental. |
| G11 | Chasis / VIN | El caso local usa chasis como posición. El flujo Perú valida selección de VIN del embarque y evita duplicidades y asociaciones previas. No se prueba una validación universal de formato VIN en todas las entradas del sistema. |
| G12 | Creación automática de pedidos | La rutina se invoca bajo condición de alcance local y cliente específico y utiliza valores prefijados. Se describe como caso particular; no se publica el nombre del cliente ni se generaliza la automatización. |
| G13 | EDP automático | La asignación puede registrar una anotación automática con un identificador de etapa fijo. Se acredita la escritura, pero no se asigna un nombre a ese código sin leer el catálogo operativo. |
| G14 | Resumen y solicitudes | El resumen usa una fila y prioridades de fechas; las listas aduaneras usan filtros diferentes y algunas enlazan por cliente y referencia de pedido. No representan necesariamente el estado agregado de todos los casos. |
| G15 | Costos y moneda | Se separa propuesta del operador del registro de costos por categoría. La sustitución lógica de una categoría no debe interpretarse como importe acumulable. Faltan reglas contables, impuestos y conversión de divisas; no se inventan. |
| G16 | Actores especializados | Gestor, agente aduanero, agente de seguro, agente de proveedor y declarante se distinguen por relaciones y selecciones observadas. Sus responsabilidades contractuales o legales requieren confirmación externa al código. |
| G17 | Documento | Se separan archivo adjunto, selección de soporte de viaje y registro documental previo. La existencia del registro no prueba archivo recibido, autorización, firma ni vigencia. |
| G18 | Inventario / nacionalización / despacho | Se describen secciones de inspección. Una etiqueta post nacionalización no prueba que el trámite esté concluido; despacho físico e inventario no equivalen al filtro aduanero de despacho. |
| G19 | Concesionario y kilometraje Perú | Se documenta la selección de concesionarios y el componente específico de kilometraje con imagen. El concepto general de kilometraje ya aparece en accesorios de master; no se afirma que sea exclusivo de Perú. |

Referencias clave para resolver estas dudas (el índice completo está en el glosario):

- **G02:** `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/embarques/EmbarqueClass.php:L39-L60`; `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/embarques/EmbarqueClass.php:L83-L104`; `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/embarques/CotizacionClass.php:L549-L559`; `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/embarques/CotizacionClass.php:L549-L558`.
- **G03:** `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/parametros/clientes/ClienteProveedorClass.php:L12-L28`; `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/parametros/clientes/ClienteProveedorClass.php:L12-L28`.
- **G04:** `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/embarques/componentes/embarques_datos.php:L71-L78`; `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/embarques/componentes/embarques_datos.php:L71-L78`.
- **G07:** `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/embarques/SolicitudesClass.php:L160-L176`; `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/embarques/SolicitudesClass.php:L125-L141`.
- **G08:** `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/embarques/SolicitudesClass.php:L402-L408`; `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/embarques/SolicitudesClass.php:L308-L314`; `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/embarques/SolicitudesClass.php:L442-L447`; `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/embarques/SolicitudesClass.php:L348-L353`.
- **G09:** `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/embarques/componentes/inventario/index.js:L11-L16`; `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/embarques/componentes/inventario/index.js:L11-L16`.
- **G10 master:** `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/embarques/componentes/inventario/parte-recepcion.js:L27-L48`.
- **G10 Perú:** `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/embarques/componentes/inventario/parte-recepcion.js:L1-L31`; `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/embarques/componentes/inventario/parte-recepcion.js:L54-L77`.
- **G11:** `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/embarques/frames/items.php:L61-L76`; `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/embarques/ajax/FlujoCrearViajeDesdeItems.php:L19-L54`; `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/embarques/ajax/FlujoCrearViajeDesdeItems.php:L68-L106`.
- **G14:** `master@a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/embarques/componentes/estado-pedidos/controllers/EstadoPedidosClass.php:L117-L138`; `origin/master_peru@95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/embarques/componentes/estado-pedidos/controllers/EstadoPedidosClass.php:L117-L138`.

## Disposición de los 891 candidatos históricos

La fuente original es [BUSINESS_GLOSSARY.csv](../../source-audits/brownfield/reports/business_glossary/BUSINESS_GLOSSARY.csv), acompañada de [BUSINESS_GLOSSARY.md](../../source-audits/brownfield/reports/business_glossary/BUSINESS_GLOSSARY.md) y [BUSINESS_GLOSSARY_REVIEW.md](../../source-audits/brownfield/reports/business_glossary/BUSINESS_GLOSSARY_REVIEW.md). Su contenido se conserva en `source-audits`, incluidas las copias de release; no se reescribe ni se sustituye por este diccionario.

| Grupo histórico | Filas | Disposición en esta revisión |
| --- | ---: | --- |
| Business domain | 3 | Grupos genéricos históricos; no se usan como glosario de negocio terminado. |
| Business entity | 865 | Candidatos por entidad; sin promoción por parecido de nombre o por una referencia aislada. |
| Business field concept | 23 | Candidatos de campo; sin aprobación de acepción ni equivalencia automática. |
| Total | 891 | Se conserva `INFERRED_DRAFT_REVIEW_REQUIRED` en las 891 filas. |

SHA256 del CSV original: `57a0927cc7da3f5ed5263bd5865d2b6b26e573f9b9a3805e93c8bc98963826bb`.

**Residual sin validación individual: 891.** No se resta 81 a 891 porque un concepto puede reunir varias estructuras, una estructura puede servir a varios conceptos y las fuentes históricas no tienen correspondencia uno a uno con los pasajes master revisados. Cero candidatos fueron promovidos, rechazados o reclasificados individualmente por este trabajo.

Según la coordinación, el proceso principal prepara un registro de disposición de 891 filas que contrastará `source_object` con referencias SQL master y enlazará conceptos revisados solo cuando exista evidencia directa. Los candidatos de esquema que solo procedan de la historia Perú deberán conservar esa procedencia. Este documento **no afirma que esa conciliación ya exista ni que esté validada**; su resultado no se reemplaza con conteos de este glosario.

Para una promoción futura se necesita lectura de fuente por rama, definición de negocio contextual y confirmación de la acepción; para una regla regulatoria se requiere una fuente autorizada adicional. Una mención SQL es evidencia de uso, no prueba de despliegue del objeto físico.

## Validación del artefacto

**Resultado observado: comprobaciones superadas.**

- Esquema completo Draft 2020-12: comprobado y validado con `jsonschema`.
- 81 identificadores únicos; campos obligatorios, ámbitos y niveles de confianza válidos; conteos recalculados y coincidentes.
- Índices por identificador, término, alias, ámbito, confianza y categoría coherentes con las entradas. Las búsquedas de alias normalizados eliminan repeticiones del mismo identificador.
- Correspondencia entre las 81 entradas JSON y las 81 definiciones Markdown, con anclas e índice alfabético completos.
- 193 rangos de evidencia únicos contrastados contra **42 objetos archivo–commit**: existencia de archivo, rango inclusivo válido y referencia representada en Markdown. Los 76 conceptos `shared_evidence` tienen citas de ambos commits.
- Commits de ambas referencias Git coincidentes con los SHA fijados.
- CSV histórico leído de nuevo: 891 filas, distribución de categorías coincidente, 891 estados originales `INFERRED_DRAFT_REVIEW_REQUIRED` y SHA256 idéntico al registrado.
- Enlaces documentales locales válidos y sin espacios sobrantes al final de línea.

La verificación estructural complementa la inspección semántica directa; no sustituye una prueba de ejecución ni una aprobación de negocio. No se generaron ni ejecutaron pruebas de la aplicación.

No se ejecutó la aplicación. La coordinación informó que Windows App Control bloqueó el ejecutable nativo ASGARD: debe constar como **no ejecutado**, sin atribuirle resultados del escaneo estático alternativo. El Dockerfile master usa PHP 5.4; una comprobación con PHP 8.4, si se incorpora desde el proceso paralelo, es solo un resultado sobre ese intérprete y no validación de la ejecución prevista.

## Reproducción de la validación JSON

Desde la raíz del repositorio de conocimiento, con Python y `jsonschema` disponibles:

```powershell
python -c "import json,jsonschema,pathlib; d=json.loads(pathlib.Path('knowledge/glossary/business-glossary.json').read_text(encoding='utf-8')); jsonschema.Draft202012Validator.check_schema(d['schema']); jsonschema.Draft202012Validator(d['schema']).validate(d); print('Schema OK')"
```

Los controles de correspondencia entre índices, conteos y archivos Git se describen arriba y son adicionales al esquema: JSON Schema no prueba que el texto citado respalde una definición. Esa revisión requirió lectura directa.
